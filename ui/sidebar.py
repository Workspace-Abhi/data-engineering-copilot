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
