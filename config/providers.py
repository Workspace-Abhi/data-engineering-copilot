"""AI provider metadata and configuration."""
import os

# Provider definitions
PROVIDERS = {
    "ollama": {
        "name": "🏠 Ollama (Local)",
        "short": "Ollama",
        "env_key": None,
        "models": [],          # populated dynamically from Ollama API
        "default_model": "llama3.2",
        "requires_key": False,
        "description": "Local models via Ollama — free, private, no internet needed.",
    },
    "openai": {
        "name": "🤖 OpenAI (GPT)",
        "short": "OpenAI",
        "env_key": "OPENAI_API_KEY",
        "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
        "default_model": "gpt-4o",
        "requires_key": True,
        "description": "OpenAI GPT-4o and GPT-3.5 — best general-purpose reasoning.",
    },
    "gemini": {
        "name": "💎 Google Gemini",
        "short": "Gemini",
        "env_key": "GOOGLE_API_KEY",
        "models": ["gemini-2.0-flash", "gemini-2.5-flash"],
        "default_model": "gemini-2.0-flash",
        "requires_key": True,
        "description": "Google Gemini — great for long context and multimodal tasks.",
    },
    "anthropic": {
        "name": "🧠 Anthropic (Claude)",
        "short": "Claude",
        "env_key": "ANTHROPIC_API_KEY",
        "models": ["claude-3-5-sonnet-20241022", "claude-3-haiku-20240307", "claude-3-opus-20240229"],
        "default_model": "claude-3-5-sonnet-20241022",
        "requires_key": True,
        "description": "Anthropic Claude — excellent for code, analysis, and safety.",
    },
}

PROVIDER_LIST = list(PROVIDERS.keys())

def get_api_key(provider_key: str) -> str:
    """Get API key from env, returns empty string if not set."""
    env_var = PROVIDERS[provider_key].get("env_key")
    if env_var:
        return os.getenv(env_var, "")
    return ""
