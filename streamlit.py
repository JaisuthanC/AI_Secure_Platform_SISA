import streamlit as st
import requests

# Page config

st.set_page_config(page_title="AI Secure Platform", layout="wide")

# Custom CSS for styling

st.markdown(""" <style>
.main-title {
font-size: 32px;
font-weight: bold;
text-align: center;
margin-bottom: 10px;
}
.subtitle {
text-align: center;
color: gray;
margin-bottom: 30px;
}
.card {
padding: 15px;
border-radius: 10px;
background-color: #f9f9f9;
margin-bottom: 15px;
border: 1px solid #ddd;
} </style>
""", unsafe_allow_html=True)

# Title

st.markdown('<div class="main-title">🔐 AI Secure Data Intelligence Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Analyze logs to detect sensitive data, risks, and insights</div>', unsafe_allow_html=True)

# Layout

col1, col2 = st.columns(2)

# Input Section

with col1:
    st.subheader("📥 Input Data")
    input_text = st.text_area("Paste Logs / Text", height=200)
    uploaded_file = st.file_uploader("Upload Log File", type=["txt", "log"])


    analyze_btn = st.button("🚀 Analyze")

# Output Section

with col2:
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
                response = requests.post(
                    "http://127.0.0.1:8000/analyze",
                    json={
                        "input_type": "log",
                        "content": text
                    }
                )

                data = response.json()
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
