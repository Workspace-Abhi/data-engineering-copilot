"""Data catalog agent interface tab."""
import streamlit as st
from agents.data_catalog_agent import get_data_catalog_agent
from utils.helpers import create_download_link

def render_catalog_tab():
    st.header("📇 Data Catalog Agent")
    st.caption("Generate markdown Data Dictionaries and Mermaid Source-to-Target Data Lineage charts")

    catalog_agent = get_data_catalog_agent()

    chat_sub, dict_sub, lineage_sub = st.tabs(["💬 Chat", "📘 Data Dictionary", "📈 Mermaid Data Lineage"])

    with chat_sub:
        query = st.text_area("Ask about metadata cataloging:",
                             placeholder="How can I automate table descriptions ingestion in Unity Catalog?",
                             key="cat_chat_query",
                             height=100)
        if st.button("Submit Query", type="primary", key="cat_chat_submit"):
            if query:
                with st.spinner("Analyzing..."):
                    res = catalog_agent.process(query)
                    st.markdown(res)

    with dict_sub:
        st.subheader("Generate Markdown Data Dictionary")
        table_name = st.text_input("Table Name", value="dim_customers", key="cat_table_name")
        cols_input = st.text_area("Columns Definition (JSON format)",
                                  value='[\n  {"name": "customer_id", "type": "int", "is_key": true, "nullable": false, "description": "Primary key for customers"},\n  {"name": "email_address", "type": "varchar(255)", "is_key": false, "nullable": true, "description": "Primary contact email"}\n]',
                                  key="cat_cols_input",
                                  height=100)
        if st.button("Generate Dictionary", type="primary", key="cat_dict_btn"):
            try:
                import json
                columns = json.loads(cols_input)
                markdown_dict = catalog_agent.generate_data_dictionary(table_name, columns)
                st.markdown(markdown_dict)
                st.markdown(create_download_link(markdown_dict, f"data_dictionary_{table_name}.md", "text/markdown"), unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Failed to generate: {e}")

    with lineage_sub:
        st.subheader("Generate Source-to-Target Lineage Diagram")
        sources_input = st.text_input("Source Tables (comma separated)", value="raw_customers, stg_crm_data, raw_orders", key="cat_sources")
        target_input = st.text_input("Target Table", value="fact_sales", key="cat_target")
        if st.button("Generate Lineage Code", type="primary", key="cat_lineage_btn"):
            sources = [s.strip() for s in sources_input.split(",") if s.strip()]
            mermaid_code = catalog_agent.generate_lineage_definition(sources, target_input)
            
            st.code(mermaid_code, language="mermaid")
            # Render Mermaid using Streamlit markdown container if supported
            st.markdown(f"""
```mermaid
{mermaid_code}
```
""", unsafe_allow_html=True)
            st.markdown(create_download_link(mermaid_code, f"lineage_{target_input}.mermaid", "text/plain"), unsafe_allow_html=True)
