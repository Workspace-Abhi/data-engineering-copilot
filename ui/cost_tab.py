"""Cost optimization agent interface tab."""
import streamlit as st
from agents.cost_optimization_agent import get_cost_optimization_agent
from utils.helpers import create_download_link

def render_cost_tab():
    st.header("💰 Cost Optimization Agent")
    st.caption("Calculate optimal cluster sizes and generate storage tiering configurations")

    cost_agent = get_cost_optimization_agent()

    chat_sub, sizing_sub, tiering_sub = st.tabs(["💬 Chat", "🧮 Cluster Sizing Calculator", "📂 Storage Tiering Policy"])

    with chat_sub:
        query = st.text_area("Ask about cost optimizations:",
                             placeholder="How can I reduce compute costs on idle Snowflake SQL Warehouses?",
                             key="cost_chat_query",
                             height=100)
        if st.button("Submit Query", type="primary", key="cost_chat_submit"):
            if query:
                with st.spinner("Analyzing..."):
                    res = cost_agent.process(query)
                    st.markdown(res)

    with sizing_sub:
        st.subheader("Compute Sizing Calculator")
        workload = st.selectbox("Workload Type", ["ETL", "Interactive Query / Dashboarding", "Machine Learning Training"], key="cost_workload")
        size_gb = st.number_input("Workload Target Dataset Size (GB)", min_value=1, max_value=100000, value=250, step=10, key="cost_size")
        
        if st.button("Calculate Sizing", type="primary", key="cost_calc_btn"):
            res = cost_agent.suggest_cluster_sizing(workload, size_gb)
            st.markdown(f"#### Suggested Compute Configuration")
            st.metric("VM / Worker Size", res["suggested_vm"])
            st.metric("Base Worker Count", res["worker_count"])
            st.write(f"**Enable Autoscale:** {'Yes (Recommended)' if res['autoscale'] else 'No (Not needed)'}")
            st.info(res["notes"])

    with tiering_sub:
        st.subheader("Storage Tiering & Lifecycle Policy")
        retention = st.slider("Archive Data Threshold (Days)", 30, 730, 180, 30, key="cost_retention")
        if st.button("Generate Storage Policy", type="primary", key="cost_policy_btn"):
            policy = cost_agent.suggest_storage_tiering(retention)
            st.code(policy, language="json")
            st.markdown(create_download_link(policy, "storage_lifecycle_policy.json", "application/json"), unsafe_allow_html=True)
