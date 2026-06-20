import streamlit as st
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import APP_TITLE, APP_ICON, VERSION, THEME_COLORS
from config.logging_config import setup_logging
from ui.sidebar import render_sidebar
from ui.chat_tab import render_chat_tab
from ui.sql_tab import render_sql_tab
from ui.databricks_tab import render_databricks_tab
from ui.adf_tab import render_adf_tab
from ui.dataverse_tab import render_dataverse_tab
from ui.jira_tab import render_jira_tab
from ui.meeting_tab import render_meeting_tab
from ui.ppt_tab import render_ppt_tab
from ui.kb_tab import render_kb_tab

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
<style>
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    .main-header {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(to right, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        letter-spacing: -0.04em;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-bottom: 2.2rem;
        font-weight: 400;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.6);
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
        background: rgba(15, 23, 42, 0.45);
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
        background: rgba(15, 23, 42, 0.6);
    }
    .agent-card h3 {
        margin-top: 0;
        color: #38bdf8;
        font-size: 1.15rem;
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
</style>
""", unsafe_allow_html=True)

def main():
    """Main application entry point."""

    # Header
    st.markdown('<div class="main-header">🤖 Data Engineering Copilot</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">AI-Powered Data Engineering Assistant v{VERSION} | Multi-Agent System</div>', unsafe_allow_html=True)

    # Sidebar
    render_sidebar()

    # Main tabs
    tab_icons = {
        "💬 Chat": "chat",
        "🗃️ SQL": "sql", 
        "🔥 Databricks": "databricks",
        "🔷 ADF": "adf",
        "📊 Dataverse": "dataverse",
        "🐛 Jira": "jira",
        "📝 Meetings": "meetings",
        "📑 PPT": "ppt",
        "📚 Knowledge Base": "kb"
    }

    tabs = st.tabs(list(tab_icons.keys()))

    with tabs[0]:
        render_chat_tab()
    with tabs[1]:
        render_sql_tab()
    with tabs[2]:
        render_databricks_tab()
    with tabs[3]:
        render_adf_tab()
    with tabs[4]:
        render_dataverse_tab()
    with tabs[5]:
        render_jira_tab()
    with tabs[6]:
        render_meeting_tab()
    with tabs[7]:
        render_ppt_tab()
    with tabs[8]:
        render_kb_tab()

if __name__ == "__main__":
    main()
