"""dbt agent interface tab."""
import streamlit as st
from agents.dbt_agent import get_dbt_agent
from utils.helpers import create_download_link

def render_dbt_tab():
    st.header("🧱 dbt Agent")
    st.caption("Generate dbt models, schema tests, snapshots, and macros")

    dbt_agent = get_dbt_agent()

    chat_sub, model_sub, snap_macro_sub = st.tabs(["💬 Chat", "📐 Model & Tests", "📸 Snapshots & Macros"])

    with chat_sub:
        query = st.text_area("Ask about dbt patterns:",
                             placeholder="How can I refactor my sql to dbt incremental models?",
                             key="dbt_chat_query",
                             height=100)
        if st.button("Submit Query", type="primary", key="dbt_chat_submit"):
            if query:
                with st.spinner("Analyzing..."):
                    res = dbt_agent.process(query)
                    st.markdown(res)

    with model_sub:
        st.subheader("Generate Model & schema.yml")
        model_name = st.text_input("Model Name", value="stg_users", key="dbt_model_name")
        src_table = st.text_input("Source Table", value="raw_users", key="dbt_src_table")
        cols_input = st.text_area("Columns (comma separated list)", value="id, email, created_at, status", key="dbt_cols_input")
        
        if st.button("Generate dbt Model", type="primary", key="dbt_model_btn"):
            try:
                columns = [c.strip() for c in cols_input.split(",") if c.strip()]
                model_sql = dbt_agent.generate_model(model_name, src_table, columns)
                st.code(model_sql, language="sql")
                dl_link = create_download_link(model_sql, f"{model_name}.sql", "text/sql")
                st.markdown(dl_link, unsafe_allow_html=True)
                
                # Mock metadata dicts for schema.yml tests
                cols_meta = [{"name": c, "nullable": c == "email", "unique": c == "id"} for c in columns]
                yml_code = dbt_agent.generate_schema_yml(model_name, cols_meta)
                st.code(yml_code, language="yaml")
                dl_link_yml = create_download_link(yml_code, "schema.yml", "text/yaml")
                st.markdown(dl_link_yml, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Failed to generate: {e}")

    with snap_macro_sub:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Generate Snapshot")
            snap_name = st.text_input("Snapshot Name", value="users_snapshot", key="dbt_snap_name")
            target_schema = st.text_input("Target Schema", value="snapshots", key="dbt_snap_schema")
            unique_key = st.text_input("Unique Key", value="id", key="dbt_snap_key")
            updated_at = st.text_input("Updated At Column", value="updated_at", key="dbt_snap_updated")
            if st.button("Generate Snapshot", type="primary", key="dbt_snap_btn"):
                snap_sql = dbt_agent.generate_snapshot(snap_name, target_schema, unique_key, updated_at)
                st.code(snap_sql, language="sql")
                st.markdown(create_download_link(snap_sql, f"{snap_name}.sql"), unsafe_allow_html=True)
        with col2:
            st.subheader("Generate Macro")
            macro_name = st.text_input("Macro Name", value="fill_null_string", key="dbt_macro_name")
            column_name = st.text_input("Column Name parameter", value="status", key="dbt_macro_col")
            if st.button("Generate Macro", type="primary", key="dbt_macro_btn"):
                macro_code = dbt_agent.generate_macro(macro_name, column_name)
                st.code(macro_code, language="jinja")
                st.markdown(create_download_link(macro_code, f"{macro_name}.sql"), unsafe_allow_html=True)
