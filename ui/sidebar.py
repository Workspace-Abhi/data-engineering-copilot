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
        # ── Theme Toggle ──────────────────────────────────────────────
        col_title, col_toggle = st.columns([3, 1])
        with col_title:
            st.title(f"⚙️ {APP_TITLE}")
            st.caption(f"v{VERSION}")
        with col_toggle:
            st.write("")
            st.write("")
            dark = st.session_state.get("dark_mode", True)
            label = "🌙" if dark else "☀️"
            if st.button(label, key="theme_toggle_btn", help="Switch Day / Night mode"):
                st.session_state["dark_mode"] = not dark
                st.rerun()
        st.divider()

        # Navigation
        st.subheader("📂 Module Category")
        categories = [
            "🏠 Dashboard",
            "💬 RAG & Chat",
            "🛠️ Orchestration & Pipelines",
            "💾 Models & Databases",
            "🛡️ Quality & Governance",
            "👥 Team & Reporting"
        ]
        
        CATEGORIES_MAP = {
            "🏠 Dashboard": ["🏠 Dashboard"],
            "💬 RAG & Chat": ["💬 Chat", "📚 Knowledge Base"],
            "🛠️ Orchestration & Pipelines": ["🔷 ADF", "🌪️ Airflow", "🔥 Databricks", "🌊 Streaming"],
            "💾 Models & Databases": ["🗃️ SQL", "🧱 dbt", "📊 Dataverse", "📇 Catalog", "🤖 MLOps"],
            "🛡️ Quality & Governance": ["⚡ Data Quality", "🛡️ Governance", "💰 Cost", "👁️ Observability", "🧪 Testing", "🔍 Code Review", "🛠️ Terraform IaC"],
            "👥 Team & Reporting": ["🐛 Jira", "📝 Meetings", "📑 PPT", "🚢 Migration"]
        }
        
        MODULES_KEYS_MAP = {
            "🏠 Dashboard": "dashboard",
            "💬 Chat": "chat",
            "📚 Knowledge Base": "kb",
            
            "🔷 ADF": "adf",
            "🌪️ Airflow": "airflow",
            "🔥 Databricks": "databricks",
            "🌊 Streaming": "streaming",
            
            "🗃️ SQL": "sql",
            "🧱 dbt": "dbt",
            "📊 Dataverse": "dataverse",
            "📇 Catalog": "catalog",
            "🤖 MLOps": "mlops",
            
            "⚡ Data Quality": "data_quality",
            "🛡️ Governance": "governance",
            "💰 Cost": "cost",
            "👁️ Observability": "observability",
            "🧪 Testing": "testing",
            "🔍 Code Review": "code_review",
            "🛠️ Terraform IaC": "terraform",
            
            "🐛 Jira": "jira",
            "📝 Meetings": "meeting",
            "📑 PPT": "ppt",
            "🚢 Migration": "migration"
        }

        # Determine current category from session state
        default_cat = st.session_state.get("active_category", "🏠 Dashboard")
        if default_cat not in categories:
            default_cat = "🏠 Dashboard"
        cat_index = categories.index(default_cat)

        active_category = st.selectbox(
            "Select Workspace Category",
            options=categories,
            index=cat_index,
            label_visibility="collapsed",
            key="_sb_cat_select"   # private key — never set from outside
        )
        st.session_state["active_category"] = active_category

        # Determine current module inside that category
        module_options = CATEGORIES_MAP[active_category]
        
        if len(module_options) > 1:
            st.write("")
            st.subheader("🎯 Select Agent/View")
            default_mod = st.session_state.get("active_module_display", module_options[0])
            if default_mod not in module_options:
                default_mod = module_options[0]
            mod_index = module_options.index(default_mod)
            
            active_module_display = st.radio(
                "Select Agent/View",
                options=module_options,
                index=mod_index,
                label_visibility="collapsed",
                key="_sb_mod_radio"   # private key — never set from outside
            )
        else:
            active_module_display = module_options[0]
            
        st.session_state["active_module_display"] = active_module_display
        st.session_state["active_module"] = MODULES_KEYS_MAP[active_module_display]

        st.divider()

        # System Status
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
            st.info(f"Start Ollama: `ollama serve`")

        # ── AI Provider & Model Configuration ────────────────────────
        st.subheader("🤖 AI Provider")

        from config.providers import PROVIDERS, get_api_key

        # Provider radio
        provider_options  = list(PROVIDERS.keys())
        provider_labels   = [PROVIDERS[p]["name"] for p in provider_options]
        current_provider  = st.session_state.get("ai_provider", "ollama")
        if current_provider not in provider_options:
            current_provider = "ollama"
        prov_idx = provider_options.index(current_provider)

        selected_label = st.radio(
            "Provider",
            options=provider_labels,
            index=prov_idx,
            label_visibility="collapsed",
            key="_sb_provider_radio",
        )
        selected_provider = provider_options[provider_labels.index(selected_label)]
        if selected_provider != st.session_state.get("ai_provider"):
            st.session_state["ai_provider"] = selected_provider
            # Reset model to provider default on switch
            st.session_state["model_config"] = {
                "model": PROVIDERS[selected_provider]["default_model"],
                "temperature": 0.7,
                "max_tokens": 4096,
            }

        prov_cfg = PROVIDERS[selected_provider]
        st.caption(prov_cfg["description"])

        # API Key input (for cloud providers)
        if prov_cfg["requires_key"]:
            env_key = get_api_key(selected_provider)
            key_in_env = bool(env_key)
            if key_in_env:
                st.success(f"🔑 Key loaded from `.env` ({prov_cfg['env_key']})")
                api_key = env_key
            else:
                api_key = st.text_input(
                    f"🔑 {prov_cfg['short']} API Key",
                    value=st.session_state.get(f"api_key_{selected_provider}", ""),
                    type="password",
                    placeholder=f"Enter your {prov_cfg['short']} API key...",
                    key=f"_sb_apikey_{selected_provider}",
                )
            st.session_state[f"api_key_{selected_provider}"] = api_key
        else:
            st.session_state[f"api_key_{selected_provider}"] = ""

        # Model selector — list depends on provider
        if selected_provider == "ollama":
            ollama_status = check_ollama_status()
            available_models = ollama_status.get("models") or ["llama3.2", "mistral", "codellama"]
        else:
            available_models = prov_cfg["models"]

        default_model = prov_cfg["default_model"]
        current_model = st.session_state.get("model_config", {}).get("model", default_model)
        if current_model not in available_models:
            current_model = available_models[0] if available_models else default_model

        selected_model = st.selectbox(
            "Model",
            options=available_models,
            index=available_models.index(current_model) if current_model in available_models else 0,
            key=f"_sb_model_{selected_provider}",
        )

        temperature = st.slider(
            "Temperature",
            min_value=0.0, max_value=1.0,
            value=st.session_state.get("model_config", {}).get("temperature", 0.7),
            step=0.05,
            help="Lower = more deterministic, Higher = more creative",
        )
        max_tokens = st.slider(
            "Max Tokens",
            min_value=256, max_value=8192,
            value=st.session_state.get("model_config", {}).get("max_tokens", 4096),
            step=256,
        )

        # Persist model config
        st.session_state["model_config"] = {
            "model": selected_model,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        st.divider()

        # Mode Setting
        st.subheader("⚙️ Mode Setting")
        simulated_mode = st.checkbox(
            "Enable Simulated Mode (Mock LLM)",
            value=not is_ollama_running if selected_provider == "ollama" else False,
            help="Use high-fidelity local mock engines when Ollama is offline or not installed.",
            key="simulated_mode_checkbox"
        )
        st.session_state["simulated_mode"] = simulated_mode
        if simulated_mode:
            st.info("🛠️ Simulated Mode is active.")

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

