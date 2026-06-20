"""Document management for upload, parse, index, and search."""
from typing import List, Dict, Optional
import os
import uuid
import streamlit as st
from config.logging_config import get_logger
from services.rag_service import get_rag_service
from utils.file_parser import parse_uploaded_file
from utils.chunking import chunk_document

logger = get_logger("document_manager")

class DocumentManager:
    """Manages documents in the knowledge base."""

    def __init__(self):
        self.rag_service = get_rag_service()

    def upload_document(self, uploaded_file) -> Dict:
        """Upload and index a document."""
        try:
            # Parse the file
            parsed = parse_uploaded_file(uploaded_file)
            text = parsed["text"]
            metadata = parsed["metadata"]

            if not text.strip():
                return {"success": False, "error": "No text content found in file"}

            # Chunk the document
            file_type = metadata.get("type", "text")
            chunks = chunk_document(text, file_type)

            # Prepare for indexing
            documents = []
            metadatas = []
            ids = []

            for chunk in chunks:
                doc_id = f"{metadata.get('file_name', 'doc')}_{uuid.uuid4().hex[:8]}_{chunk['index']}"
                documents.append(chunk["text"])
                metadatas.append({
                    **metadata,
                    "chunk_index": chunk["index"],
                    "chunk_type": chunk["type"],
                    "source": metadata.get("file_name", "unknown")
                })
                ids.append(doc_id)

            # Add to vector store
            self.rag_service.add_documents(documents, metadatas, ids)

            return {
                "success": True,
                "document_id": ids[0].split("_")[0] if ids else str(uuid.uuid4()),
                "chunks": len(chunks),
                "file_name": metadata.get("file_name"),
                "type": file_type
            }
        except Exception as e:
            logger.error(f"Document upload failed: {e}")
            return {"success": False, "error": str(e)}

    def search_documents(self, query: str, k: int = 5) -> List[Dict]:
        """Search documents in the knowledge base."""
        return self.rag_service.search(query, k=k)

    def get_all_documents(self) -> List[Dict]:
        """Get all indexed documents."""
        return self.rag_service.get_all_documents()

    def delete_document(self, doc_id: str) -> bool:
        """Delete a document from the knowledge base."""
        try:
            self.rag_service.delete_document(doc_id)
            return True
        except Exception as e:
            logger.error(f"Document deletion failed: {e}")
            return False

    def get_stats(self) -> Dict:
        """Get knowledge base statistics."""
        return {
            "total_documents": self.rag_service.count(),
            "collection_name": self.rag_service.collection_name
        }


def get_document_manager() -> DocumentManager:
    """Get document manager instance."""
    return DocumentManager()
