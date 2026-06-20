import streamlit as st
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config.settings import APP_TITLE, APP_ICON, VERSION, THEME_COLORS
from config.logging_config import setup_logging
from ui import (
    render_sidebar, render_chat_tab, render_sql_tab, render_databricks_tab,
    render_adf_tab, render_dataverse_tab, render_jira_tab, render_meeting_tab,
    render_ppt_tab, render_kb_tab, render_data_quality_tab, render_dbt_tab,
    render_airflow_tab, render_terraform_tab, render_governance_tab,
    render_cost_tab, render_migration_tab, render_observability_tab,
    render_catalog_tab, render_testing_tab, render_code_review_tab,
    render_streaming_tab, render_mlops_tab
)
from ui.dashboard import render_dashboard_tab

# Setup logging
logger = setup_logging()

# Page config
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Dark Glassmorphism Theme
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    .stApp {
        background-color: #0a0d16;
        color: #f3f4f6;
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #0d0f1b !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    .main-header {
        font-size: 2.8rem;
        font-weight: 900;
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(to right, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        letter-spacing: -0.04em;
    }
    .sub-header {
        font-size: 1.1rem;
        font-family: 'Inter', sans-serif;
        color: #94a3b8;
        margin-bottom: 2.2rem;
        font-weight: 400;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(13, 15, 27, 0.6);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 8px;
        color: #94a3b8 !important;
        font-weight: 600;
        padding: 0 16px;
        transition: all 0.2s ease;
        border: none !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.03);
        color: #f3f4f6 !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #38bdf8 0%, #6366f1 100%) !important;
        color: white !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
    }
    .metric-card {
        background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%);
        padding: 20px;
        border-radius: 14px;
        color: white;
        border: 1px solid rgba(139, 92, 246, 0.2);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    }
    .agent-card {
        background: rgba(13, 15, 27, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 14px;
        padding: 18px;
        margin: 12px 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    }
    .agent-card:hover {
        border-color: rgba(56, 189, 248, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 10px 24px rgba(56, 189, 248, 0.15);
        background: rgba(13, 15, 27, 0.6);
    }
    .agent-card h3 {
        margin-top: 0;
        color: #38bdf8;
        font-size: 1.15rem;
        font-family: 'Outfit', sans-serif;
    }
    .agent-card p {
        color: #cbd5e1;
        font-size: 0.9rem;
        margin-bottom: 8px;
    }
    .agent-card small {
        color: #64748b;
    }
    /* Styled buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #38bdf8 0%, #6366f1 100%) !important;
        color: white !important;
        border: none !important;
        padding: 8px 20px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.15) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 16px rgba(56, 189, 248, 0.3) !important;
    }
    /* Glassmorphic elements */
    code, pre {
        background-color: rgba(13, 15, 27, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
    }
    .streamlit-expanderHeader {
        background-color: rgba(13, 15, 27, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] > div {
        background-color: rgba(13, 15, 27, 0.6) !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
    }
    input, textarea {
        background-color: rgba(13, 15, 27, 0.6) !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application entry point."""

    # Header
    st.markdown('<div class="main-header">🤖 Data Engineering Copilot</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">AI-Powered Data Engineering Assistant v{VERSION} | Multi-Agent System</div>', unsafe_allow_html=True)

    # Sidebar
    render_sidebar()

    # Category routing
    active_cat = st.session_state.get("active_category", "🏠 Dashboard")

    if active_cat == "🏠 Dashboard":
        render_dashboard_tab()
    
    elif active_cat == "💬 RAG & Chat":
        tab_names = ["💬 Chat", "📚 Knowledge Base"]
        tabs = st.tabs(tab_names)
        with tabs[0]:
            render_chat_tab()
        with tabs[1]:
            render_kb_tab()
            
    elif active_cat == "🛠️ Orchestration & Pipelines":
        tab_names = ["🔷 ADF", "🌪️ Airflow", "🔥 Databricks", "🌊 Streaming"]
        tabs = st.tabs(tab_names)
        with tabs[0]:
            render_adf_tab()
        with tabs[1]:
            render_airflow_tab()
        with tabs[2]:
            render_databricks_tab()
        with tabs[3]:
            render_streaming_tab()

    elif active_cat == "💾 Models & Databases":
        tab_names = ["🗃️ SQL", "🧱 dbt", "📊 Dataverse", "📇 Catalog", "🤖 MLOps"]
        tabs = st.tabs(tab_names)
        with tabs[0]:
            render_sql_tab()
        with tabs[1]:
            render_dbt_tab()
        with tabs[2]:
            render_dataverse_tab()
        with tabs[3]:
            render_catalog_tab()
        with tabs[4]:
            render_mlops_tab()

    elif active_cat == "🛡️ Quality & Governance":
        tab_names = ["⚡ Data Quality", "🛡️ Governance", "💰 Cost", "👁️ Observability", "🧪 Testing", "🔍 Code Review", "🛠️ Terraform IaC"]
        tabs = st.tabs(tab_names)
        with tabs[0]:
            render_data_quality_tab()
        with tabs[1]:
            render_governance_tab()
        with tabs[2]:
            render_cost_tab()
        with tabs[3]:
            render_observability_tab()
        with tabs[4]:
            render_testing_tab()
        with tabs[5]:
            render_code_review_tab()
        with tabs[6]:
            render_terraform_tab()

    elif active_cat == "👥 Team & Reporting":
        tab_names = ["🐛 Jira", "📝 Meetings", "📑 PPT", "🚢 Migration"]
        tabs = st.tabs(tab_names)
        with tabs[0]:
            render_jira_tab()
        with tabs[1]:
            render_meeting_tab()
        with tabs[2]:
            render_ppt_tab()
        with tabs[3]:
            render_migration_tab()


if __name__ == "__main__":
    main()
