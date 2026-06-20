"""Session-based chat memory management."""
from typing import List, Dict, Optional
import streamlit as st
from config.settings import MAX_CHAT_HISTORY
from config.logging_config import get_logger

logger = get_logger("conversation_memory")

class ConversationMemory:
    """Manages conversation history for the current session."""

    def __init__(self, max_history: int = None):
        self.max_history = max_history or MAX_CHAT_HISTORY
        self._init_session_state()

    def _init_session_state(self):
        """Initialize session state for chat history."""
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "agent_context" not in st.session_state:
            st.session_state.agent_context = {}

    def add_message(self, role: str, content: str, agent: str = None):
        """Add a message to the conversation history."""
        message = {
            "role": role,
            "content": content,
            "agent": agent
        }
        st.session_state.chat_history.append(message)

        # Trim history if too long
        if len(st.session_state.chat_history) > self.max_history:
            st.session_state.chat_history = st.session_state.chat_history[-self.max_history:]

    def get_history(self, limit: int = None) -> List[Dict]:
        """Get conversation history."""
        history = st.session_state.chat_history
        if limit:
            return history[-limit:]
        return history

    def get_formatted_history(self, limit: int = 10) -> List[Dict[str, str]]:
        """Get history formatted for LLM messages."""
        history = self.get_history(limit=limit)
        formatted = []
        for msg in history:
            formatted.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        return formatted

    def clear(self):
        """Clear conversation history."""
        st.session_state.chat_history = []
        st.session_state.agent_context = {}
        logger.info("Conversation history cleared")

    def set_agent_context(self, agent: str, context: Dict):
        """Set context for a specific agent."""
        st.session_state.agent_context[agent] = context

    def get_agent_context(self, agent: str) -> Optional[Dict]:
        """Get context for a specific agent."""
        return st.session_state.agent_context.get(agent)

    def get_last_agent(self) -> Optional[str]:
        """Get the last used agent."""
        for msg in reversed(st.session_state.chat_history):
            if msg.get("agent"):
                return msg["agent"]
        return None


def get_memory() -> ConversationMemory:
    """Get conversation memory instance."""
    return ConversationMemory()
