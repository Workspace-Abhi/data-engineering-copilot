"""Pipeline observability agent interface tab."""
import streamlit as st
from agents.observability_agent import get_observability_agent
from utils.helpers import create_download_link

def render_observability_tab():
    st.header("👁️ Observability Agent")
    st.caption("Design SLI/SLO pipelines targets and generate Prometheus/Grafana alerts configurations")

    obs_agent = get_observability_agent()

    chat_sub, sli_sub, alert_sub = st.tabs(["💬 Chat", "📐 SLI/SLO Definitions", "🚨 Prometheus Alert Rules"])

    with chat_sub:
        query = st.text_area("Ask about system observability & alerts:",
                             placeholder="How can I construct an alert query for spikes in spark job write times?",
                             key="obs_chat_query",
                             height=100)
        if st.button("Submit Query", type="primary", key="obs_chat_submit"):
            if query:
                with st.spinner("Analyzing..."):
                    res = obs_agent.process(query)
                    st.markdown(res)

    with sli_sub:
        st.subheader("Define SLI/SLO Targets")
        service_name = st.text_input("Pipeline / Service Name", value="IncrementalIngestionPipeline", key="obs_service")
        if st.button("Generate SLA Framework", type="primary", key="obs_sli_btn"):
            framework = obs_agent.generate_sli_slo_definitions(service_name)
            st.markdown(framework)
            st.markdown(create_download_link(framework, f"sli_slo_{service_name}.md", "text/markdown"), unsafe_allow_html=True)

    with alert_sub:
        st.subheader("Generate Prometheus Alerting Configurations")
        if st.button("Generate Alert Rules", type="primary", key="obs_alert_btn"):
            rules = obs_agent.generate_alert_rules()
            st.code(rules, language="yaml")
            st.markdown(create_download_link(rules, "prometheus_alert_rules.yml", "text/yaml"), unsafe_allow_html=True)
