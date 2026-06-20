"""MLOps data agent interface tab."""
import streamlit as st
from agents.mlops_data_agent import get_mlops_data_agent
from utils.helpers import create_download_link

def render_mlops_tab():
    st.header("🤖 MLOps Data Agent")
    st.caption("Generate Feast Feature Store definitions and statistical data drift detection scripts")

    mlops_agent = get_mlops_data_agent()

    chat_sub, feast_sub, drift_sub = st.tabs(["💬 Chat", "🍱 Feast Feature Store", "📈 Data Drift Detection"])

    with chat_sub:
        query = st.text_area("Ask about MLOps data engineering patterns:",
                             placeholder="How can I compute feature store updates on demand during inference?",
                             key="ml_chat_query",
                             height=100)
        if st.button("Submit Query", type="primary", key="ml_chat_submit"):
            if query:
                with st.spinner("Analyzing..."):
                    res = mlops_agent.process(query)
                    st.markdown(res)

    with feast_sub:
        st.subheader("Generate Feast Feature Definition")
        if st.button("Generate Feast View", type="primary", key="ml_feast_btn"):
            code = mlops_agent.generate_feast_definition()
            st.code(code, language="python")
            st.markdown(create_download_link(code, "feast_features.py"), unsafe_allow_html=True)

    with drift_sub:
        st.subheader("Generate KS-Test Drift Detection script")
        if st.button("Generate KS-Test Function", type="primary", key="ml_drift_btn"):
            code = mlops_agent.generate_drift_detection_check()
            st.code(code, language="python")
            st.markdown(create_download_link(code, "drift_detector.py"), unsafe_allow_html=True)
