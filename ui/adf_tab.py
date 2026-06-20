"""ADF agent interface tab."""
import json
import streamlit as st
from config.logging_config import get_logger
from agents.adf_agent import get_adf_agent

logger = get_logger("adf_tab")

def render_adf_tab():
    """Render the ADF agent interface."""
    from utils.visualizers import render_data_lineage, render_adf_flow
    
    st.header("🔷 Azure Data Factory Agent")
    st.caption("Pipeline design, expressions, watermark patterns")

    # Render architecture pipeline lineage
    st.markdown(render_data_lineage("ADF"), unsafe_allow_html=True)
    st.divider()

    adf_agent = get_adf_agent()

    sub_tab = st.radio(
        "Select Operation",
        ["💬 Chat", "💧 Watermark Pipeline", "🔣 Expressions", "📋 Copy Activity"],
        horizontal=True,
        key="adf_operation_radio"
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
            source_table = st.text_input("Source Table", "dbo.SourceTable", key="adf_source_t")
            target_table = st.text_input("Target Table", "dbo.TargetTable", key="adf_target_t")
        with col2:
            watermark_col = st.text_input("Watermark Column", "ModifiedDate", key="adf_wm_col")
            source_conn = st.text_input("Source Connection", "SourceDataset", key="adf_src_conn")
            target_conn = st.text_input("Target Connection", "TargetDataset", key="adf_tgt_conn")

        # Render dynamic visual pipeline flowchart live!
        st.divider()
        st.subheader("📊 Dynamic ADF Ingestion Flowchart")
        st.markdown(render_adf_flow(source_table, target_table, watermark_col), unsafe_allow_html=True)
        st.divider()

        if st.button("Generate Pipeline", type="primary", key="adf_pipeline_btn"):
            pipeline = adf_agent.generate_watermark_pipeline(
                source_table, target_table, watermark_col, source_conn, target_conn
            )
            st.json(pipeline)
            st.download_button(
                "Download JSON", 
                json.dumps(pipeline, indent=2), 
                file_name=f"{pipeline['name']}.json",
                key="adf_download_pipeline"
            )

    elif sub_tab == "🔣 Expressions":
        expr_type = st.selectbox(
            "Expression Type",
            ["current_date", "format_date", "pipeline_name", "run_id", 
             "trigger_time", "parameter", "concat", "if_condition", 
             "coalesce", "string_interpolation", "folder_path"],
            key="adf_expr_type"
        )
        expression = adf_agent.generate_expression(expr_type)
        st.code(expression, language="json")
        st.info("Copy this expression into your ADF activity's dynamic content")

    elif sub_tab == "📋 Copy Activity":
        source_type = st.selectbox("Source Type", ["AzureSqlSource", "DelimitedTextSource", "ParquetSource", "JsonSource"], key="adf_source_type")
        sink_type = st.selectbox("Sink Type", ["AzureSqlSink", "DelimitedTextSink", "ParquetSink", "JsonSink"], key="adf_sink_type")

        if st.button("Generate Activity", type="primary", key="adf_activity_btn"):
            activity = adf_agent.generate_copy_activity(
                source_type, sink_type,
                {"query": "SELECT * FROM Table"}, {"tableName": "TargetTable"}
            )
            st.json(activity)

