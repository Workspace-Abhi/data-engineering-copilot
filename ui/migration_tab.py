"""Data migration agent interface tab."""
import streamlit as st
from agents.data_migration_agent import get_data_migration_agent
from utils.helpers import create_download_link

def render_migration_tab():
    st.header("🚢 Data Migration Agent")
    st.caption("Generate schema migrations, feasibility assessments, and recovery rollback plans")

    mig_agent = get_data_migration_agent()

    chat_sub, assessment_sub, rollback_sub = st.tabs(["💬 Chat", "📋 Migration Assessment", "🚨 Rollback Runbook"])

    with chat_sub:
        query = st.text_area("Ask about database/warehouse migrations:",
                             placeholder="How can I migrate a live Oracle database to PostgreSQL with minimal downtime?",
                             key="mig_chat_query",
                             height=100)
        if st.button("Submit Query", type="primary", key="mig_chat_submit"):
            if query:
                with st.spinner("Analyzing..."):
                    res = mig_agent.process(query)
                    st.markdown(res)

    with assessment_sub:
        st.subheader("Generate Migration Assessment Report")
        source = st.selectbox("Source System", ["SQL Server", "Oracle", "PostgreSQL (On-Premise)", "Teradata"], key="mig_src")
        target = st.selectbox("Target System", ["Snowflake", "Google BigQuery", "AWS Redshift", "Azure Synapse"], key="mig_tgt")
        tables = st.number_input("Number of Tables in Scope", min_value=1, max_value=5000, value=50, key="mig_tables")
        if st.button("Generate Assessment", type="primary", key="mig_assess_btn"):
            report = mig_agent.generate_migration_assessment(source, target, tables)
            st.markdown(report)
            st.markdown(create_download_link(report, "migration_assessment.md", "text/markdown"), unsafe_allow_html=True)

    with rollback_sub:
        st.subheader("Generate Fallback & Rollback Runbook")
        migration_id = st.text_input("Migration Job Identifier", value="MIG_PROD_CUSTOMERS_002", key="mig_id")
        if st.button("Generate Runbook", type="primary", key="mig_rollback_btn"):
            plan = mig_agent.generate_rollback_plan(migration_id)
            st.markdown(plan)
            st.markdown(create_download_link(plan, f"rollback_runbook_{migration_id}.md", "text/markdown"), unsafe_allow_html=True)
