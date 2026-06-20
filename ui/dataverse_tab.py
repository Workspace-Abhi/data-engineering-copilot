"""Dataverse agent interface tab."""
import json
import streamlit as st
from config.logging_config import get_logger
from agents.dataverse_agent import get_dataverse_agent

logger = get_logger("dataverse_tab")

def render_dataverse_tab():
    """Render the Dataverse agent interface."""
    st.header("📊 Dataverse Agent")
    st.caption("Entity mapping, ingestion, field types")

    dataverse_agent = get_dataverse_agent()

    sub_tab = st.radio(
        "Select Operation",
        ["💬 Chat", "🗺️ SQL to Dataverse Mapping", "📥 Ingestion Flow"],
        horizontal=True
    )

    if sub_tab == "💬 Chat":
        query = st.text_area("Ask about Dataverse:", 
                            placeholder="How do I map SQL types to Dataverse? What's the best ingestion pattern for...", 
                            height=100)
        if st.button("Submit", type="primary", key="dataverse_submit"):
            if query:
                with st.spinner("Analyzing..."):
                    response = dataverse_agent.process(query)
                    st.markdown(response)

    elif sub_tab == "🗺️ SQL to Dataverse Mapping":
        st.info("Enter your SQL table schema to generate Dataverse entity mapping")

        table_name = st.text_input("Table Name", "Customers")
        schema_input = st.text_area("SQL Schema (simplified)", 
                                   placeholder="ID INT PRIMARY KEY, Name NVARCHAR(100), Email NVARCHAR(255), CreatedDate DATETIME", 
                                   height=100)

        if st.button("Generate Mapping", type="primary"):
            columns = []
            for col in schema_input.split(","):
                parts = col.strip().split()
                if len(parts) >= 2:
                    columns.append({
                        "name": parts[0],
                        "type": parts[1],
                        "nullable": "NOT" not in col.upper()
                    })

            sql_table = {"name": table_name, "columns": columns}
            mapping = dataverse_agent.map_sql_to_dataverse(sql_table)
            st.json(mapping)

            st.subheader("Field Mapping")
            field_data = []
            for field in mapping.get("fields", []):
                field_data.append({
                    "Dataverse Field": field["name"],
                    "Display Name": field["display_name"],
                    "Data Type": field["data_type"],
                    "Required": field["required"]
                })
            st.dataframe(field_data, use_container_width=True)

    elif sub_tab == "📥 Ingestion Flow":
        source_entity = st.text_input("Source Entity", "dbo.Customers")
        target_entity = st.text_input("Dataverse Entity", "cr234_customers")

        mapping_text = st.text_area("Column Mapping (source=target, one per line)", 
                                   "CustomerID=cr234_customerid\nName=cr234_name\nEmail=cr234_email\nCreatedDate=cr234_createdon")

        if st.button("Generate Flow", type="primary"):
            mapping = {}
            for line in mapping_text.strip().split("\n"):
                if "=" in line:
                    src, tgt = line.strip().split("=", 1)
                    mapping[src] = tgt

            flow = dataverse_agent.generate_ingestion_flow(source_entity, target_entity, mapping)
            st.code(flow, language="python")
            st.download_button("Download M Code", flow, file_name="ingestion_flow.m")
