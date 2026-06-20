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
from ui.sidebar import is_dark_mode

# Setup logging
logger = setup_logging()

# Page config
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

def inject_theme():
    """Inject dark or light theme CSS based on session state."""
    dark = is_dark_mode()

    if dark:
        # ── NIGHT (dark) theme ──────────────────────────────────────
        APP_BG        = "#0a0d16"
        SIDEBAR_BG    = "#0d0f1b"
        INPUT_BG      = "#131628"
        CARD_BG       = "rgba(19,22,40,0.6)"
        TEXT_PRIMARY  = "#f3f4f6"
        TEXT_SECONDARY= "#94a3b8"
        TEXT_MUTED    = "#64748b"
        BORDER        = "rgba(255,255,255,0.07)"
        ACCENT        = "#38bdf8"
        ACCENT2       = "#6366f1"
        HEADER_GRAD   = "linear-gradient(to right, #38bdf8, #818cf8, #c084fc)"
        METRIC_BG     = "linear-gradient(135deg, #1e1b4b 0%, #311042 100%)"
        METRIC_BORDER = "rgba(139, 92, 246, 0.2)"
        CODE_BG       = "rgba(13,15,27,0.8)"
        CODE_COLOR    = "#a5f3fc"
        EXPANDER_BG   = "rgba(19,22,40,0.6)"
        SUCCESS_BG    = "rgba(16,185,129,0.12)"
        ERROR_BG      = "rgba(239,68,68,0.12)"
        WARNING_BG    = "rgba(245,158,11,0.12)"
        INFO_BG       = "rgba(56,189,248,0.10)"
        SCROLLBAR     = "rgba(99,102,241,0.4)"
        TOGGLE_BORDER = "rgba(255,255,255,0.12)"
    else:
        # ── DAY (light) theme ───────────────────────────────────────
        APP_BG        = "#f0f4f8"
        SIDEBAR_BG    = "#e8edf4"
        INPUT_BG      = "#ffffff"
        CARD_BG       = "rgba(255,255,255,0.85)"
        TEXT_PRIMARY  = "#1e293b"
        TEXT_SECONDARY= "#475569"
        TEXT_MUTED    = "#94a3b8"
        BORDER        = "rgba(0,0,0,0.08)"
        ACCENT        = "#0284c7"
        ACCENT2       = "#4f46e5"
        HEADER_GRAD   = "linear-gradient(to right, #0284c7, #4f46e5, #7c3aed)"
        METRIC_BG     = "linear-gradient(135deg, #dbeafe 0%, #ede9fe 100%)"
        METRIC_BORDER = "rgba(99,102,241,0.2)"
        CODE_BG       = "rgba(241,245,249,0.9)"
        CODE_COLOR     = "#0f172a"
        EXPANDER_BG   = "rgba(241,245,249,0.9)"
        SUCCESS_BG    = "rgba(16,185,129,0.08)"
        ERROR_BG      = "rgba(239,68,68,0.08)"
        WARNING_BG    = "rgba(245,158,11,0.08)"
        INFO_BG       = "rgba(2,132,199,0.08)"
        SCROLLBAR     = "rgba(99,102,241,0.3)"
        TOGGLE_BORDER = "rgba(0,0,0,0.12)"

    st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    html, body, [data-testid="stAppViewContainer"], .stApp {{
        background-color: {APP_BG} !important;
        color: {TEXT_PRIMARY} !important;
        font-family: 'Inter', sans-serif !important;
    }}
    [data-testid="stHeader"], [data-testid="stToolbar"] {{
        background-color: {APP_BG} !important;
    }}
    /* ── Sidebar ── */
    [data-testid="stSidebar"] {{
        background-color: {SIDEBAR_BG} !important;
        border-right: 1px solid {BORDER} !important;
    }}
    [data-testid="stSidebar"] * {{ color: {TEXT_PRIMARY} !important; }}
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stCaption {{ color: {TEXT_SECONDARY} !important; }}
    [data-testid="stSidebar"] [data-baseweb="select"] > div {{
        background-color: {INPUT_BG} !important;
        border-color: {BORDER} !important;
        color: {TEXT_PRIMARY} !important;
    }}
    [data-testid="stSidebar"] .streamlit-expanderHeader {{
        background-color: {EXPANDER_BG} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 8px !important;
        color: {TEXT_SECONDARY} !important;
    }}
    /* ── Main text ── */
    .stMarkdown, .stText, p, li, label {{ color: {TEXT_PRIMARY} !important; }}
    h1, h2, h3, h4, h5, h6 {{ color: {TEXT_PRIMARY} !important; }}
    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: {CARD_BG};
        padding: 6px; border-radius: 12px;
        border: 1px solid {BORDER}; gap: 8px;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 42px; border-radius: 8px;
        color: {TEXT_SECONDARY} !important;
        font-weight: 600; border: none !important;
        background-color: transparent;
    }}
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {ACCENT} 0%, {ACCENT2} 100%) !important;
        color: white !important;
        box-shadow: 0 4px 14px rgba(99,102,241,0.3);
    }}
    /* ── Custom cards ── */
    .metric-card {{
        background: {METRIC_BG};
        padding: 20px; border-radius: 14px;
        border: 1px solid {METRIC_BORDER};
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    }}
    .agent-card {{
        background: {CARD_BG};
        backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
        border: 1px solid {BORDER}; border-radius: 14px;
        padding: 18px; margin: 12px 0;
        transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }}
    .agent-card:hover {{
        border-color: {ACCENT}; transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(56,189,248,0.15);
    }}
    .agent-card h3 {{ color: {ACCENT}; font-family: 'Outfit', sans-serif; }}
    .agent-card p   {{ color: {TEXT_SECONDARY}; }}
    .agent-card small {{ color: {TEXT_MUTED}; }}
    /* ── Headers ── */
    .main-header {{
        font-size: 2.8rem; font-weight: 900;
        font-family: 'Outfit', sans-serif;
        background: {HEADER_GRAD};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem; letter-spacing: -0.04em;
    }}
    .sub-header {{
        font-size: 1.1rem; color: {TEXT_SECONDARY};
        margin-bottom: 2.2rem; font-weight: 400;
    }}
    /* ── Inputs ── */
    input, textarea {{
        background-color: {INPUT_BG} !important;
        color: {TEXT_PRIMARY} !important;
        border-color: {TOGGLE_BORDER} !important;
    }}
    input::placeholder, textarea::placeholder {{ color: {TEXT_MUTED} !important; }}
    [data-baseweb="base-input"] {{
        background-color: {INPUT_BG} !important;
        border-color: {TOGGLE_BORDER} !important;
    }}
    [data-baseweb="base-input"]:focus-within {{
        border-color: {ACCENT} !important;
        box-shadow: 0 0 0 2px rgba(56,189,248,0.2) !important;
    }}
    /* ── Dropdowns & Select Popover (portal layer) ── */
    div[data-baseweb="select"] > div {{
        background-color: {INPUT_BG} !important;
        border-color: {TOGGLE_BORDER} !important;
        color: {TEXT_PRIMARY} !important;
    }}
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {{
        color: {TEXT_PRIMARY} !important;
        background-color: transparent;
    }}
    /* Portal layer — rendered at body root, outside stApp */
    body > div[data-baseweb="layer"],
    body > div[data-baseweb="layer"] * {{
        background-color: {INPUT_BG} !important;
        color: {TEXT_PRIMARY} !important;
    }}
    [data-baseweb="popover"] {{
        background-color: {INPUT_BG} !important;
        border: 1px solid {BORDER} !important;
        box-shadow: 0 8px 30px rgba(0,0,0,0.35) !important;
    }}
    [data-baseweb="menu"] {{
        background-color: {INPUT_BG} !important;
        border: 1px solid {BORDER} !important;
    }}
    [data-baseweb="option"] {{
        background-color: {INPUT_BG} !important;
        color: {TEXT_PRIMARY} !important;
        padding: 10px 14px !important;
    }}
    [data-baseweb="option"]:hover {{
        background-color: rgba(56,189,248,0.15) !important;
        color: {ACCENT} !important;
        cursor: pointer !important;
    }}
    [aria-selected="true"][data-baseweb="option"] {{
        background-color: rgba(99,102,241,0.18) !important;
        color: {ACCENT} !important;
        font-weight: 600 !important;
    }}
    /* Cover all list items inside the popover */
    ul[data-baseweb="menu"] li {{
        background-color: {INPUT_BG} !important;
        color: {TEXT_PRIMARY} !important;
    }}
    ul[data-baseweb="menu"] li:hover {{
        background-color: rgba(56,189,248,0.12) !important;
        color: {ACCENT} !important;
    }}
    /* ── Metric widgets ── */
    [data-testid="stMetricValue"] {{ color: {ACCENT} !important; font-weight: 700 !important; }}
    [data-testid="stMetricLabel"] {{ color: {TEXT_SECONDARY} !important; }}
    [data-testid="metric-container"] {{
        background: {CARD_BG} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 12px !important; padding: 16px !important;
    }}
    /* ── Radio / Checkbox ── */
    [data-testid="stRadio"] label, [data-testid="stCheckbox"] label {{
        color: {TEXT_SECONDARY} !important;
    }}
    /* ── Alerts ── */
    [data-testid="stAlert"] {{ background-color: {CARD_BG} !important; border-radius: 10px !important; }}
    .stSuccess {{ background-color: {SUCCESS_BG} !important; }}
    .stError   {{ background-color: {ERROR_BG}   !important; }}
    .stWarning {{ background-color: {WARNING_BG} !important; }}
    .stInfo    {{ background-color: {INFO_BG}    !important; }}
    /* ── Buttons ── */
    div.stButton > button {{
        background: linear-gradient(135deg, {ACCENT} 0%, {ACCENT2} 100%) !important;
        color: white !important; border: none !important;
        padding: 8px 20px !important; border-radius: 8px !important;
        font-weight: 600 !important; transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(56,189,248,0.15) !important;
    }}
    div.stButton > button:hover {{
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 16px rgba(56,189,248,0.3) !important;
        opacity: 0.92 !important;
    }}
    /* ── Expanders ── */
    .streamlit-expanderHeader {{
        background-color: {EXPANDER_BG} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 8px !important; color: {TEXT_SECONDARY} !important;
    }}
    /* ── Code ── */
    code, pre {{
        background-color: {CODE_BG} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 8px !important; color: {CODE_COLOR} !important;
    }}
    /* ── Chat ── */
    [data-testid="stChatMessage"] {{
        background-color: {CARD_BG} !important;
        border: 1px solid {BORDER} !important; border-radius: 12px !important;
    }}
    [data-testid="stChatInputContainer"] {{
        background-color: {SIDEBAR_BG} !important;
        border-top: 1px solid {BORDER} !important;
    }}
    [data-testid="stChatInput"] textarea {{
        background-color: {INPUT_BG} !important;
        color: {TEXT_PRIMARY} !important;
    }}
    /* ── Misc ── */
    hr {{ border-color: {BORDER} !important; }}
    [data-testid="stDataFrame"] {{ background-color: {INPUT_BG} !important; }}
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: {APP_BG}; }}
    ::-webkit-scrollbar-thumb {{ background: {SCROLLBAR}; border-radius: 3px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: {ACCENT2}; }}
</style>
""", unsafe_allow_html=True)
def main():
    """Main application entry point."""

    # Header
    inject_theme()
    st.markdown('<div class="main-header">🤖 Data Engineering Copilot</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">AI-Powered Data Engineering Assistant v{VERSION} | Multi-Agent System</div>', unsafe_allow_html=True)

    # Sidebar
    render_sidebar()

    # Module routing
    active_module = st.session_state.get("active_module", "dashboard")

    if active_module == "dashboard":
        render_dashboard_tab()
    elif active_module == "chat":
        render_chat_tab()
    elif active_module == "kb":
        render_kb_tab()
    elif active_module == "sql":
        render_sql_tab()
    elif active_module == "databricks":
        render_databricks_tab()
    elif active_module == "adf":
        render_adf_tab()
    elif active_module == "dataverse":
        render_dataverse_tab()
    elif active_module == "jira":
        render_jira_tab()
    elif active_module == "meeting":
        render_meeting_tab()
    elif active_module == "ppt":
        render_ppt_tab()
    elif active_module == "data_quality":
        render_data_quality_tab()
    elif active_module == "dbt":
        render_dbt_tab()
    elif active_module == "airflow":
        render_airflow_tab()
    elif active_module == "terraform":
        render_terraform_tab()
    elif active_module == "governance":
        render_governance_tab()
    elif active_module == "cost":
        render_cost_tab()
    elif active_module == "migration":
        render_migration_tab()
    elif active_module == "observability":
        render_observability_tab()
    elif active_module == "catalog":
        render_catalog_tab()
    elif active_module == "testing":
        render_testing_tab()
    elif active_module == "code_review":
        render_code_review_tab()
    elif active_module == "streaming":
        render_streaming_tab()
    elif active_module == "mlops":
        render_mlops_tab()


if __name__ == "__main__":
    main()
