"""Databricks agent interface tab."""
import streamlit as st
from config.logging_config import get_logger
from agents.databricks_agent import get_databricks_agent

logger = get_logger("databricks_tab")

def render_databricks_tab():
    """Render the Databricks agent interface."""
    st.header("🔥 Databricks Agent")
    st.caption("PySpark, Delta Lake, SCD Type 1/2 implementations")

    databricks_agent = get_databricks_agent()

    sub_tab = st.radio(
        "Select Operation",
        ["💬 Chat", "🔄 SCD Type 1", "📊 SCD Type 2", "⚡ Optimize Delta"],
        horizontal=True
    )

    if sub_tab == "💬 Chat":
        query = st.text_area("Ask about Databricks/PySpark:", 
                            placeholder="How do I optimize a Delta table? Write a PySpark job for...", 
                            height=100)
        if st.button("Submit", type="primary", key="databricks_submit"):
            if query:
                with st.spinner("Analyzing..."):
                    response = databricks_agent.process(query)
                    st.markdown(response)

    elif sub_tab == "🔄 SCD Type 1":
        col1, col2 = st.columns(2)
        with col1:
            source_path = st.text_input("Source Path", "/mnt/staging/customers")
            target_path = st.text_input("Target Delta Path", "/mnt/delta/customers")
        with col2:
            key_cols = st.text_input("Key Columns", "customer_id")
            update_cols = st.text_input("Update Columns", "name, email, updated_at")

        if st.button("Generate SCD Type 1", type="primary"):
            key_columns = [c.strip() for c in key_cols.split(",")]
            update_columns = [c.strip() for c in update_cols.split(",")]
            code = databricks_agent.generate_scd_type1("source", "target", key_columns, update_columns)
            st.code(code, language="python")
            st.download_button("Download Notebook", code, file_name="scd_type1.py")

    elif sub_tab == "📊 SCD Type 2":
        col1, col2 = st.columns(2)
        with col1:
            source_path = st.text_input("Source Path", "/mnt/staging/customers")
            target_path = st.text_input("Target Delta Path", "/mnt/delta/customers_hist")
        with col2:
            key_cols = st.text_input("Key Columns", "customer_id")
            track_cols = st.text_input("Tracking Columns", "name, email, status")

        if st.button("Generate SCD Type 2", type="primary"):
            key_columns = [c.strip() for c in key_cols.split(",")]
            tracking_columns = [c.strip() for c in track_cols.split(",")]
            code = databricks_agent.generate_scd_type2("source", "target", key_columns, tracking_columns)
            st.code(code, language="python")
            st.download_button("Download Notebook", code, file_name="scd_type2.py")

    elif sub_tab == "⚡ Optimize Delta":
        table_path = st.text_input("Delta Table Path", "/mnt/delta/customers")
        zorder_cols = st.text_input("ZORDER Columns (optional)", "customer_id, date")

        if st.button("Generate Optimization", type="primary"):
            zorder_columns = [c.strip() for c in zorder_cols.split(",")] if zorder_cols else None
            code = databricks_agent.optimize_delta_table(table_path, zorder_columns)
            st.code(code, language="python")
            st.download_button("Download Notebook", code, file_name="optimize_delta.py")
