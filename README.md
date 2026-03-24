# AI Secure Data Intelligence Platform

## Overview

AI Secure Platform is a full-stack application that analyzes logs and detects sensitive data such as emails, passwords, API keys, and system errors. It calculates risk scores and provides actionable insights to improve security.

---

## Features

- Sensitive data detection (email, password, API keys)
- Risk scoring engine (low, medium, high, critical)
- AI-generated insights
- Highlighted risky log lines
- Professional UI using Streamlit

## Tech Stack

- FastAPI (Backend API)
- Streamlit (Frontend UI)
- Python

---

## ▶️ How to Run

### 1 Start Backend

```bash
cd Backend
uvicorn main:app --reload
```

### 2 Start Frontend

```bash
cd ..
streamlit run streamlit.py
```

---

## Example Input

```text
email=admin@test.com
password=admin123
api_key=sk-prod-xyz
ERROR Exception occurred
```

---

## Output

- Detects sensitive data
- Calculates risk score and level
- Generates insights
- Highlights risky log lines

---

## Use Case

This system helps organizations identify sensitive information exposure in logs and improve security monitoring.

---

## Author

Jaisuthan
