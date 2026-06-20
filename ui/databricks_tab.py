"""Databricks agent interface tab."""
import streamlit as st
from config.logging_config import get_logger
from agents.databricks_agent import get_databricks_agent

logger = get_logger("databricks_tab")

def render_databricks_tab():
    """Render the Databricks agent interface."""
    from utils.visualizers import render_data_lineage
    
    st.header("🔥 Databricks Agent")
    st.caption("PySpark, Delta Lake, SCD Type 1/2 implementations")

    # Interactive Stage Explorer
    selected_stage = st.selectbox(
        "🗺️ Interactive Pipeline Stage Explorer", 
        ["Source", "ADF", "Bronze", "Silver", "Gold"], 
        index=3, 
        key="lineage_stage_explorer"
    )

    # Render architecture pipeline lineage
    st.markdown(render_data_lineage(selected_stage), unsafe_allow_html=True)

    stage_details = {
        "Source": {
            "title": "🔌 Ingestion Source (SQL Server / ADLS Gen2)",
            "format": "Relational Tables / JSON / CSV / Parquet",
            "schema": "Raw untrusted schemas direct from transactional systems.",
            "ops": "Ingested via ADF Watermark pipelines or Spark Auto Loader.",
            "spark": "# Read from raw sources\ndf = spark.read.format('parquet').load('/mnt/raw/source_data')"
        },
        "ADF": {
            "title": "🔷 Orchestrator (Azure Data Factory)",
            "format": "JSON Metadata Configured Pipeline",
            "schema": "Configures and runs Copy Activities and lookup watermarks.",
            "ops": "Runs incremental loads and handles pipeline scheduling.",
            "spark": "# Pipeline defined in JSON, orchestrating Copy Activity\n# Checks watermark in Control Table and pulls increments"
        },
        "Bronze": {
            "title": "🟫 Bronze Stage (Raw Delta Landing)",
            "format": "Delta Lake (Append-Only)",
            "schema": "Preserves original source fields + ingestion metadata columns.",
            "ops": "Appends new runs with load date tracking. No structural updates.",
            "spark": "# Append incoming data directly to Bronze\ndf_incoming.write.format('delta').mode('append').save('/mnt/delta/bronze')"
        },
        "Silver": {
            "title": "🥈 Silver Stage (Enriched History & SCD Type 2)",
            "format": "Delta Lake (ACID Transactions enabled)",
            "schema": "Cleaned, null-coerced schemas with effective dates and current indicators.",
            "ops": "Executes Slowly Changing Dimension (SCD Type 1 & 2) merges.",
            "spark": "# Perform Silver SCD Type 2 merge to update history\ntargetTable.alias('t').merge(sourceDF.alias('s'), 't.id = s.id').whenMatchedUpdate(...)"
        },
        "Gold": {
            "title": "🥇 Gold Stage (Business Aggregations & Target Ingestion)",
            "format": "Delta Lake / Synapse Serverless / Dataverse",
            "schema": "Business-level star schemas, facts, and dimension summaries.",
            "ops": "Applies optimization (Z-Order clustering, compaction, vacuuming). Reads alternate keys.",
            "spark": "# Optimize delta storage files for quick BI queries\nspark.sql('OPTIMIZE delta.`/mnt/delta/gold` ZORDER BY (customer_id)')"
        }
    }

    details = stage_details[selected_stage]
    st.markdown(f"""
    <div style="background: rgba(15, 23, 42, 0.45); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 12px; padding: 18px; margin-top: 15px; margin-bottom: 15px;">
        <h4 style="color:#38bdf8; margin-top:0;">{details['title']}</h4>
        <p style="margin: 4px 0;"><b>Data Format:</b> <code>{details['format']}</code></p>
        <p style="margin: 4px 0;"><b>Purpose & Schema:</b> {details['schema']}</p>
        <p style="margin: 4px 0;"><b>Common Operations:</b> {details['ops']}</p>
    </div>
    """, unsafe_allow_html=True)
    with st.expander("📝 View Stage Code Snippet"):
        st.code(details['spark'], language="python")

    st.divider()

    databricks_agent = get_databricks_agent()

    sub_tab = st.radio(
        "Select Operation",
        ["💬 Chat", "🔄 SCD Type 1", "📊 SCD Type 2", "⚡ Optimize Delta"],
        horizontal=True,
        key="databricks_operation_radio"
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

        if st.button("Generate SCD Type 1", type="primary", key="databricks_scd1_btn"):
            key_columns = [c.strip() for c in key_cols.split(",")]
            update_columns = [c.strip() for c in update_cols.split(",")]
            code = databricks_agent.generate_scd_type1("source", "target", key_columns, update_columns)
            st.code(code, language="python")
            st.download_button("Download Notebook", code, file_name="scd_type1.py", key="databricks_download_scd1")

    elif sub_tab == "📊 SCD Type 2":
        col1, col2 = st.columns(2)
        with col1:
            source_path = st.text_input("Source Path", "/mnt/staging/customers")
            target_path = st.text_input("Target Delta Path", "/mnt/delta/customers_hist")
        with col2:
            key_cols = st.text_input("Key Columns", "customer_id")
            track_cols = st.text_input("Tracking Columns", "name, email, status")

        if st.button("Generate SCD Type 2", type="primary", key="databricks_scd2_btn"):
            key_columns = [c.strip() for c in key_cols.split(",")]
            tracking_columns = [c.strip() for c in track_cols.split(",")]
            code = databricks_agent.generate_scd_type2("source", "target", key_columns, tracking_columns)
            st.code(code, language="python")
            st.download_button("Download Notebook", code, file_name="scd_type2.py", key="databricks_download_scd2")

    elif sub_tab == "⚡ Optimize Delta":
        table_path = st.text_input("Delta Table Path", "/mnt/delta/customers")
        zorder_cols = st.text_input("ZORDER Columns (optional)", "customer_id, date")

        if st.button("Generate Optimization", type="primary", key="databricks_optimize_btn"):
            zorder_columns = [c.strip() for c in zorder_cols.split(",")] if zorder_cols else None
            code = databricks_agent.optimize_delta_table(table_path, zorder_columns)
            st.code(code, language="python")
            st.download_button("Download Notebook", code, file_name="optimize_delta.py", key="databricks_download_optimize")

