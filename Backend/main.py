from fastapi import FastAPI
from pydantic import BaseModel
from analyzer.regex_detector import detect_sensitive_data
from analyzer.log_analyzer import analyze_logs
from analyzer.risk_engine import calculate_risk

app = FastAPI()

class RequestModel(BaseModel):
    input_type: str
    content: str

@app.get("/")
def home():
    return {"message": "Server Running"}

@app.post("/analyze")
def analyze(data: RequestModel):

    # 1. Detect findings
    if data.input_type == "log":
        findings = analyze_logs(data.content)
    else:
        findings = []

    # 2. Calculate risk
    score, level = calculate_risk(findings)

    # 3. Create summary
    summary = "Log contains "

    if any(f["type"] == "password" for f in findings):
        summary += "sensitive credentials, "

    if any(f["type"] == "api_key" for f in findings):
        summary += "API keys, "

    if any(f["type"] == "error" for f in findings):
        summary += "system errors, "

    summary = summary.rstrip(", ")

    # ✅ 4. ADD THIS LINE HERE (INSIDE FUNCTION)
    insights = generate_insights(findings)

    # 5. Return response
    return {
        "summary": summary,
        "content_type": data.input_type,
        "findings": findings,
        "risk_score": score,
        "risk_level": level,
        "action": "masked",
        "insights": insights   
    }
def generate_insights(findings):
    insights = []

    if any(f["type"] == "password" for f in findings):
        insights.append("Sensitive credentials exposed in logs")

    if any(f["type"] == "api_key" for f in findings):
        insights.append("API key exposed in logs")

    if any(f["type"] == "email" for f in findings):
        insights.append("User email data detected")

    if any(f["type"] == "error" for f in findings):
        insights.append("System errors and stack traces detected")

    if len(findings) == 0:
        insights.append("No major security issues detected")

    return insights    
    
    