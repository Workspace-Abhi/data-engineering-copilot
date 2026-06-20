"""SQL agent interface tab."""
import streamlit as st
from config.logging_config import get_logger
from agents.sql_agent import get_sql_agent
from utils.helpers import format_code_block

logger = get_logger("sql_tab")

def render_sql_tab():
    """Render the SQL agent interface."""
    st.header("🗃️ SQL Agent")
    st.caption("SQL validation, reconciliation, CDC, and MERGE operations")

    sql_agent = get_sql_agent()

    # Sub-tabs for different SQL operations
    sub_tab = st.radio(
        "Select Operation",
        ["💬 Chat", "✅ Validate Query", "🔄 Generate MERGE", "📊 Generate CDC", "🔍 Reconcile Data"],
        horizontal=True
    )

    if sub_tab == "💬 Chat":
        query = st.text_area("Ask about SQL:", placeholder="How do I optimize this query? Write a MERGE statement for...", height=100)
        if st.button("Submit", type="primary", key="sql_submit"):
            if query:
                with st.spinner("Analyzing..."):
                    response = sql_agent.process(query)
                    st.markdown(response)

    elif sub_tab == "✅ Validate Query":
        col1, col2 = st.columns([3, 1])
        with col1:
            sql_input = st.text_area("SQL Query to Validate:", placeholder="Paste your SQL query here...", height=200)
        with col2:
            dialect = st.selectbox("Dialect", ["sqlserver", "mysql", "postgresql", "oracle", "snowflake", "bigquery"])

        if st.button("Validate", type="primary"):
            if sql_input:
                with st.spinner("Validating..."):
                    result = sql_agent.validate_query(sql_input, dialect)
                    st.markdown(result["validation"])

    elif sub_tab == "🔄 Generate MERGE":
        col1, col2 = st.columns(2)
        with col1:
            source_table = st.text_input("Source Table", "staging.Customers")
            target_table = st.text_input("Target Table", "dbo.Customers")
        with col2:
            key_cols = st.text_input("Key Columns (comma-separated)", "CustomerID")
            update_cols = st.text_input("Update Columns (comma-separated)", "Name, Email, ModifiedDate")

        if st.button("Generate MERGE", type="primary"):
            key_columns = [c.strip() for c in key_cols.split(",")]
            update_columns = [c.strip() for c in update_cols.split(",")]
            merge_sql = sql_agent.generate_merge(source_table, target_table, key_columns, update_columns)
            st.code(merge_sql, language="sql")
            st.download_button("Download SQL", merge_sql, file_name="merge_statement.sql")

    elif sub_tab == "📊 Generate CDC":
        table_name = st.text_input("Table Name", "dbo.Customers")
        key_column = st.text_input("Key Column", "ID")

        if st.button("Generate CDC", type="primary"):
            cdc_sql = sql_agent.generate_cdc(table_name, key_column)
            st.code(cdc_sql, language="sql")
            st.download_button("Download SQL", cdc_sql, file_name="cdc_setup.sql")

    elif sub_tab == "🔍 Reconcile Data":
        col1, col2 = st.columns(2)
        with col1:
            source_query = st.text_area("Source Query", placeholder="SELECT * FROM SourceTable", height=150)
        with col2:
            target_query = st.text_area("Target Query", placeholder="SELECT * FROM TargetTable", height=150)
        key_cols = st.text_input("Key Columns (comma-separated)", "ID")

        if st.button("Generate Reconciliation", type="primary"):
            if source_query and target_query:
                key_columns = [c.strip() for c in key_cols.split(",")]
                reconcile_sql = sql_agent.reconcile_data(source_query, target_query, key_columns)
                st.code(reconcile_sql, language="sql")
                st.download_button("Download SQL", reconcile_sql, file_name="reconciliation.sql")
