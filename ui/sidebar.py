"""Sidebar component with system info, model selector, and settings."""
import streamlit as st
from config.settings import APP_TITLE, VERSION, OLLAMA_MODEL, AGENTS
from config.logging_config import get_logger
from utils.helpers import check_ollama_status, get_system_info
from services.llm_service import get_llm_service

logger = get_logger("sidebar")

def render_sidebar():
    """Render the application sidebar."""
    with st.sidebar:
        st.title(f"⚙️ {APP_TITLE}")
        st.caption(f"v{VERSION}")
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
            key="workspace_category_select"
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
                key="workspace_module_radio"
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

        st.divider()

        # Mode Setting
        st.subheader("⚙️ Mode Setting")
        simulated_mode = st.checkbox(
            "Enable Simulated Mode (Mock LLM)",
            value=not is_ollama_running,
            help="Use high-fidelity local mock engines when Ollama is offline or not installed."
        )
        st.session_state["simulated_mode"] = simulated_mode
        if simulated_mode:
            st.info("🛠️ Simulated Mode is active.")

        st.divider()

        # Model Selector
        st.subheader("🤖 Model Configuration")
        available_models = ollama_status.get("models", [OLLAMA_MODEL])
        selected_model = st.selectbox(
            "LLM Model",
            options=available_models,
            index=available_models.index(OLLAMA_MODEL) if OLLAMA_MODEL in available_models else 0
        )

        # Temperature slider
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Lower = more deterministic, Higher = more creative"
        )

        # Max tokens
        max_tokens = st.slider(
            "Max Tokens",
            min_value=256,
            max_value=8192,
            value=4096,
            step=256
        )

        st.divider()

        # Agent Overview
        st.subheader("🎯 Available Agents")
        for agent_key, agent_config in AGENTS.items():
            with st.expander(f"{agent_config['icon']} {agent_config['name']}"):
                st.write(agent_config["description"])
                st.caption(f"Keywords: {', '.join(agent_config['keywords'][:5])}...")

        st.divider()

        # System Info
        with st.expander("ℹ️ System Info"):
            sys_info = get_system_info()
            for key, value in sys_info.items():
                st.text(f"{key}: {value}")

        # Session controls
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
            "max_tokens": max_tokens
        }
