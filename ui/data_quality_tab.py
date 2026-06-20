"""Data Quality Agent interface tab."""
import streamlit as st
from agents.data_quality_agent import get_data_quality_agent
from utils.helpers import create_download_link

def render_data_quality_tab():
    st.header("⚡ Data Quality Agent")
    st.caption("Generate Great Expectations suites and Soda Core data validation checks")

    dq_agent = get_data_quality_agent()

    chat_sub, ge_sub, soda_sub = st.tabs(["💬 Chat", "📐 Great Expectations Suite", "🥤 Soda Core Checks"])

    with chat_sub:
        query = st.text_area("Ask about data quality validations:",
                             placeholder="How should I set up null checks for email and range checks for age?",
                             key="dq_chat_query",
                             height=100)
        if st.button("Submit Query", type="primary", key="dq_chat_submit"):
            if query:
                with st.spinner("Analyzing..."):
                    res = dq_agent.process(query)
                    st.markdown(res)

    with ge_sub:
        st.subheader("Generate Great Expectations Suite")
        table_name = st.text_input("Table Name", value="users", key="ge_table_name")
        cols_input = st.text_area("Columns Definition (JSON format)",
                                  value='[\n  {"name": "id", "type": "int", "nullable": false},\n  {"name": "email", "type": "varchar", "nullable": true}\n]',
                                  key="ge_cols_input",
                                  height=100)
        if st.button("Generate GE Suite", type="primary", key="ge_generate_btn"):
            try:
                import json
                columns = json.loads(cols_input)
                suite_json = dq_agent.generate_great_expectations_suite(table_name, columns)
                st.code(suite_json, language="json")
                dl_link = create_download_link(suite_json, f"{table_name}_suite.json", "application/json")
                st.markdown(dl_link, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Failed to generate: {e}")

    with soda_sub:
        st.subheader("Generate Soda Core Checks")
        soda_table = st.text_input("Table Name", value="users", key="soda_table_name")
        soda_cols = st.text_area("Columns Definition (JSON format)",
                                 value='[\n  {"name": "id", "type": "int", "nullable": false},\n  {"name": "email", "type": "varchar", "nullable": true}\n]',
                                 key="soda_cols_input",
                                 height=100)
        if st.button("Generate Soda Checks", type="primary", key="soda_generate_btn"):
            try:
                import json
                columns = json.loads(soda_cols)
                checks_yaml = dq_agent.generate_soda_checks(soda_table, columns)
                st.code(checks_yaml, language="yaml")
                dl_link = create_download_link(checks_yaml, f"checks_{soda_table}.yaml", "text/yaml")
                st.markdown(dl_link, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Failed to generate: {e}")
