import re

def detect_sensitive_data(text):
    findings = []

    email_pattern = r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+"
    password_pattern = r"password\s*=\s*\S+"
    api_key_pattern = r"sk-[a-zA-Z0-9]+"

    lines = text.split("\n")

    for i, line in enumerate(lines):

        if re.search(email_pattern, line):
            findings.append({
                "type": "email",
                "line": i,
                "risk": "low"
            })

        if re.search(password_pattern, line):
            findings.append({
                "type": "password",
                "line": i,
                "risk": "critical"
            })

        if re.search(api_key_pattern, line):
            findings.append({
                "type": "api_key",
                "line": i,
                "risk": "high"
            })

    return findings