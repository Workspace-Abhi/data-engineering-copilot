"""Data testing agent interface tab."""
import streamlit as st
from agents.testing_agent import get_testing_agent
from utils.helpers import create_download_link

def render_testing_tab():
    st.header("🧪 Data Testing Agent")
    st.caption("Generate SQL reconciliation assertions and mock datasets insert queries")

    testing_agent = get_testing_agent()

    chat_sub, sql_sub, mock_sub = st.tabs(["💬 Chat", "📐 SQL Unit Tests", "📁 Mock Data Generator"])

    with chat_sub:
        query = st.text_area("Ask about testing methodologies:",
                             placeholder="How can I test for duplicated keys and orphan rows dynamically?",
                             key="test_chat_query",
                             height=100)
        if st.button("Submit Query", type="primary", key="test_chat_submit"):
            if query:
                with st.spinner("Analyzing..."):
                    res = testing_agent.process(query)
                    st.markdown(res)

    with sql_sub:
        st.subheader("Generate SQL Unit Test")
        test_name = st.text_input("Test Case Description", value="check_customer_name_transformation", key="test_sql_name")
        expected = st.text_area("Expected Dataset SQL Query", value="SELECT id, UPPER(name) AS name FROM raw_customers", key="test_sql_exp", height=80)
        actual = st.text_area("Actual Dataset SQL Query", value="SELECT id, name FROM dim_customers", key="test_sql_act", height=80)
        if st.button("Generate SQL Assertion", type="primary", key="test_sql_btn"):
            code = testing_agent.generate_sql_unit_test(test_name, expected, actual)
            st.code(code, language="sql")
            st.markdown(create_download_link(code, f"test_{test_name}.sql", "text/sql"), unsafe_allow_html=True)

    with mock_sub:
        st.subheader("Generate Mock Datasets inserts")
        count = st.slider("Number of Rows to generate", 1, 50, 5, key="test_mock_count")
        cols_input = st.text_area("Columns Definition (JSON format)",
                                  value='[\n  {"name": "id", "type": "int"},\n  {"name": "email", "type": "varchar"},\n  {"name": "score", "type": "float"}\n]',
                                  key="test_mock_cols",
                                  height=100)
        if st.button("Generate Mock Data", type="primary", key="test_mock_btn"):
            try:
                import json
                columns = json.loads(cols_input)
                inserts_sql = testing_agent.generate_mock_data(columns, count)
                st.code(inserts_sql, language="sql")
                st.markdown(create_download_link(inserts_sql, "mock_inserts.sql", "text/sql"), unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Failed to generate: {e}")
