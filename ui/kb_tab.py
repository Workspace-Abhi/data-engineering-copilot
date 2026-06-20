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
        query = st.text_input("Search Knowledge Base", placeholder="Search for patterns, best practices, examples...")

        if query and st.button("Search", type="primary"):
            with st.spinner("Searching..."):
                results = doc_manager.search_documents(query, k=5)
                if results:
                    for i, result in enumerate(results):
                        with st.expander(f"Result {i+1} | {result['metadata'].get('source', 'Unknown')} | Score: {1-result['distance']:.3f}"):
                            st.text(result["content"][:500] + "...")
                            st.caption(f"Metadata: {result['metadata']}")
                else:
                    st.info("No results found. Try uploading documents first.")

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
