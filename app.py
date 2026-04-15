import streamlit as st
from PIL import Image
import ocr_utils
import model as model

st.set_page_config(
    page_title="HealthScan AI",
    page_icon="🏥",
    layout="wide"
)

st.markdown("""
<style>
/* Background */
.stApp {
    background: ;
}

/* Header */
.main-header {
    
    font-size: 42px;
    font-weight: bold;
    color: white;
    text-align: center;
    margin-bottom: 10px;
}

.sub-header {
    text-align: center;
    color: #475569;
    margin-bottom: 30px;
}



/* Buttons */
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    height: 45px;
    font-size: 16px;
}

/* Text area */
textarea {
    border-radius: 10px !important;
}

/* Footer */
.footer {
    text-align: center;
    font-size: 13px;
    color: gray;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🏥 HealthScan AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Medical Report Analyzer</div>', unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📥 Upload or Enter Report")

    input_mode = st.radio(
        "Choose Input Method:",
        ["📷 Upload Image", "📝 Paste Text"],
        horizontal=True
    )

    report_text = ""

    if input_mode == "📷 Upload Image":
        uploaded_file = st.file_uploader("Upload Report", type=["jpg", "png", "jpeg"])

        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="Uploaded Report", use_column_width=True)

            with st.spinner("🔍 Extracting text using AI OCR..."):
                raw_text = ocr_utils.extract_text_from_image(img)

            report_text = st.text_area(
                "✏️ Review & Edit Extracted Text:",
                value=raw_text,
                height=200
            )

    else:
        report_text = st.text_area(
            "Paste Medical Report:",
            height=250,
            placeholder="Paste CBC, LFT, MRI findings..."
        )

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔬 AI Clinical Analysis")

    if st.button("🚀 Analyze Report", use_container_width=True):
        if report_text.strip():

            with st.spinner("🧠 Analyzing medical data..."):
                summary, findings, alerts, suggestions = model.analyze_complex_report(report_text)

            # Summary
            st.success(f"🧾 **Summary:** {summary}")

            # Alerts
            if alerts:
                st.error("🚨 Critical Alerts")
                for a in alerts:
                    st.markdown(f"- **{a}**")
            else:
                st.success("✅ No major abnormalities detected.")

            # Findings
            with st.expander("📋 Detailed Findings", expanded=True):
                if findings:
                    for f in findings:
                        st.write(f"• {f}")
                else:
                    st.write("No significant findings.")

            # Suggestions
            st.warning("💡 Recommendations")
            if suggestions:
                for s in suggestions:
                    st.markdown(f"👉 {s}")
            else:
                st.write("Consult a Doctor for routine evaluation.")

        else:
            st.warning("⚠️ Please provide report data.")

    st.markdown('</div>', unsafe_allow_html=True)

st.divider()
st.markdown(
    '<div class="footer">🚨 This tool is for educational purposes only. Always consult a certified doctor.</div>',
    unsafe_allow_html=True
)