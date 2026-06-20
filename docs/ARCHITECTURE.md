# System Architecture

## Overview

The Data Engineering Copilot is a multi-agent AI system built on:
- **Streamlit** for UI
- **Ollama** for local LLM inference
- **ChromaDB** for vector storage
- **LangChain-compatible** architecture

## Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         User                                  │
└──────────────────────┬────────────────────────────────────────┘
                       │
┌──────────────────────▼────────────────────────────────────────┐
│              Streamlit Application (app.py)                   │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐           │
│  │ Sidebar │ │  Chat   │ │  SQL    │ │Databricks│  ...      │
│  │(Config) │ │(Router) │ │(Agent)  │ │ (Agent)  │           │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘           │
└──────────────────────┬────────────────────────────────────────┘
                       │
┌──────────────────────▼────────────────────────────────────────┐
│                    Agent Router                               │
│         (Keyword matching + LLM fallback)                     │
└──────────────────────┬────────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┬──────────────┐
        │              │              │              │
   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
   │  SQL    │   │Databricks│   │  ADF   │   │Dataverse│
   │ Agent   │   │ Agent   │   │ Agent  │   │ Agent  │
   └────┬────┘   └────┬────┘   └────┬────┘   └────┬────┘
        │              │              │              │
        └──────────────┴──────────────┴──────────────┘
                       │
┌──────────────────────▼────────────────────────────────────────┐
│              Services Layer                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│  │ LLM Service │  │ RAG Service │  │ Conversation Memory │   │
│  │  (Ollama)   │  │  (ChromaDB) │  │   (Session State)   │   │
│  └─────────────┘  └─────────────┘  └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

1. **User Query** → Streamlit UI
2. **Router** analyzes intent (keywords + LLM fallback)
3. **Agent** processes with specialized system prompt
4. **RAG Service** retrieves relevant documents from ChromaDB
5. **LLM Service** generates response with augmented context
6. **Memory** stores interaction for context

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Local LLM (Ollama) | Data privacy, no API costs, offline capability |
| ChromaDB | Lightweight, persistent, good Python integration |
| Streamlit | Rapid UI development, native Python |
| Session Memory | Simple, no external database needed |
| File-based KB | Easy backup, version control friendly |

## Extensibility

To add a new agent:
1. Create `agents/new_agent.py` with `process()` method
2. Add keywords to `config/settings.py` AGENTS dict
3. Create `ui/new_tab.py` with Streamlit interface
4. Register in `app.py` tabs and `agents/__init__.py`
