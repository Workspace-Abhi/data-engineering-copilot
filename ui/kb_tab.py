"""Knowledge base management tab."""
import streamlit as st
from config.logging_config import get_logger
from knowledge_base.document_manager import get_document_manager
from utils.helpers import get_file_icon

logger = get_logger("kb_tab")

def render_kb_tab():
    """Render the knowledge base management interface."""
    st.header("📚 Knowledge Base")
    st.caption("Upload, manage, and search your data engineering documents")

    doc_manager = get_document_manager()

    sub_tab = st.radio(
        "Select Operation",
        ["📤 Upload Documents", "🔍 Search", "📋 Browse All", "📊 Statistics"],
        horizontal=True
    )

    if sub_tab == "📤 Upload Documents":
        st.info("Upload documents to enhance the RAG system. Supported: PDF, DOCX, CSV, XLSX, JSON, SQL, PY, YAML, TXT, MD, IPYNB")

        uploaded_files = st.file_uploader(
            "Choose files", 
            type=["pdf", "docx", "csv", "xlsx", "json", "sql", "py", "yaml", "yml", "txt", "md", "ipynb"],
            accept_multiple_files=True
        )

        if uploaded_files:
            progress_bar = st.progress(0)
            for i, uploaded_file in enumerate(uploaded_files):
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    result = doc_manager.upload_document(uploaded_file)
                    if result["success"]:
                        st.success(f"✅ {uploaded_file.name}: {result['chunks']} chunks indexed")
                    else:
                        st.error(f"❌ {uploaded_file.name}: {result['error']}")
                progress_bar.progress((i + 1) / len(uploaded_files))

    elif sub_tab == "🔍 Search":
        # Extract unique sources for filtering
        docs = doc_manager.get_all_documents()
        unique_sources = sorted(list(set([d["metadata"].get("source", "Unknown") for d in docs])))
        
        col1, col2 = st.columns([3, 2])
        with col1:
            query = st.text_input("Search Knowledge Base", placeholder="Search for patterns, best practices, examples...", key="kb_search_input")
        with col2:
            source_filter = st.multiselect("Filter by Source File", unique_sources, key="kb_source_filter")
            
        filter_dict = None
        if source_filter:
            if len(source_filter) == 1:
                filter_dict = {"source": source_filter[0]}
            else:
                filter_dict = {"$or": [{"source": s} for s in source_filter]}

        if query and st.button("Search", type="primary", key="kb_search_btn"):
            with st.spinner("Searching..."):
                results = doc_manager.rag_service.search(query, k=5, filter_dict=filter_dict)
                if results:
                    st.success(f"Found {len(results)} relevant documents matching your query.")
                    for i, result in enumerate(results):
                        source = result["metadata"].get("source", "Unknown")
                        c_index = result["metadata"].get("chunk_index", 0)
                        dist = result.get("distance", 0.5)
                        score = 1.0 - dist
                        
                        # Score color coding
                        if score > 0.8:
                            score_label = f"🟢 High Match ({score:.3f})"
                        elif score > 0.5:
                            score_label = f"🟡 Medium Match ({score:.3f})"
                        else:
                            score_label = f"🔴 Low Match ({score:.3f})"
                        
                        with st.expander(f"📖 Result {i+1} | {source} (Chunk {c_index}) | {score_label}"):
                            st.progress(max(0.0, min(1.0, float(score))))
                            
                            child_text = result.get("child_text")
                            if child_text:
                                c1, c2 = st.columns(2)
                                with c1:
                                    st.markdown("🔑 **Semantic Child Match** (High-precision vector hit)")
                                    st.markdown(f'<div style="background-color:rgba(56,189,248,0.05); border-left: 3px solid #38bdf8; padding:12px; border-radius:4px; font-size:0.9rem; color:#e2e8f0; max-height:220px; overflow-y:auto; font-family:monospace;">{child_text}</div>', unsafe_allow_html=True)
                                with c2:
                                    st.markdown("📚 **Expanded Parent Document Context** (Returned to LLM)")
                                    st.markdown(f'<div style="background-color:rgba(16,185,129,0.05); border-left: 3px solid #10b981; padding:12px; border-radius:4px; font-size:0.9rem; color:#e2e8f0; max-height:220px; overflow-y:auto;">{result["content"]}</div>', unsafe_allow_html=True)
                            else:
                                st.markdown("### Document Content")
                                st.markdown(result["content"])
                            
                            st.divider()
                            st.markdown("⚙️ **Metadata Properties**")
                            st.json(result["metadata"])
                else:
                    st.info("No matching results found. Adjust your keywords or search query filters.")

    elif sub_tab == "📋 Browse All":
        documents = doc_manager.get_all_documents()
        if documents:
            st.write(f"Total documents: {len(documents)}")

            sources = {}
            for doc in documents:
                source = doc["metadata"].get("source", "Unknown")
                if source not in sources:
                    sources[source] = []
                sources[source].append(doc)

            for source, docs in sources.items():
                with st.expander(f"{get_file_icon(docs[0]['metadata'].get('type', 'text'))} {source} ({len(docs)} chunks)"):
                    for doc in docs[:3]:
                        st.text(doc["content"][:200] + "...")
                    if len(docs) > 3:
                        st.caption(f"... and {len(docs) - 3} more chunks")
        else:
            st.info("No documents in knowledge base yet.")

    elif sub_tab == "📊 Statistics":
        stats = doc_manager.get_stats()
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Documents", stats["total_documents"])
        col2.metric("Collection", stats["collection_name"])
        col3.metric("Status", "Active")

        st.divider()
        st.subheader("Supported File Types")
        file_types = {
            "📄 PDF": "Research papers, architecture docs",
            "📝 DOCX": "Requirements, specifications",
            "📊 CSV/Excel": "Data samples, mappings",
            "🗃️ SQL": "Query templates, schemas",
            "🐍 Python": "PySpark, utility scripts",
            "⚙️ YAML": "Pipeline configs, definitions",
            "📓 Notebook": "Jupyter notebooks",
            "📄 Text/Markdown": "Documentation, notes"
        }
        for icon_desc, usage in file_types.items():
            st.text(f"{icon_desc}: {usage}")
