import streamlit as st
import json
from Backend.analyzer.log_analyzer import analyze_logs
from Backend.analyzer.risk_engine import calculate_risk

st.set_page_config(page_title="AI Secure Platform", layout="wide")

st.markdown("""
<style>
header, footer, #MainMenu {visibility: hidden;}

/* BACKGROUND */
.stApp {
    background: #0b0b0f;
    color: #f1f5f9;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}

/* TOP BAR */
.top-bar {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(20px);
    padding: 18px;
    border-radius: 16px;
    text-align: center;
    font-size: 24px;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 30px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* CARD */
.card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(20px);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* METRIC */
.metric {
    background: rgba(255,255,255,0.03);
    border-radius: 14px;
    padding: 15px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.06);
}

/* BUTTON */
.stButton>button {
    background: #1c1c1e;
    color: #f1f5f9;
    border-radius: 12px;
    padding: 10px 20px;
    border: 1px solid rgba(255,255,255,0.08);
    transition: 0.2s ease;
}

.stButton>button:hover {
    background: #2c2c2e;
}

/* TEXT AREA */
textarea {
    background-color: #111113 !important;
    color: #f1f5f9 !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.06);
}

/* HEADINGS */
h1, h2, h3 {
    color: #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown('<div class="top-bar"> AI Secure Data Intelligence Platform</div>', unsafe_allow_html=True)

# ---------- INPUT ----------
st.markdown("## Input Data")

input_text = st.text_area("Paste Logs / Text", height=200)
uploaded_file = st.file_uploader("Upload Log File", type=["txt", "log"])
analyze_btn = st.button(" Analyze")

# ---------- RESULTS ----------
if analyze_btn:

    text = input_text
    if uploaded_file:
        text = uploaded_file.read().decode("utf-8")

    if not text:
        st.warning("Please enter text or upload file")

    else:
        findings = analyze_logs(text)
        score, level = calculate_risk(findings)

        # ---------- OVERVIEW ----------
        st.markdown("## Overview")

        m1, m2, m3 = st.columns(3)

        with m1:
            st.markdown(f'<div class="metric">Issues<br><h2>{len(findings)}</h2></div>', unsafe_allow_html=True)

        with m2:
            st.markdown(f'<div class="metric">Risk Score<br><h2>{score}</h2></div>', unsafe_allow_html=True)

        with m3:
            color = "#22c55e"
            if level == "high":
                color = "#ef4444"
            elif level == "medium":
                color = "#f59e0b"

            st.markdown(f'<div class="metric" style="background:{color}">RISK<br><h2>{level.upper()}</h2></div>', unsafe_allow_html=True)

        # ---------- INSIGHTS ----------
        st.markdown("##  AI Insights")

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.write(
            f"Detected {len(findings)} potential security issues. "
            f"The system identifies sensitive data exposure and categorizes risks based on severity."
        )

        st.write("• Sensitive credentials exposed")
        st.write("• Potential security risks detected")
        st.write("• System errors found in logs")

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------- TABLE ----------
        st.markdown("##  Detected Risks")

        table = []
        for f in findings:
            table.append({
                "Line": f["line"],
                "Type": f["type"].upper(),
                "Severity": f["risk"].upper(),
                "Description": f"{f['type']} detected"
            })

        st.dataframe(table, use_container_width=True)

        # ---------- DOWNLOAD ----------
        st.markdown("##  Download Report")

        report = json.dumps(table, indent=4)

        st.download_button(
            "⬇ Download Report",
            data=report,
            file_name="report.json",
            mime="application/json"
        )