# ============================================================
# Observer_AI_v4_DEEPSEEK.py
# ROLE: AI OBSERVER / EARLY WARNING ANALYST (READ-ONLY)
# ============================================================

import csv
import json
import os
import time
import requests
import logging
from datetime import datetime, timezone
from statistics import mean, pstdev

# ===============================
# LOGGING SETUP
# ===============================
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ===============================
# CONFIG
# ===============================
VERSION = "Observer_AI_v4_DEEPSEEK"

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_MODEL   = "deepseek-chat"
DEEPSEEK_URL     = "https://api.deepseek.com/v1/chat/completions"

# Dynamically load observer_config.json if exists, else defaults
CONFIG = {
    "MIN_SAMPLE_SIZE": 10,
    "RECENT_WINDOW": 5,
    "LOG_CSV_PATH": "d:\\WT3D_Project\\Z_Log\\MAXSKILLS_Learning_Log.csv",
    "REPORT_PATH": "d:\\WT3D_Project\\Z_Log\\observer_report_v4.jsonl",
    "MAX_RETRIES": 3,
    "RETRY_BACKOFF": 2.0,
    "RISK_VOLATILITY_THRESHOLD": 0.2
}
config_path = "d:\\WT3D_Project\\Z_Tools\\observer_config.json"
if os.path.exists(config_path):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            CONFIG.update(json.load(f))
    except Exception as e:
        logging.warning("Failed to load config, using defaults. Error: %s", e)

# ===============================
# UTILS
# ===============================
def safe_float(v, default=0.0):
    try:
        return float(v)
    except Exception:
        return default


def read_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ===============================
# METRIC EXTRACTION
# ===============================
def extract(rows):
    m = {"risk": [], "health": [], "clamp": [], "prefight": []}
    
    logged_warnings = set()
    for r in rows:
        for key in ["RiskScore", "Health", "GovernorClamp", "PrefightTriggered"]:
            if r.get(key) is None and key not in logged_warnings:
                logging.warning("CSV is missing column Data: '%s'. Substituting 0.0", key)
                logged_warnings.add(key)
                
        m["risk"].append(safe_float(r.get("RiskScore")))
        m["health"].append(safe_float(r.get("Health")))
        m["clamp"].append(safe_float(r.get("GovernorClamp")))
        m["prefight"].append(1 if r.get("PrefightTriggered") == "True" else 0)
    return m


# ===============================
# TREND + EARLY WARNING
# ===============================
def trend_analysis(metrics):
    min_sample = CONFIG["MIN_SAMPLE_SIZE"]
    recent_win = CONFIG["RECENT_WINDOW"]

    n = len(metrics["risk"])
    if n < min_sample:
        return {"status": "UNCERTAIN", "note": "Insufficient data"}

    base_risk   = mean(metrics["risk"][:-recent_win])
    recent_risk = mean(metrics["risk"][-recent_win:])
    base_health = mean(metrics["health"][:-recent_win])
    recent_health = mean(metrics["health"][-recent_win:])

    risk_trend   = recent_risk - base_risk
    health_trend = recent_health - base_health
    
    risk_volatility = pstdev(metrics["risk"])
    health_volatility = pstdev(metrics["health"])

    ews = 0
    if risk_trend > 0: ews += 1
    if health_trend < 0: ews += 1
    if sum(metrics["clamp"][-recent_win:]) > 0: ews += 1
    
    vol_thresh = CONFIG.get("RISK_VOLATILITY_THRESHOLD", 0.2)
    if risk_volatility > vol_thresh: ews += 1

    return {
        "base_risk": round(base_risk, 3),
        "recent_risk": round(recent_risk, 3),
        "risk_trend": round(risk_trend, 3),
        "risk_volatility": round(risk_volatility, 3),
        "base_health": round(base_health, 3),
        "recent_health": round(recent_health, 3),
        "health_trend": round(health_trend, 3),
        "health_volatility": round(health_volatility, 3),
        "early_warning_score": ews,
        "warning_level": ["LOW", "MEDIUM", "HIGH", "CRITICAL"][min(ews, 3)]
    }


# ===============================
# DEEPSEEK LLM INTERPRETER
# ===============================
def deepseek_interpret(trend_result):
    prompt = f"""You are an AI OBSERVER agent inside the Antigravity system.

ROLE:
- Monitor system metrics (risk, health, clamp, prefight, volatility).
- Detect early warning signals and degradation patterns.
- Interpret trends in engineering terms, not just raw numbers.
- Provide conceptual recommendations for improvement.

STRICT RULES:
- Do NOT propose numeric tuning or parameter changes.
- Do NOT give code or execution advice.
- Do NOT alter system configuration.
- Focus ONLY on conceptual, high-level recommendations.

INPUT DATA:
{json.dumps(trend_result, indent=2)}

OUTPUT JSON ONLY:
Respond ONLY with valid JSON. Do not include markdown formatting or conversational text.
{{
  "situation_summary": "...",
  "risk_outlook": "...",
  "suspected_system_behavior": "...",
  "conceptual_recommendation": "..."
}}

STYLE:
- Clear, concise, professional.
- Explanations must be understandable to engineers and decision-makers.
- Always include reasoning for warnings or recommendations.
"""

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }

    max_retries = CONFIG.get("MAX_RETRIES", 3)
    backoff = CONFIG.get("RETRY_BACKOFF", 2.0)
    
    last_err = None
    for attempt in range(max_retries):
        try:
            r = requests.post(DEEPSEEK_URL, headers=headers, json=payload, timeout=30)
            r.raise_for_status()
            content = r.json()["choices"][0]["message"]["content"]
            # In case the model wraps the output in markdown block ```json ... ```
            content = content.replace("```json\\n", "").replace("```json", "").replace("```", "").strip()
            
            if not content.startswith("{"):
                raise json.JSONDecodeError("Output does not start with {", content, 0)
                
            return json.loads(content)
        except requests.exceptions.RequestException as req_e:
            last_err = req_e
            logging.warning("API Network Error (Attempt %d/%d): %s", attempt + 1, max_retries, req_e)
            if attempt < max_retries - 1:
                time.sleep(backoff * (attempt + 1))
        except json.JSONDecodeError as json_e:
            logging.error("Failed to parse DeepSeek JSON: %s\nContent: %s", json_e, content if 'content' in locals() else 'None')
            return {
                "situation_summary": "DeepSeek returned invalid format",
                "risk_outlook": "Unknown",
                "suspected_system_behavior": "LLM failed to adhere to JSON constraints",
                "conceptual_recommendation": "Fine-tune prompt or use strict mode"
            }
        except Exception as e:
            last_err = e
            logging.error("Unexpected error in LLM interpreter: %s", e)
            break

    logging.error("DeepSeek API exhausted after %d retries: %s", max_retries, last_err)
    return {
        "situation_summary": "DeepSeek request failed consistently",
        "risk_outlook": "Unknown",
        "suspected_system_behavior": str(last_err),
        "conceptual_recommendation": "Check API connection, key, and endpoint availability"
    }


# ===============================
# REPORT
# ===============================
def write_report(trend, llm, samples):
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "observer_version": VERSION,
        "sample_count": samples,
        "trend_analysis": trend,
        "llm_interpretation": llm
    }
    with open(CONFIG["REPORT_PATH"], "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ===============================
# MAIN
# ===============================
def main():
    rows = read_csv(CONFIG["LOG_CSV_PATH"])
    if not rows:
        logging.warning("CSV data is empty or missing! Aborting AI observation.")
        return

    metrics = extract(rows)

    trend = trend_analysis(metrics)
    llm   = deepseek_interpret(trend)

    write_report(trend, llm, len(rows))

    logging.info("Observer_AI_v4_DEEPSEEK complete.")
    logging.info("Result:\n%s", json.dumps(llm, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
