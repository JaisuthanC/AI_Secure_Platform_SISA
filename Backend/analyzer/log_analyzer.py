import re

def analyze_logs(content):
    findings = []
    lines = content.split("\n")

    for i, line in enumerate(lines):

        # Email detection
        if re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", line):
            findings.append({
                "type": "email",
                "value": line,
                "risk": "low",
                "line": i + 1
            })

        # Password detection
        if re.search(r"password\s*=\s*\w+", line, re.IGNORECASE):
            findings.append({
                "type": "password",
                "risk": "critical",
                "line": i + 1
            })

        # API key detection
        if re.search(r"api[_-]?key\s*=\s*\w+", line, re.IGNORECASE):
            findings.append({
                "type": "api_key",
                "risk": "high",
                "line": i + 1
            })

        # Error / Exception detection
        if "ERROR" in line or "Exception" in line:
            findings.append({
                "type": "error",
                "risk": "medium",
                "line": i + 1
            })

    return findings