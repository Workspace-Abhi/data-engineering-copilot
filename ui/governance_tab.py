"""Data Governance agent interface tab."""
import streamlit as st
from agents.data_governance_agent import get_data_governance_agent
from utils.helpers import create_download_link

def render_governance_tab():
    st.header("🛡️ Data Governance Agent")
    st.caption("Generate RBAC policies and target field classification / PII detection rules")

    gov_agent = get_data_governance_agent()

    chat_sub, rbac_sub, pii_sub = st.tabs(["💬 Chat", "👥 RBAC Configuration", "🏷️ PII Masking Rules"])

    with chat_sub:
        query = st.text_area("Ask about security policies & data governance:",
                             placeholder="How do I write column masking rules for sensitive fields in Snowflake?",
                             key="gov_chat_query",
                             height=100)
        if st.button("Submit Query", type="primary", key="gov_chat_submit"):
            if query:
                with st.spinner("Analyzing..."):
                    res = gov_agent.process(query)
                    st.markdown(res)

    with rbac_sub:
        st.subheader("Generate RBAC Policy JSON")
        roles_input = st.text_area("User Roles (comma separated)", value="admin, data_engineer, analyst", key="gov_rbac_roles")
        resources_input = st.text_area("Restricted Tables (comma separated)", value="customers, transactions, transactions_summary", key="gov_rbac_res")
        if st.button("Generate RBAC Policy", type="primary", key="gov_rbac_btn"):
            try:
                roles = [r.strip() for r in roles_input.split(",") if r.strip()]
                resources = [r.strip() for r in resources_input.split(",") if r.strip()]
                policy_json = gov_agent.generate_rbac_policy(roles, resources)
                st.code(policy_json, language="json")
                st.markdown(create_download_link(policy_json, "rbac_policy.json", "application/json"), unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Failed to generate: {e}")

    with pii_sub:
        st.subheader("PII Detection & Masking Rules Mapping")
        cols_input = st.text_area("List of Columns to Classify (comma separated)", value="id, email_address, phone_number, age, salary, creation_date", key="gov_pii_cols")
        if st.button("Detect sensitive fields & Generate Rules", type="primary", key="gov_pii_btn"):
            try:
                columns = [c.strip() for c in cols_input.split(",") if c.strip()]
                rules_json = gov_agent.generate_pii_detection_rules(columns)
                st.code(rules_json, language="json")
                st.markdown(create_download_link(rules_json, "pii_masking_rules.json", "application/json"), unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Failed to generate: {e}")
