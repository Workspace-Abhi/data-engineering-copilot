"""Jira analysis interface tab."""
import pandas as pd
import streamlit as st
from config.logging_config import get_logger
from agents.jira_agent import get_jira_agent

logger = get_logger("jira_tab")

def get_sample_backlog():
    import io
    csv_data = """Issue Key,Summary,Description,Story Points,Theme,Status,Priority
DE-101,SCD Type 2 expiry logic bug,PySpark script fails to close old records correctly during merge when alternate keys are present,5,SCD2 Migration,In Progress,High
DE-102,Delta table Z-Order clustering optimization,Need to run OPTIMIZE delta table ZORDER BY customer_id to speed up reporting queries,3,Performance,To Do,Medium
DE-103,ADF lookup watermark concurrency failure,Parallel ingestion pipelines hit deadlock on watermarks control table,8,ADF Pipelines,Blocked,High
DE-104,MSAL token authentication credentials expiry,OAuth token expires every hour; need to implement refresh token rotation,3,Authentication,To Do,Medium
DE-105,Dataverse OptionSet choice field mapping,Need custom lookup configuration mapping for customer status choice lists,5,Dataverse Sync,To Do,Low
DE-106,Synapse Serverless SQL query timeout,Serverless database times out when scanning large partition folders,5,Performance,To Do,Medium
DE-107,Jira Agile remediation plan definition,Create structured sprint allocation and remediation plan for key data pipeline blockers,2,Planning,To Do,Low
DE-108,Delta Lake VACUUM transaction log cleanup,VACUUM removes transaction files older than 168 hours causing read inconsistency on concurrent scans,8,Performance,In Progress,High
DE-109,ADF Watermark init setup script,Create initialization scripts for all tables in SQL control db metadata store,3,ADF Pipelines,To Do,Low
DE-110,MSAL authentication Azure Key Vault integration,Fetch client credentials securely from vault instead of environmental plaintext config,5,Authentication,To Do,High
"""
    return pd.read_csv(io.StringIO(csv_data))

def render_jira_tab():
    """Render the Jira analysis interface."""
    st.header("🐛 Jira Agent")
    st.caption("Issue grouping, workstreams, remediation planning")

    jira_agent = get_jira_agent()

    sub_tab = st.radio(
        "Select Operation",
        ["💬 Chat", "📊 Analyze Issues", "📋 Remediation Plan", "🏷️ Group by Theme"],
        horizontal=True,
        key="jira_operation_radio"
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

    else:
        uploaded_file = st.file_uploader("Upload Jira Export (CSV)", type=["csv"], key=f"jira_upload_{sub_tab.replace(' ', '_')}")
        
        df = None
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df.head(), use_container_width=True)
        elif st.session_state.get("sample_backlog") is not None:
            df = st.session_state["sample_backlog"]
            st.info("⚡ Premium Sample Backlog loaded.")
            st.dataframe(df.head(), use_container_width=True)
            if st.button("🗑️ Clear Sample Backlog", key=f"jira_clear_{sub_tab.replace(' ', '_')}"):
                del st.session_state["sample_backlog"]
                st.rerun()
        else:
            if st.button("⚡ Load Premium Sample Backlog (Azure Spark Migration)", key=f"jira_load_sample_{sub_tab.replace(' ', '_')}"):
                st.session_state["sample_backlog"] = get_sample_backlog()
                st.rerun()

        if df is not None:
            if sub_tab == "📊 Analyze Issues":
                if st.button("Analyze Issues", type="primary", key="jira_analyze_btn"):
                    with st.spinner("Analyzing..."):
                        result = jira_agent.analyze_issues(df)
                        st.markdown(result["analysis"])
                        st.metric("Total Issues", result["issue_count"])

            elif sub_tab == "📋 Remediation Plan":
                team_capacity = st.slider("Team Capacity (story points/sprint)", 20, 100, 40)
                if st.button("Generate Plan", type="primary", key="jira_plan_btn"):
                    with st.spinner("Generating plan..."):
                        result = jira_agent.generate_remediation_plan(df, team_capacity)
                        st.markdown(result["plan"])
                        st.info(f"Planned capacity: {result['capacity']} story points per sprint")

            elif sub_tab == "🏷️ Group by Theme":
                if st.button("Group by Theme", type="primary", key="jira_theme_btn"):
                    with st.spinner("Grouping..."):
                        result = jira_agent.group_by_theme(df)
                        if "error" in result:
                            st.error(result["error"])
                        else:
                            st.markdown(result["grouping"])
