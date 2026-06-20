"""Sidebar component with system info, model selector, and settings."""
import streamlit as st
from config.settings import APP_TITLE, VERSION, OLLAMA_MODEL, AGENTS
from config.logging_config import get_logger
from utils.helpers import check_ollama_status, get_system_info
from services.llm_service import get_llm_service

logger = get_logger("sidebar")

def is_dark_mode() -> bool:
    """Return True if the app is in dark (night) mode."""
    return st.session_state.get("dark_mode", True)

def render_sidebar():
    """Render the application sidebar."""
    with st.sidebar:
        dark = st.session_state.get("dark_mode", True)

        # ── Theme-aware sidebar CSS (no portal, all inline) ──────────
        if dark:
            RADIO_ACTIVE_BG  = "rgba(56,189,248,0.15)"
            RADIO_ACTIVE_BD  = "#38bdf8"
            RADIO_ACTIVE_TXT = "#38bdf8"
            RADIO_BG         = "rgba(255,255,255,0.03)"
            RADIO_TXT        = "#cbd5e1"
            RADIO_HOVER      = "rgba(255,255,255,0.06)"
        else:
            RADIO_ACTIVE_BG  = "rgba(2,132,199,0.12)"
            RADIO_ACTIVE_BD  = "#0284c7"
            RADIO_ACTIVE_TXT = "#0284c7"
            RADIO_BG         = "rgba(0,0,0,0.03)"
            RADIO_TXT        = "#334155"
            RADIO_HOVER      = "rgba(0,0,0,0.05)"

        st.markdown(f"""
        <style>
            /* ── Sidebar radio buttons styled as nav items ── */
            [data-testid="stSidebar"] [data-testid="stRadio"] > div {{
                gap: 4px !important;
            }}
            [data-testid="stSidebar"] [data-testid="stRadio"] label {{
                display: flex !important;
                align-items: center !important;
                width: 100% !important;
                padding: 8px 12px !important;
                border-radius: 8px !important;
                border: 1px solid transparent !important;
                cursor: pointer !important;
                font-size: 0.92rem !important;
                font-weight: 500 !important;
                color: {RADIO_TXT} !important;
                background: {RADIO_BG} !important;
                transition: all 0.18s ease !important;
                margin: 1px 0 !important;
            }}
            [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {{
                background: {RADIO_HOVER} !important;
                color: {RADIO_ACTIVE_TXT} !important;
                border-color: {RADIO_ACTIVE_BD} !important;
            }}
            [data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"],
            [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {{
                background: {RADIO_ACTIVE_BG} !important;
                color: {RADIO_ACTIVE_TXT} !important;
                border-color: {RADIO_ACTIVE_BD} !important;
                font-weight: 700 !important;
            }}
            /* Hide the actual radio circle dot */
            [data-testid="stSidebar"] [data-testid="stRadio"] input[type="radio"] {{
                display: none !important;
            }}
            [data-testid="stSidebar"] [data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {{
                font-size: 0.92rem !important;
                color: inherit !important;
                margin: 0 !important;
            }}
        </style>
        """, unsafe_allow_html=True)

        # ── Header + Toggle ──────────────────────────────────────────
        col_title, col_toggle = st.columns([3, 1])
        with col_title:
            st.title(f"⚙️ {APP_TITLE}")
            st.caption(f"v{VERSION}")
        with col_toggle:
            st.write("")
            st.write("")
            label = "🌙" if dark else "☀️"
            if st.button(label, key="theme_toggle_btn", help="Switch Day / Night mode"):
                st.session_state["dark_mode"] = not dark
                st.rerun()
        st.divider()

        # ── Navigation (radio, no portal) ────────────────────────────
        CATEGORIES_MAP = {
            "🏠 Dashboard":                ["\U0001f3e0 Dashboard"],
            "💬 RAG & Chat":               ["💬 Chat", "📚 Knowledge Base"],
            "🛠️ Orchestration & Pipelines": ["🔷 ADF", "🌪️ Airflow", "🔥 Databricks", "🌊 Streaming"],
            "💾 Models & Databases":        ["🗃️ SQL", "🧱 dbt", "📊 Dataverse", "📇 Catalog", "🤖 MLOps"],
            "🛡️ Quality & Governance":     ["⚡ Data Quality", "🛡️ Governance", "💰 Cost",
                                             "👁️ Observability", "🧪 Testing", "🔍 Code Review", "🛠️ Terraform IaC"],
            "👥 Team & Reporting":          ["🐛 Jira", "📝 Meetings", "📑 PPT", "🚢 Migration"],
        }
        categories = list(CATEGORIES_MAP.keys())

        MODULES_KEYS_MAP = {
            "\U0001f3e0 Dashboard": "dashboard",
            "💬 Chat": "chat",       "📚 Knowledge Base": "kb",
            "🔷 ADF": "adf",         "🌪️ Airflow": "airflow",
            "🔥 Databricks": "databricks", "🌊 Streaming": "streaming",
            "🗃️ SQL": "sql",         "🧱 dbt": "dbt",
            "📊 Dataverse": "dataverse",   "📇 Catalog": "catalog",
            "🤖 MLOps": "mlops",
            "⚡ Data Quality": "data_quality", "🛡️ Governance": "governance",
            "💰 Cost": "cost",       "👁️ Observability": "observability",
            "🧪 Testing": "testing", "🔍 Code Review": "code_review",
            "🛠️ Terraform IaC": "terraform",
            "🐛 Jira": "jira",       "📝 Meetings": "meeting",
            "📑 PPT": "ppt",         "🚢 Migration": "migration",
        }

        # Category selection — radio (no dropdown portal)
        st.subheader("📂 Module Category")
        default_cat = st.session_state.get("active_category", categories[0])
        if default_cat not in categories:
            default_cat = categories[0]
        cat_index = categories.index(default_cat)

        active_category = st.radio(
            "Category",
            options=categories,
            index=cat_index,
            label_visibility="collapsed",
            key="workspace_category_select",
        )
        st.session_state["active_category"] = active_category

        # Module selection within category
        module_options = CATEGORIES_MAP[active_category]
        if len(module_options) > 1:
            st.write("")
            st.subheader("🎯 Select Agent/View")
            default_mod = st.session_state.get("active_module_display", module_options[0])
            if default_mod not in module_options:
                default_mod = module_options[0]
            mod_index = module_options.index(default_mod)

            active_module_display = st.radio(
                "Agent/View",
                options=module_options,
                index=mod_index,
                label_visibility="collapsed",
                key="workspace_module_radio",
            )
        else:
            active_module_display = module_options[0]

        st.session_state["active_module_display"] = active_module_display
        st.session_state["active_module"] = MODULES_KEYS_MAP.get(active_module_display, "dashboard")

        st.divider()

        # ── System Status ─────────────────────────────────────────────
        st.subheader("🔌 System Status")
        ollama_status = check_ollama_status()
        is_ollama_running = (ollama_status["status"] == "running")

        if is_ollama_running:
            st.success("✅ Ollama Connected")
            with st.expander("Available Models"):
                for model in ollama_status.get("models", []):
                    st.text(f"• {model}")
        else:
            st.error("❌ Ollama Not Running")
            st.info("Start Ollama: `ollama serve`")

        st.divider()

        # ── Mode Setting ──────────────────────────────────────────────
        st.subheader("⚙️ Mode Setting")
        simulated_mode = st.checkbox(
            "Enable Simulated Mode (Mock LLM)",
            value=not is_ollama_running,
            help="Use high-fidelity local mock engines when Ollama is offline or not installed.",
        )
        st.session_state["simulated_mode"] = simulated_mode
        if simulated_mode:
            st.info("🛠️ Simulated Mode is active.")

        st.divider()

        # ── Model Configuration ───────────────────────────────────────
        st.subheader("🤖 Model Configuration")
        available_models = ollama_status.get("models", [OLLAMA_MODEL])

        # Radio instead of selectbox to avoid portal rendering issue
        selected_model_idx = 0
        if OLLAMA_MODEL in available_models:
            selected_model_idx = available_models.index(OLLAMA_MODEL)

        selected_model = st.radio(
            "LLM Model",
            options=available_models,
            index=selected_model_idx,
            key="model_radio_select",
        )

        temperature = st.slider(
            "Temperature",
            min_value=0.0, max_value=1.0, value=0.7, step=0.1,
            help="Lower = more deterministic, Higher = more creative",
        )
        max_tokens = st.slider(
            "Max Tokens",
            min_value=256, max_value=8192, value=4096, step=256,
        )

        st.divider()

        # ── Agent Overview ────────────────────────────────────────────
        st.subheader("🎯 Available Agents")
        for agent_key, agent_config in AGENTS.items():
            with st.expander(f"{agent_config['icon']} {agent_config['name']}"):
                st.write(agent_config["description"])
                st.caption(f"Keywords: {', '.join(agent_config['keywords'][:5])}...")

        st.divider()

        # ── System Info ───────────────────────────────────────────────
        with st.expander("ℹ️ System Info"):
            sys_info = get_system_info()
            for key, value in sys_info.items():
                st.text(f"{key}: {value}")

        # ── Session Controls ──────────────────────────────────────────
        st.divider()
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            from services.conversation_memory import get_memory
            memory = get_memory()
            memory.clear()
            st.success("Chat history cleared!")
            st.rerun()

        # Store settings in session state
        st.session_state["model_config"] = {
            "model": selected_model,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
