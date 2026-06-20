"""SQL agent interface tab."""
import streamlit as st
from config.logging_config import get_logger
from agents.sql_agent import get_sql_agent
from utils.helpers import format_code_block

logger = get_logger("sql_tab")

def render_sql_tab():
    """Render the SQL agent interface."""
    from utils.visualizers import render_data_lineage, render_reconciliation_chart
    
    st.header("🗃️ SQL Agent")
    st.caption("SQL validation, reconciliation, CDC, and MERGE operations")

    # Render architecture pipeline lineage
    st.markdown(render_data_lineage("Source"), unsafe_allow_html=True)
    st.divider()

    sql_agent = get_sql_agent()

    # Sub-tabs for different SQL operations
    sub_tab = st.radio(
        "Select Operation",
        ["💬 Chat", "✅ Validate Query", "🔄 Generate MERGE", "📊 Generate CDC", "🔍 Reconcile Data"],
        horizontal=True,
        key="sql_operation_radio"
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

        if st.button("Validate", type="primary", key="sql_validate_btn"):
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

        if st.button("Generate MERGE", type="primary", key="sql_merge_btn"):
            key_columns = [c.strip() for c in key_cols.split(",")]
            update_columns = [c.strip() for c in update_cols.split(",")]
            merge_sql = sql_agent.generate_merge(source_table, target_table, key_columns, update_columns)
            st.code(merge_sql, language="sql")
            st.download_button("Download SQL", merge_sql, file_name="merge_statement.sql", key="sql_download_merge")

    elif sub_tab == "📊 Generate CDC":
        table_name = st.text_input("Table Name", "dbo.Customers")
        key_column = st.text_input("Key Column", "ID")

        if st.button("Generate CDC", type="primary", key="sql_cdc_btn"):
            cdc_sql = sql_agent.generate_cdc(table_name, key_column)
            st.code(cdc_sql, language="sql")
            st.download_button("Download SQL", cdc_sql, file_name="cdc_setup.sql", key="sql_download_cdc")

    elif sub_tab == "🔍 Reconcile Data":
        col1, col2 = st.columns(2)
        with col1:
            source_query = st.text_area("Source Query", "SELECT * FROM staging.Customers", height=120, key="rec_source_q")
        with col2:
            target_query = st.text_area("Target Query", "SELECT * FROM dbo.Customers", height=120, key="rec_target_q")
        
        st.markdown('<div style="background-color: rgba(255, 255, 255, 0.02); padding: 15px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 15px;">', unsafe_allow_html=True)
        st.write("📊 **Interactive Reconciliation Metrics (Live Chart Simulator)**")
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        with metric_col1:
            source_rows = st.number_input("Source Row Count", min_value=0, max_value=1000000, value=15000, step=500, key="rec_src_rows")
        with metric_col2:
            target_rows = st.number_input("Target Row Count", min_value=0, max_value=1000000, value=14850, step=500, key="rec_tgt_rows")
        with metric_col3:
            missing_in_target = st.number_input("Missing in Target", min_value=0, max_value=100000, value=150, step=10, key="rec_miss_tgt")
        with metric_col4:
            missing_in_source = st.number_input("Missing in Source", min_value=0, max_value=100000, value=0, step=10, key="rec_miss_src")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Render visual comparison chart live!
        svg_chart = render_reconciliation_chart(source=source_rows, target=target_rows, missing_t=missing_in_target, missing_s=missing_in_source)
        st.markdown(svg_chart, unsafe_allow_html=True)
        
        key_cols = st.text_input("Key Columns (comma-separated)", "CustomerID", key="rec_key_cols")

        if st.button("Generate Reconciliation SQL", type="primary", key="sql_reconcile_btn"):
            if source_query and target_query:
                key_columns = [c.strip() for c in key_cols.split(",")]
                reconcile_sql = sql_agent.reconcile_data(source_query, target_query, key_columns)
                st.code(reconcile_sql, language="sql")
                st.download_button("Download SQL", reconcile_sql, file_name="reconciliation.sql", key="sql_download_reconcile")
