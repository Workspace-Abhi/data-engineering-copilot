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

def render_chat_tab():
    """Render the chat assistant tab."""
    st.header("💬 RAG-Powered Chat Assistant")
    st.caption("Ask anything about data engineering. The system will route to the best agent and use your knowledge base.")

    # Initialize memory
    memory = get_memory()

    # Display chat history
    chat_container = st.container()
    with chat_container:
        for msg in memory.get_history():
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                if msg.get("agent"):
                    agent_info = AGENTS.get(msg["agent"])
                    if agent_info:
                        st.caption(f"🤖 Routed to {agent_info['name']}")

    # Chat input
    if prompt := st.chat_input(CHAT_INPUT_PLACEHOLDER):
        # Add user message
        memory.add_message("user", prompt)

        with st.chat_message("user"):
            st.write(prompt)

        # Route to agent
        router = get_router()
        agent_key, confidence = router.route(prompt)

        # Get RAG context
        rag_service = get_rag_service()
        results = rag_service.search(prompt, k=3)
        context = ""
        if results:
            context_parts = []
            for idx, r in enumerate(results):
                source = r["metadata"].get("source", "Unknown")
                context_parts.append(f"[Document {idx+1} from {source}]\n{r['content']}")
            context = "\n\n".join(context_parts)

        # Generate response based on agent
        with st.chat_message("assistant"):
            agent_name = AGENTS.get(agent_key, {}).get("name", "AI Agent")
            with st.spinner(f"Consulting {agent_name}..."):
                llm_service = get_llm_service()

                # Build system prompt based on agent
                agent_prompts = {
                    "sql": "You are a SQL expert. Provide SQL code and explanations.",
                    "databricks": "You are a Databricks/PySpark expert. Provide PySpark code and Delta Lake best practices.",
                    "adf": "You are an Azure Data Factory expert. Provide pipeline JSON and expressions.",
                    "dataverse": "You are a Microsoft Dataverse expert. Provide schema mappings and integration patterns.",
                    "jira": "You are an Agile project management expert. Provide structured analysis and plans.",
                    "meeting": "You are a meeting facilitator. Provide structured analysis and action items.",
                    "ppt": "You are an executive presentation designer. Provide storyline and slide recommendations."
                }

                system_prompt = agent_prompts.get(agent_key, "You are a helpful data engineering assistant.")

                # Build full prompt with context
                full_prompt = f"""Context from knowledge base:
{context}

User Question: {prompt}

Provide a comprehensive, accurate response. Include code examples where applicable."""

                response = llm_service.generate(
                    full_prompt,
                    system_prompt=system_prompt,
                    temperature=st.session_state.get("model_config", {}).get("temperature", 0.7),
                    max_tokens=st.session_state.get("model_config", {}).get("max_tokens", 4096)
                )

                # Show routing badge
                st.caption(f"🤖 Routed to **{agent_name}** (Confidence: {confidence:.2f})")

                # Show sources inside an expander if RAG matched documents
                if results:
                    with st.expander("📚 View Retrieved Reference Sources"):
                        for idx, r in enumerate(results):
                            src = r["metadata"].get("source", "Unknown")
                            c_idx = r["metadata"].get("chunk_index", 0)
                            st.markdown(f"**Source {idx+1}:** {src} (Chunk {c_idx})")
                            st.text(r["content"][:400] + "...")

                # Stream response text
                def response_generator():
                    import time
                    for word in response.split(" "):
                        yield word + " "
                        time.sleep(0.015)
                
                st.write_stream(response_generator)

        # Add assistant message
        memory.add_message("assistant", response, agent=agent_key)

        # Rerun to update display
        st.rerun()
