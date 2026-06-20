"""Jira analysis interface tab."""
import pandas as pd
import streamlit as st
from config.logging_config import get_logger
from agents.jira_agent import get_jira_agent

logger = get_logger("jira_tab")

def render_jira_tab():
    """Render the Jira analysis interface."""
    st.header("🐛 Jira Agent")
    st.caption("Issue grouping, workstreams, remediation planning")

    jira_agent = get_jira_agent()

    sub_tab = st.radio(
        "Select Operation",
        ["💬 Chat", "📊 Analyze Issues", "📋 Remediation Plan", "🏷️ Group by Theme"],
        horizontal=True
    )

    if sub_tab == "💬 Chat":
        query = st.text_area("Ask about Jira/Agile:", 
                            placeholder="How should I group these issues? What's the best sprint allocation for...", 
                            height=100)
        if st.button("Submit", type="primary", key="jira_submit"):
            if query:
                with st.spinner("Analyzing..."):
                    response = jira_agent.process(query)
                    st.markdown(response)

    elif sub_tab == "📊 Analyze Issues":
        uploaded_file = st.file_uploader("Upload Jira Export (CSV)", type=["csv"])

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df.head(), use_container_width=True)

            if st.button("Analyze Issues", type="primary"):
                with st.spinner("Analyzing..."):
                    result = jira_agent.analyze_issues(df)
                    st.markdown(result["analysis"])
                    st.metric("Total Issues", result["issue_count"])

    elif sub_tab == "📋 Remediation Plan":
        uploaded_file = st.file_uploader("Upload Jira Export (CSV)", type=["csv"])
        team_capacity = st.slider("Team Capacity (story points/sprint)", 20, 100, 40)

        if uploaded_file is not None and st.button("Generate Plan", type="primary"):
            df = pd.read_csv(uploaded_file)
            with st.spinner("Generating plan..."):
                result = jira_agent.generate_remediation_plan(df, team_capacity)
                st.markdown(result["plan"])
                st.info(f"Planned capacity: {result['capacity']} story points per sprint")

    elif sub_tab == "🏷️ Group by Theme":
        uploaded_file = st.file_uploader("Upload Jira Export (CSV)", type=["csv"])

        if uploaded_file is not None and st.button("Group by Theme", type="primary"):
            df = pd.read_csv(uploaded_file)
            with st.spinner("Grouping..."):
                result = jira_agent.group_by_theme(df)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.markdown(result["grouping"])
