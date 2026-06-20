"""Configuration module."""
from config.settings import (
    APP_TITLE, VERSION, OLLAMA_BASE_URL, OLLAMA_MODEL,
    CHROMA_COLLECTION_NAME, AGENTS
)
from config.logging_config import setup_logging, get_logger

__all__ = [
    "APP_TITLE", "VERSION", "OLLAMA_BASE_URL", "OLLAMA_MODEL",
    "CHROMA_COLLECTION_NAME", "AGENTS", "setup_logging", "get_logger"
]
