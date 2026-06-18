# 🤖 Data Engineering Copilot

A complete, production-ready, fully local and free AI application for Data Engineers.

**100% Offline** | **100% Free** | **100% Open Source**

## Features

- **Chat Assistant** with RAG (Retrieval-Augmented Generation)
- **SQL Agent** - Validation, Reconciliation, CDC, MERGE queries
- **Databricks Agent** - PySpark, Delta Lake, SCD patterns
- **ADF Agent** - Pipeline design, dynamic expressions, watermark logic
- **Dataverse Agent** - Entity mapping, ingestion logic, validation
- **Jira Agent** - Issue analysis, workstreams, remediation planning
- **Meeting Notes Agent** - Transcript summarization, action items
- **PPT Story Agent** - Executive presentation storylines
- **Knowledge Base** - Document upload, indexing, semantic search

## Technology Stack

- Python 3.9+
- Streamlit
- Ollama (Local LLM)
- ChromaDB (Vector Database)
- Pandas / OpenPyXL
- Sentence Transformers (via Ollama embeddings)

## Prerequisites

1. **Install Ollama**: https://ollama.com
2. **Pull required models**:
   ```bash
   ollama pull qwen3:8b
   ollama pull nomic-embed-text
   ollama pull llama3.1:8b  # fallback
