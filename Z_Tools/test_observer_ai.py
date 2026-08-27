import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import requests

import Observer_AI_v4_DEEPSEEK as observer

class TestObserverAI(unittest.TestCase):

    def test_safe_float(self):
        self.assertEqual(observer.safe_float("1.23"), 1.23)
        self.assertEqual(observer.safe_float("0"), 0.0)
        self.assertEqual(observer.safe_float("invalid", 4.0), 4.0)
        self.assertEqual(observer.safe_float(None), 0.0)

    @patch('Observer_AI_v4_DEEPSEEK.logging.warning')
    def test_extract_missing_columns(self, mock_warning):
        # Create row missing the "RiskScore" and "GovernorClamp" columns
        rows = [
            {"Health": "100", "PrefightTriggered": "True"},
            {"Health": "90", "PrefightTriggered": "False"}
        ]
        metrics = observer.extract(rows)
        
        # Verify it falls back to safe_float defaults (0.0)
        self.assertEqual(metrics["risk"], [0.0, 0.0])
        self.assertEqual(metrics["clamp"], [0.0, 0.0])
        self.assertEqual(metrics["prefight"], [1, 0])
        
        # It should log warning exactly once per missing key, despite 2 rows
        self.assertEqual(mock_warning.call_count, 2)
        mock_warning.assert_any_call("CSV is missing column Data: '%s'. Substituting 0.0", "RiskScore")
        mock_warning.assert_any_call("CSV is missing column Data: '%s'. Substituting 0.0", "GovernorClamp")

    def test_trend_analysis_insufficient_data(self):
        original_min = observer.CONFIG["MIN_SAMPLE_SIZE"]
        observer.CONFIG["MIN_SAMPLE_SIZE"] = 10
        
        metrics = { "risk": [0.1, 0.2, 0.3], "health": [90, 80], "clamp": [0] }
        result = observer.trend_analysis(metrics)
        self.assertEqual(result["status"], "UNCERTAIN")
        
        observer.CONFIG["MIN_SAMPLE_SIZE"] = original_min

    def test_trend_analysis_valid(self):
        original_min = observer.CONFIG["MIN_SAMPLE_SIZE"]
        observer.CONFIG["MIN_SAMPLE_SIZE"] = 10
        recent = observer.CONFIG["RECENT_WINDOW"]
        base_size = 10 - recent
        
        metrics = {
            "risk": [0.1] * base_size + [0.8] * recent,
            "health": [100.0] * base_size + [70.0] * recent,
            "clamp": [0] * base_size + [1, 0, 1, 0, 0][:recent]
        }
        
        result_valid = observer.trend_analysis(metrics)
        self.assertAlmostEqual(result_valid["base_risk"], 0.1)
        self.assertTrue(result_valid["risk_trend"] > 0)
        self.assertGreaterEqual(result_valid["early_warning_score"], 3)
        
        # Check standard deviation calculation exists
        self.assertIn("risk_volatility", result_valid)
        self.assertIn("health_volatility", result_valid)
        
        observer.CONFIG["MIN_SAMPLE_SIZE"] = original_min

    def test_trend_analysis_volatility_and_config(self):
        original_thresh = observer.CONFIG.get("RISK_VOLATILITY_THRESHOLD", 0.2)
        observer.CONFIG["MIN_SAMPLE_SIZE"] = 10
        
        # Mock high amplitude variance to force high pstdev calculation
        metrics = {
            "risk": [0.1, 0.9, 0.1, 0.9, 0.1, 0.9] * 2,  
            "health": [100, 20, 100, 20, 100, 20] * 2,
            "clamp": [0] * 12
        }
        
        # Scenario 1: Low threshold -> Should trigger EWS increment
        observer.CONFIG["RISK_VOLATILITY_THRESHOLD"] = 0.1
        result = observer.trend_analysis(metrics)
        self.assertGreater(result["risk_volatility"], 0.3)
        self.assertGreater(result["health_volatility"], 30.0)
        self.assertGreaterEqual(result["early_warning_score"], 1)

        # Scenario 2: High threshold -> Should NOT trigger EWS increment
        observer.CONFIG["RISK_VOLATILITY_THRESHOLD"] = 1.0
        result_high = observer.trend_analysis(metrics)
        self.assertLess(result_high["early_warning_score"], result["early_warning_score"])
        
        observer.CONFIG["RISK_VOLATILITY_THRESHOLD"] = original_thresh

    @patch('Observer_AI_v4_DEEPSEEK.requests.post')
    def test_deepseek_interpret_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        
        expected_json = {
            "situation_summary": "System failing",
            "conceptual_recommendation": "Fix logic"
        }
        
        mock_response.json.return_value = {
            "choices": [{"message": {"content": json.dumps(expected_json)}}]
        }
        mock_post.return_value = mock_response
        
        result = observer.deepseek_interpret({"test": "data"})
        self.assertEqual(result["situation_summary"], "System failing")

    @patch('Observer_AI_v4_DEEPSEEK.time.sleep', return_value=None)
    @patch('Observer_AI_v4_DEEPSEEK.requests.post')
    def test_deepseek_interpret_retry_logic(self, mock_post, mock_sleep):
        # Setup mock to raise exceptions consistently
        mock_post.side_effect = requests.exceptions.RequestException("Network Error Mock")
        
        # Override config so retries happen fast
        observer.CONFIG["MAX_RETRIES"] = 3
        
        result = observer.deepseek_interpret({"risk": "high"})
        
        # Should attempt 3 times
        self.assertEqual(mock_post.call_count, 3)
        self.assertEqual(result["situation_summary"], "DeepSeek request failed consistently")
        self.assertIn("Check API connection", result["conceptual_recommendation"])

    @patch('Observer_AI_v4_DEEPSEEK.requests.post')
    def test_deepseek_interpret_json_decode_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        
        # Respond with invalid JSON
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "not a json string at all"}}]
        }
        mock_post.return_value = mock_response
        
        result = observer.deepseek_interpret({"risk": "high"})
        self.assertEqual(result["situation_summary"], "DeepSeek returned invalid format")

    @patch('builtins.open', new_callable=mock_open)
    def test_write_report(self, mock_file):
        observer.write_report({"trend": 1}, {"llm": "data"}, 15)
        
        # Check that file was opened in append mode
        mock_file.assert_called_with(observer.CONFIG["REPORT_PATH"], "a", encoding="utf-8")
        
        # Capture what was written
        handle = mock_file()
        written = "".join(call.args[0] for call in handle.write.mock_calls)
        
        # Parse it to verify structure
        parsed = json.loads(written.strip())
        self.assertEqual(parsed["sample_count"], 15)
        self.assertEqual(parsed["trend_analysis"]["trend"], 1)

    @patch('Observer_AI_v4_DEEPSEEK.read_csv')
    @patch('Observer_AI_v4_DEEPSEEK.write_report')
    @patch('Observer_AI_v4_DEEPSEEK.deepseek_interpret')
    @patch('Observer_AI_v4_DEEPSEEK.logging.info')
    def test_main_flow(self, mock_info, mock_interpret, mock_write, mock_read):
        # Mock CSV reading -> Returns robust mocked data
        mock_rows = [
            {"RiskScore": "0.1", "Health": "100", "GovernorClamp": "0", "PrefightTriggered": "False"}
            for _ in range(12)
        ]
        mock_read.return_value = mock_rows
        
        mock_interpret.return_value = {"situation": "MOCK_OK"}
        
        # Execute main
        observer.main()
        
        # Verify read_csv was called once with correct path
        mock_read.assert_called_once_with(observer.CONFIG["LOG_CSV_PATH"])
        
        # Verify write_report was called with len(rows) = 12
        self.assertTrue(mock_write.called)
        self.assertEqual(mock_write.call_args[0][2], 12)
        
        # Verify logging
        mock_info.assert_any_call("Observer_AI_v4_DEEPSEEK complete.")

if __name__ == "__main__":
    unittest.main()
