import os
import json
import logging
from datetime import datetime

# You can install the openai library to use DeepSeek's OpenAI-compatible API
# pip install openai
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# ==========================================
# CONFIGURATION
# ==========================================
LOG_CSV_PATH = r"d:\WT3D_Project\Z_Log\MAXSKILLS_Learning_Log.csv"
REPORT_JSON_PATH = r"d:\WT3D_Project\Z_Log\Observer_Report.json"

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "YOUR_DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# ==========================================
# PROMPTS & ROLE
# ==========================================
SYSTEM_PROMPT = """ROLE: AI OBSERVER / ANALYST (READ-ONLY)

MISSION:
You are an AI responsible ONLY for monitoring system operation,
logging data, analyzing patterns, and proposing high-level improvements.

ALLOWED ACTIONS (ONLY):
1. Observe runtime data and logs
2. Evaluate system stability and risk
3. Analyze patterns, trends, and anomalies
4. Propose improvement ideas at conceptual level

FORBIDDEN ACTIONS (ABSOLUTE):
- Do NOT modify code
- Do NOT execute or trigger actions
- Do NOT change parameters or thresholds
- Do NOT control runtime behavior
- Do NOT act as decision-maker or autopilot

OUTPUT FORMAT (JSON ONLY, MUST START WITH { AND END WITH }):
{
  "stability_rating": "GOOD | WARNING | CRITICAL",
  "pattern_detected": "...",
  "risk_assessment": "...",
  "root_cause_hypothesis": "...",
  "improvement_suggestion": "conceptual recommendation only"
}

RULES OF THINKING:
- Observation before judgment
- Evidence-based analysis only
- If uncertain, explicitly state uncertainty
- Prefer system stability over optimization
- Never exceed observer authority

CORE PRINCIPLE:
You are a flight recorder and analyst, NOT a controller.
If you attempt to act, decide, or modify the system, you are violating your role.
"""

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def get_recent_logs(lines_to_read=10):
    """Retrieve the most recent operation logs from the CSV."""
    if not os.path.exists(LOG_CSV_PATH):
        return "No log file found."
    
    try:
        with open(LOG_CSV_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        header = lines[0].strip() if len(lines) > 0 else "Timestamp,Model,Profile,PartCount,BlockedCount,Health,Status,RiskPattern,OverrideSource"
        data_lines = [line.strip() for line in lines[1:] if line.strip()]
        
        recent = data_lines[-lines_to_read:] if len(data_lines) >= lines_to_read else data_lines
        
        log_content = f"CSV HEADER: {header}\n"
        for i, row in enumerate(recent, 1):
            log_content += f"Row -{len(recent)-i+1}: {row}\n"
            
        return log_content
    except Exception as e:
        return f"Error reading logs: {str(e)}"

def analyze_logs_with_deepseek(log_data):
    """Call DeepSeek API to analyze the logs."""
    if OpenAI is None:
        logging.error("OpenAI package is not installed. Please run 'pip install openai'")
        return None
        
    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
    
    prompt = f"Analyze the following recent system logs:\n\n{log_data}"
    
    logging.info("Sending observation context to DeepSeek API...")
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.0 # Zero temperature for strict observational logic
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"DeepSeek API Error: {str(e)}")
        return None

def main():
    logging.info("Starting AI Observer Routine...")
    logs = get_recent_logs(20) # Read last 20 operations
    
    if "No log file found" in logs:
        logging.warning(logs)
        return
        
    logging.info("Recent logs extracted. Analyzing...")
    
    # Analyze with DeepSeek
    # Note: Will fail gracefully if API key is invalid or module missing.
    # For proof-of-concept/testing without an API key, we mock the output if API call fails
    result = analyze_logs_with_deepseek(logs)
    
    if not result:
        logging.info("Falling back to local static JSON template due to API absence.")
        result = json.dumps({
            "stability_rating": "WARNING",
            "pattern_detected": "(Mock) API Key missing. No real pattern analyzed.",
            "risk_assessment": "(Mock) Cannot assess without API.",
            "root_cause_hypothesis": "(Mock) N/A",
            "improvement_suggestion": "(Mock) Supply DEEPSEEK_API_KEY environment variable."
        }, indent=2)
        
    # Write report
    try:
        report_dir = os.path.dirname(REPORT_JSON_PATH)
        if report_dir and not os.path.exists(report_dir):
            os.makedirs(report_dir)
            
        with open(REPORT_JSON_PATH, "w", encoding="utf-8") as f:
            if isinstance(result, str):
                f.write(result)
            else:
                json.dump(result, f, indent=2)
                
        logging.info(f"Observer Report generated at {REPORT_JSON_PATH}")
        print("\n--- AI OBSERVER REPORT ---")
        print(result)
        print("--------------------------")
    except Exception as e:
        logging.error(f"Failed to write report: {str(e)}")

if __name__ == "__main__":
    main()
