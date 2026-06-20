"""Utility helpers for formatting, Ollama checks, and system info."""
import os
import platform
import subprocess
from typing import Dict, List
import streamlit as st
from config.settings import OLLAMA_BASE_URL, VERSION
from config.logging_config import get_logger

logger = get_logger("helpers")

@st.cache_data(ttl=30)   # re-check Ollama every 30 seconds, not on every render
def check_ollama_status() -> Dict:
    """Check if Ollama is running and list available models."""
    try:
        import requests
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = [m["name"] for m in data.get("models", [])]
            return {
                "status": "running",
                "models": models,
                "url": OLLAMA_BASE_URL
            }
        else:
            return {"status": "error", "message": f"Status code: {response.status_code}"}
    except Exception as e:
        return {"status": "not_running", "message": str(e)}

@st.cache_data(ttl=300)  # system info changes very rarely — cache 5 min
def get_system_info() -> Dict:
    """Get system information."""
    return {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "python_version": platform.python_version(),
        "processor": platform.processor(),
        "machine": platform.machine(),
        "app_version": VERSION
    }


def format_code_block(code: str, language: str = "") -> str:
    """Format code for display."""
    return f"```{language}\n{code}\n```"

def format_agent_card(agent_name: str, agent_icon: str, description: str, 
                       keywords: List[str] = None) -> str:
    """Format an agent card for display."""
    keywords_str = ", ".join(keywords) if keywords else ""
    return f"""
    <div class="agent-card">
        <h3>{agent_icon} {agent_name}</h3>
        <p>{description}</p>
        <small><b>Keywords:</b> {keywords_str}</small>
    </div>
    """

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."

def estimate_tokens(text: str) -> int:
    """Roughly estimate token count."""
    # Rough estimate: ~4 characters per token for English
    return len(text) // 4

def create_download_link(data: str, filename: str, mime_type: str = "text/plain") -> str:
    """Create a download link for data."""
    import base64
    b64 = base64.b64encode(data.encode()).decode()
    return f'<a href="data:{mime_type};base64,{b64}" download="{filename}">Download {filename}</a>'

def sanitize_filename(filename: str) -> str:
    """Sanitize a filename."""
    import re
    return re.sub(r'[^\w\-_.]', '_', filename)

def get_file_icon(file_type: str) -> str:
    """Get an emoji icon for a file type."""
    icons = {
        "pdf": "📄",
        "docx": "📝",
        "csv": "📊",
        "excel": "📊",
        "json": "📋",
        "sql": "🗃️",
        "py": "🐍",
        "yaml": "⚙️",
        "notebook": "📓",
        "text": "📄"
    }
    return icons.get(file_type, "📄")
