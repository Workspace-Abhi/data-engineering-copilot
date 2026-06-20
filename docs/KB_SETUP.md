# Knowledge Base Setup Guide

This guide details how to index files and leverage the vector search system in Data Engineering Copilot.

## Vector Store
- We use **ChromaDB** as the default persistent vector store.
- On failure (e.g. SQLite version incompatibility on Windows), it automatically falls back to an **InMemoryCollection** saved to pickle.

## Ingestion Flow
1. **Upload File**: Upload file formats (PDF, DOCX, CSV, XLSX, JSON, SQL, PY, YAML, IPYNB, TXT, MD) via the Knowledge Base tab.
2. **Parsing**: Files are parsed using `utils/file_parser.py` text extractors.
3. **Chunking**: Text is split into sentence-boundary-aware chunks or code function chunks using `utils/chunking.py`.
4. **Embedding**: Emits embeddings via the local Ollama API or hash fallback logic.
5. **Search Query**: Searches use hybrid reciprocal rank fusion (RRF) combining ChromaDB cosine distances with a python TF-IDF keyword scorer.
