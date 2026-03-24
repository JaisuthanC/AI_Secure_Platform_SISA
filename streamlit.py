import streamlit as st
import requests
from Backend.analyzer.log_analyzer import analyze_logs
from Backend.analyzer.risk_engine import calculate_risk
# Page config

st.set_page_config(page_title="AI Secure Platform", layout="wide")
st.markdown(
    """
    <style>
    /* Hide default Streamlit header */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* Custom top bar */
    .top-bar {
        background: linear-gradient(to right, #4169E1, #00C9FF);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        color: white;
        box-shadow: 0 0 15px #00C9FF;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, #0A0F2C, #121A3A);
        color: white;
    }

    /* Buttons */
    .stButton>button {
        background-color: #4169E1;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
    }

    .stButton>button:hover {
        background-color: #00C9FF;
        color: black;
    }

    /* Text Area */
    textarea {
        background-color: #121A3A !important;
        color: white !important;
        border-radius: 10px !important;
    }

    /* File uploader */
    .stFileUploader {
        background-color: #121A3A;
        border-radius: 10px;
        padding: 10px;
    }

    /* Headers */
    h1, h2, h3 {
        color: #00C9FF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title

st.markdown(
    """
    <div class="top-bar">
        🔐 AI Secure Data Intelligence Platform
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<center>Analyze logs to detect sensitive data, risks, and insights</center>",
    unsafe_allow_html=True
)

# Layout

colA, colB = st.columns(2)

# Input Section

with colA:
    st.subheader("📥 Input Data")
    input_text = st.text_area("Paste Logs / Text", height=200)
    uploaded_file = st.file_uploader("Upload Log File", type=["txt", "log"])


    analyze_btn = st.button("🚀 Analyze")

# Output Section

with colB:
    st.subheader("📊 Results")


if analyze_btn:

    with st.spinner("Analyzing..."):

        text = input_text

        if uploaded_file is not None:
            text = uploaded_file.read().decode("utf-8")

        if not text:
            st.warning("Please enter text or upload a file")

        else:
            try:
                findings = analyze_logs(text)
                score, level = calculate_risk(findings)

                data = {
                "summary": "Log contains sensitive data",
                "content_type": "log",
                "findings": findings,
                "risk_score": score,
                "risk_level": level,
                "action": "masked",
                "insights": [
                    "Sensitive credentials exposed",
                 "Potential security risks detected",
                    "System errors found in logs"
                            ]
}
                st.markdown("## 📊 Summary")
                st.info(data["summary"])

                st.markdown("## ⚠ Risk Score")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Risk Score", data["risk_score"])

                with col2:
                    if data["risk_level"] == "high":
                        st.error(data["risk_level"].upper())
                    elif data["risk_level"] == "medium":
                        st.warning(data["risk_level"].upper())
                    else:
                        st.success(data["risk_level"].upper())

                

                    # Findings
                    st.markdown("### 🔍 Findings")
                    for f in data["findings"]:
                        st.write(f"• {f['type'].upper()} → {f['risk']} (line {f['line']})")

                    # Insights
                    st.markdown("### 💡 Insights")
                    for i in data["insights"]:
                        st.write(f"• {i}")

                    # Log Viewer
                    st.markdown("### 📜 Log Viewer")

                    lines = text.split("\n")
                    for idx, line in enumerate(lines):
                        is_risk = any(f["line"] == idx + 1 for f in data["findings"])

                        if is_risk:
                            st.markdown(f"🔴 **{idx+1}: {line}**")
                        else:
                            st.markdown(f"{idx+1}: {line}")

            except Exception as e:
                st.error("Error connecting to backend")
                st.write(e)
