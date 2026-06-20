"""Streaming agent interface tab."""
import streamlit as st
from agents.streaming_agent import get_streaming_agent
from utils.helpers import create_download_link

def render_streaming_tab():
    st.header("🌊 Streaming Agent")
    st.caption("Generate Spark Structured Streaming window aggregations and Apache Flink DDL/SQL queries")

    stream_agent = get_streaming_agent()

    chat_sub, spark_sub, flink_sub = st.tabs(["💬 Chat", "🔥 Spark Structured Streaming", "⚡ Apache Flink SQL"])

    with chat_sub:
        query = st.text_area("Ask about real-time streaming architectures:",
                             placeholder="How can I join a high-throughput event stream with a slow-changing Dimension table?",
                             key="str_chat_query",
                             height=100)
        if st.button("Submit Query", type="primary", key="str_chat_submit"):
            if query:
                with st.spinner("Analyzing..."):
                    res = stream_agent.process(query)
                    st.markdown(res)

    with spark_sub:
        st.subheader("Generate Spark Window Aggregation")
        topic = st.text_input("Kafka Subscription Topic", value="iot_sensor_events", key="str_sp_topic")
        window_size = st.text_input("Window Duration", value="10 minutes", key="str_sp_window")
        slide_size = st.text_input("Slide Duration", value="5 minutes", key="str_sp_slide")
        if st.button("Generate Spark Streaming Code", type="primary", key="str_sp_btn"):
            code = stream_agent.generate_spark_streaming_window(topic, window_size, slide_size)
            st.code(code, language="python")
            st.markdown(create_download_link(code, "spark_streaming_window.py"), unsafe_allow_html=True)

    with flink_sub:
        st.subheader("Generate Apache Flink DDL & SQL Query")
        if st.button("Generate Flink Setup", type="primary", key="str_flink_btn"):
            ddl_sql = stream_agent.generate_flink_sql_window()
            st.code(ddl_sql, language="sql")
            st.markdown(create_download_link(ddl_sql, "flink_window_query.sql", "text/sql"), unsafe_allow_html=True)
