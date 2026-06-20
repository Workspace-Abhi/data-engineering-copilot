"""Application configuration and constants."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Application Info
APP_TITLE = "Data Engineering Copilot"
APP_ICON = "🤖"
VERSION = "1.0.0"
AUTHOR = "Data Engineering Team"

# Paths
BASE_DIR = Path(__file__).parent.parent
CHROMA_DIR = BASE_DIR / "chroma_db"
LOGS_DIR = BASE_DIR / "logs"
SAMPLES_DIR = BASE_DIR / "samples"

# Create directories
CHROMA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Ollama Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
OLLAMA_TIMEOUT = 120

# LLM Parameters
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
TOP_P = 0.9

# ChromaDB Configuration
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", str(CHROMA_DIR))
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "data_eng_kb")
CHROMA_SEARCH_K = 5

# Chunking Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
CODE_CHUNK_SIZE = 500
CODE_CHUNK_OVERLAP = 100

# Agent Configuration
AGENTS = {
    "sql": {
        "name": "SQL Agent",
        "icon": "🗃️",
        "description": "SQL validation, reconciliation, CDC, and MERGE operations",
        "keywords": ["sql", "query", "table", "join", "merge", "cdc", "reconciliation", "validation", "schema"]
    },
    "databricks": {
        "name": "Databricks Agent", 
        "icon": "🔥",
        "description": "PySpark, Delta Lake, SCD Type 1/2 implementations",
        "keywords": ["spark", "pyspark", "delta", "databricks", "scd", "slowly changing dimension", "notebook", "cluster"]
    },
    "adf": {
        "name": "ADF Agent",
        "icon": "🔷",
        "description": "Azure Data Factory pipeline design and expressions",
        "keywords": ["adf", "azure data factory", "pipeline", "activity", "copy", "dataflow", "watermark", "expression"]
    },
    "dataverse": {
        "name": "Dataverse Agent",
        "icon": "📊",
        "description": "Microsoft Dataverse entity mapping and ingestion",
        "keywords": ["dataverse", "entity", "field", "column", "mapping", "ingestion", "power platform", "dynamics"]
    },
    "jira": {
        "name": "Jira Agent",
        "icon": "🐛",
        "description": "Issue grouping, workstreams, and remediation planning",
        "keywords": ["jira", "issue", "bug", "ticket", "sprint", "epic", "story", "workstream", "remediation"]
    },
    "meeting": {
        "name": "Meeting Agent",
        "icon": "📝",
        "description": "Transcript analysis and action item extraction",
        "keywords": ["meeting", "transcript", "action item", "minutes", "notes", "discussion", "follow up"]
    },
    "ppt": {
        "name": "PPT Agent",
        "icon": "📑",
        "description": "Executive presentation storylines and structure",
        "keywords": ["ppt", "presentation", "slide", "executive", "storyline", "deck", "powerpoint", "summary"]
    }
}

# Theme Colors
THEME_COLORS = {
    "primary": "#1E88E5",
    "secondary": "#7B1FA2", 
    "success": "#43A047",
    "warning": "#FB8C00",
    "error": "#E53935",
    "info": "#00ACC1"
}

# Supported File Types for Knowledge Base
SUPPORTED_FILE_TYPES = {
    "pdf": [".pdf"],
    "docx": [".docx", ".doc"],
    "excel": [".xlsx", ".xls", ".csv"],
    "code": [".sql", ".py", ".yaml", ".yml", ".json", ".ipynb"],
    "text": [".txt", ".md"]
}

# Logging Configuration
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

# UI Configuration
MAX_CHAT_HISTORY = 50
CHAT_INPUT_PLACEHOLDER = "Ask me about SQL, Databricks, ADF, Dataverse, Jira, meetings, or presentations..."
