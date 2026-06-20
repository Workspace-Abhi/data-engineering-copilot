"""ADF agent interface tab."""
import json
import streamlit as st
from config.logging_config import get_logger
from agents.adf_agent import get_adf_agent

logger = get_logger("adf_tab")

def render_adf_tab():
    """Render the ADF agent interface."""
    st.header("🔷 Azure Data Factory Agent")
    st.caption("Pipeline design, expressions, watermark patterns")

    adf_agent = get_adf_agent()

    sub_tab = st.radio(
        "Select Operation",
        ["💬 Chat", "💧 Watermark Pipeline", "🔣 Expressions", "📋 Copy Activity"],
        horizontal=True
    )

    if sub_tab == "💬 Chat":
        query = st.text_area("Ask about ADF:", 
                            placeholder="How do I design a pipeline for incremental loads? What's the best expression for...", 
                            height=100)
        if st.button("Submit", type="primary", key="adf_submit"):
            if query:
                with st.spinner("Analyzing..."):
                    response = adf_agent.process(query)
                    st.markdown(response)

    elif sub_tab == "💧 Watermark Pipeline":
        col1, col2 = st.columns(2)
        with col1:
            source_table = st.text_input("Source Table", "dbo.SourceTable")
            target_table = st.text_input("Target Table", "dbo.TargetTable")
        with col2:
            watermark_col = st.text_input("Watermark Column", "ModifiedDate")
            source_conn = st.text_input("Source Connection", "SourceDataset")
            target_conn = st.text_input("Target Connection", "TargetDataset")

        if st.button("Generate Pipeline", type="primary"):
            pipeline = adf_agent.generate_watermark_pipeline(
                source_table, target_table, watermark_col, source_conn, target_conn
            )
            st.json(pipeline)
            st.download_button(
                "Download JSON", 
                json.dumps(pipeline, indent=2), 
                file_name=f"{pipeline['name']}.json"
            )

    elif sub_tab == "🔣 Expressions":
        expr_type = st.selectbox(
            "Expression Type",
            ["current_date", "format_date", "pipeline_name", "run_id", 
             "trigger_time", "parameter", "concat", "if_condition", 
             "coalesce", "string_interpolation", "folder_path"]
        )
        expression = adf_agent.generate_expression(expr_type)
        st.code(expression, language="json")
        st.info("Copy this expression into your ADF activity's dynamic content")

    elif sub_tab == "📋 Copy Activity":
        source_type = st.selectbox("Source Type", ["AzureSqlSource", "DelimitedTextSource", "ParquetSource", "JsonSource"])
        sink_type = st.selectbox("Sink Type", ["AzureSqlSink", "DelimitedTextSink", "ParquetSink", "JsonSink"])

        if st.button("Generate Activity", type="primary"):
            activity = adf_agent.generate_copy_activity(
                source_type, sink_type,
                {"query": "SELECT * FROM Table"}, {"tableName": "TargetTable"}
            )
            st.json(activity)
