"""Airflow agent interface tab."""
import streamlit as st
from agents.airflow_agent import get_airflow_agent
from utils.helpers import create_download_link

def render_airflow_tab():
    st.header("🌪️ Airflow Agent")
    st.caption("Generate Apache Airflow DAGs, TaskGroups, and File Sensors")

    airflow_agent = get_airflow_agent()

    chat_sub, basic_dag_sub, sensor_dag_sub = st.tabs(["💬 Chat", "📅 Basic DAG", "🛰️ Sensor Ingestion DAG"])

    with chat_sub:
        query = st.text_area("Ask about Apache Airflow scheduling:",
                             placeholder="How can I handle backfills and task retries dynamically?",
                             key="af_chat_query",
                             height=100)
        if st.button("Submit Query", type="primary", key="af_chat_submit"):
            if query:
                with st.spinner("Analyzing..."):
                    res = airflow_agent.process(query)
                    st.markdown(res)

    with basic_dag_sub:
        st.subheader("Generate Basic DAG")
        dag_id = st.text_input("DAG ID", value="basic_elt_pipeline", key="af_dag_id")
        schedule = st.selectbox("Schedule Interval", ["@hourly", "@daily", "@weekly", "*/5 * * * *"], index=1, key="af_schedule")
        tasks_input = st.text_input("Tasks (comma separated flow)", value="extract, transform, load, quality_check", key="af_tasks")
        if st.button("Generate DAG", type="primary", key="af_generate_btn"):
            tasks = [t.strip() for t in tasks_input.split(",") if t.strip()]
            code = airflow_agent.generate_dag(dag_id, schedule, tasks)
            st.code(code, language="python")
            st.markdown(create_download_link(code, f"{dag_id}.py"), unsafe_allow_html=True)

    with sensor_dag_sub:
        st.subheader("Generate Ingestion DAG with FileSensor")
        sensor_dag_id = st.text_input("Sensor DAG ID", value="file_ingest_sensor_pipeline", key="af_sensor_dag_id")
        sensor_id = st.text_input("Sensor Task ID", value="wait_for_landing_csv", key="af_sensor_id")
        if st.button("Generate Sensor DAG", type="primary", key="af_sensor_generate_btn"):
            code = airflow_agent.generate_dag_with_sensor(sensor_dag_id, sensor_id)
            st.code(code, language="python")
            st.markdown(create_download_link(code, f"{sensor_dag_id}.py"), unsafe_allow_html=True)
