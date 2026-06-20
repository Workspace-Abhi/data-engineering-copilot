# 🤖 Data Engineering Copilot

AI-powered Data Engineering Assistant with 8 specialized agents, RAG-powered knowledge base, and multi-tab Streamlit interface.

## Features

- **8 Specialized AI Agents**: SQL, Databricks, ADF, Dataverse, Jira, Meeting, PPT, and General Chat
- **RAG-Powered Knowledge Base**: Upload and query your own documents
- **Multi-Agent Routing**: Intelligent query routing to the best specialist
- **Production-Ready Code Generation**: SQL, PySpark, ADF JSON, Power Query M code
- **Session-Based Memory**: Conversation history within each session

## Quick Start

```bash
# Run setup
python setup.py

# Or manually:
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start Ollama
ollama serve

# Launch app
streamlit run app.py
```

## Architecture

```
┌─────────────────────────────────────────┐
│           Streamlit UI (9 tabs)         │
├─────────────────────────────────────────┤
│      Router → 8 Specialized Agents      │
├─────────────────────────────────────────┤
│   LLM Service (Ollama) + RAG (Chroma)  │
├─────────────────────────────────────────┤
│      Knowledge Base (Document Store)   │
└─────────────────────────────────────────┘
```

## Agents

| Agent | Icon | Capabilities |
|-------|------|-------------|
| SQL | 🗃️ | Validation, MERGE, CDC, Reconciliation |
| Databricks | 🔥 | PySpark, Delta Lake, SCD Type 1/2 |
| ADF | 🔷 | Pipeline design, expressions, watermark |
| Dataverse | 📊 | Entity mapping, ingestion, field types |
| Jira | 🐛 | Issue grouping, workstreams, remediation |
| Meeting | 📝 | Transcript analysis, action items |
| PPT | 📑 | Executive storylines, slide structure |

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
CHROMA_PERSIST_DIR=./chroma_db
```

## License

MIT
