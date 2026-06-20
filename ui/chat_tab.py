"""RAG-powered chat assistant tab."""
import streamlit as st
from config.settings import CHAT_INPUT_PLACEHOLDER, AGENTS
from config.logging_config import get_logger
from services.llm_service import get_llm_service
from services.conversation_memory import get_memory
from services.rag_service import get_rag_service
from agents.router import get_router
from utils.helpers import format_code_block

logger = get_logger("chat_tab")

# Suggested starter prompts
STARTER_PROMPTS = [
    ("🗃️ SQL Optimization",      "How can I optimize a slow-running SQL query with multiple JOINs?"),
    ("🔷 ADF Pipeline",           "Create an ADF pipeline to incrementally copy data from SQL Server to ADLS Gen2."),
    ("🧱 dbt Model",              "Write a dbt incremental model for a transactions table with SCD Type 2 logic."),
    ("🔥 Databricks",             "How do I tune a PySpark job to avoid shuffle bottlenecks?"),
    ("⚡ Data Quality",            "Set up a Great Expectations suite to validate nulls and schema drift."),
    ("🛡️ Data Governance",        "What are best practices for implementing column-level lineage tracking?"),
    ("🌪️ Airflow DAG",            "Generate an Airflow DAG with a sensor, branching, and retries."),
    ("📊 Cost Optimization",      "How can I reduce Databricks compute costs with autoscaling and spot instances?"),
]

def render_chat_tab():
    """Render the chat assistant tab."""
    dark = st.session_state.get("dark_mode", True)

    # Theme palette
    if dark:
        CARD_BG       = "rgba(19,22,40,0.6)"
        CARD_BD       = "rgba(255,255,255,0.07)"
        CARD_HOVER    = "rgba(56,189,248,0.15)"
        CARD_HOVER_BD = "#38bdf8"
        PILL_BG       = "rgba(56,189,248,0.12)"
        PILL_TXT      = "#38bdf8"
        WELCOME_TXT   = "#94a3b8"
        PROMPT_TXT    = "#e2e8f0"
        ICON_GLOW     = "rgba(56,189,248,0.2)"
    else:
        CARD_BG       = "rgba(255,255,255,0.9)"
        CARD_BD       = "rgba(0,0,0,0.08)"
        CARD_HOVER    = "rgba(2,132,199,0.08)"
        CARD_HOVER_BD = "#0284c7"
        PILL_BG       = "rgba(2,132,199,0.1)"
        PILL_TXT      = "#0284c7"
        WELCOME_TXT   = "#475569"
        PROMPT_TXT    = "#1e293b"
        ICON_GLOW     = "rgba(2,132,199,0.15)"

    st.markdown(f"""
    <style>
        .chat-prompt-card {{
            background: {CARD_BG};
            border: 1px solid {CARD_BD};
            border-radius: 12px;
            padding: 14px 16px;
            cursor: pointer;
            transition: all 0.2s ease;
            margin-bottom: 8px;
            display: flex;
            align-items: flex-start;
            gap: 10px;
        }}
        .chat-prompt-card:hover {{
            background: {CARD_HOVER};
            border-color: {CARD_HOVER_BD};
            transform: translateX(3px);
        }}
        .chat-prompt-card .prompt-title {{
            font-weight: 700;
            font-size: 0.88rem;
            color: {PILL_TXT};
            margin-bottom: 3px;
        }}
        .chat-prompt-card .prompt-body {{
            font-size: 0.83rem;
            color: {WELCOME_TXT};
            line-height: 1.4;
        }}
        .welcome-icon {{
            font-size: 3.5rem;
            text-align: center;
            filter: drop-shadow(0 0 20px {ICON_GLOW});
        }}
        .welcome-heading {{
            font-size: 1.6rem;
            font-weight: 800;
            text-align: center;
            color: {PROMPT_TXT};
            margin: 8px 0 6px;
        }}
        .welcome-sub {{
            font-size: 0.95rem;
            color: {WELCOME_TXT};
            text-align: center;
            margin-bottom: 28px;
        }}
        .agent-pill {{
            display: inline-block;
            background: {PILL_BG};
            color: {PILL_TXT};
            border-radius: 999px;
            padding: 3px 10px;
            font-size: 0.78rem;
            font-weight: 600;
            margin: 2px 3px;
        }}
    </style>
    """, unsafe_allow_html=True)

    st.header("💬 RAG-Powered Chat Assistant")
    st.caption("Ask anything about data engineering. The system routes to the best agent and searches your knowledge base.")

    memory = get_memory()
    history = memory.get_history()

    # ── Empty state: rich welcome screen ─────────────────────────────
    if not history:
        st.markdown("""
        <div class="welcome-icon">🤖</div>
        <div class="welcome-heading">How can I help you today?</div>
        <div class="welcome-sub">
            Powered by <b>21 specialized agents</b> · RAG over your knowledge base · Code generation &amp; explanation
        </div>
        """, unsafe_allow_html=True)

        # Agent capability pills
        agent_pills = "".join(
            f"<span class='agent-pill'>{cfg['icon']} {cfg['name']}</span>"
            for cfg in list(AGENTS.values())[:10]
        )
        st.markdown(f"<div style='text-align:center; margin-bottom: 28px;'>{agent_pills} <span class='agent-pill'>+{len(AGENTS)-10} more</span></div>",
                    unsafe_allow_html=True)

        # Suggested prompts — clicking pre-fills the input via session state
        st.markdown("#### 💡 Try a starter prompt")
        cols = st.columns(2)
        for i, (title, prompt_text) in enumerate(STARTER_PROMPTS):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="chat-prompt-card">
                    <div>
                        <div class="prompt-title">{title}</div>
                        <div class="prompt-body">{prompt_text}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Use this →", key=f"starter_{i}", use_container_width=True):
                    st.session_state["_prefill_prompt"] = prompt_text
                    st.rerun()

        st.divider()

    # ── Chat history display ──────────────────────────────────────────
    chat_container = st.container()
    with chat_container:
        for msg in history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                if msg.get("agent"):
                    agent_info = AGENTS.get(msg["agent"])
                    if agent_info:
                        st.caption(f"🤖 Routed to {agent_info['name']}")

    # ── Chat input (with pre-fill support) ───────────────────────────
    prefill = st.session_state.pop("_prefill_prompt", None)
    prompt = st.chat_input(prefill or CHAT_INPUT_PLACEHOLDER)
    if prefill and not prompt:
        prompt = prefill

    if prompt:
        memory.add_message("user", prompt)
        with st.chat_message("user"):
            st.write(prompt)

        router = get_router()
        agent_key, confidence = router.route(prompt)

        rag_service = get_rag_service()
        results = rag_service.search(prompt, k=3)
        context = ""
        if results:
            context_parts = []
            for idx, r in enumerate(results):
                source = r["metadata"].get("source", "Unknown")
                context_parts.append(f"[Document {idx+1} from {source}]\n{r['content']}")
            context = "\n\n".join(context_parts)

        with st.chat_message("assistant"):
            agent_name = AGENTS.get(agent_key, {}).get("name", "AI Agent")
            with st.spinner(f"Consulting {agent_name}..."):
                llm_service = get_llm_service()

                agent_prompts = {
                    "sql":        "You are a SQL expert. Provide SQL code and explanations.",
                    "databricks": "You are a Databricks/PySpark expert. Provide PySpark code and Delta Lake best practices.",
                    "adf":        "You are an Azure Data Factory expert. Provide pipeline JSON and expressions.",
                    "dataverse":  "You are a Microsoft Dataverse expert. Provide schema mappings and integration patterns.",
                    "jira":       "You are an Agile project management expert. Provide structured analysis and plans.",
                    "meeting":    "You are a meeting facilitator. Provide structured analysis and action items.",
                    "ppt":        "You are an executive presentation designer. Provide storyline and slide recommendations.",
                }

                system_prompt = agent_prompts.get(agent_key, "You are a helpful data engineering assistant.")
                full_prompt = f"""Context from knowledge base:\n{context}\n\nUser Question: {prompt}\n\nProvide a comprehensive, accurate response. Include code examples where applicable."""

                response = llm_service.generate(
                    full_prompt,
                    system_prompt=system_prompt,
                    temperature=st.session_state.get("model_config", {}).get("temperature", 0.7),
                    max_tokens=st.session_state.get("model_config", {}).get("max_tokens", 4096),
                )

                st.caption(f"🤖 Routed to **{agent_name}** (Confidence: {confidence:.2f})")

                if results:
                    with st.expander("📚 View Retrieved Reference Sources"):
                        for idx, r in enumerate(results):
                            src = r["metadata"].get("source", "Unknown")
                            c_idx = r["metadata"].get("chunk_index", 0)
                            st.markdown(f"**Source {idx+1}:** {src} (Chunk {c_idx})")
                            st.text(r["content"][:400] + "...")

                def response_generator():
                    import time
                    for word in response.split(" "):
                        yield word + " "
                        time.sleep(0.015)

                st.write_stream(response_generator)

        memory.add_message("assistant", response, agent=agent_key)
        st.rerun()
