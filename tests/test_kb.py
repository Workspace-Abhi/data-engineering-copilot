"""Unit tests for knowledge base layer (document_manager)."""
import pytest
from unittest.mock import Mock, patch
from knowledge_base.document_manager import DocumentManager

class TestDocumentManager:
    """Test cases for DocumentManager."""

    @patch("knowledge_base.document_manager.parse_uploaded_file")
    @patch("knowledge_base.document_manager.get_rag_service")
    def test_upload_document(self, mock_get_rag, mock_parse_uploaded):
        """Test document uploading and indexing."""
        mock_rag = Mock()
        mock_get_rag.return_value = mock_rag
        
        mock_parse_uploaded.return_value = {
            "text": "This is a document about PySpark.",
            "metadata": {"file_name": "pyspark.md", "type": "md"}
        }

        manager = DocumentManager()
        uploaded_file = Mock()
        
        result = manager.upload_document(uploaded_file)
        
        assert result["success"] is True
        assert result["file_name"] == "pyspark.md"
        assert result["chunks"] > 0
        assert mock_rag.add_documents.called

    @patch("knowledge_base.document_manager.get_rag_service")
    def test_get_stats(self, mock_get_rag):
        """Test document manager stats retrieval."""
        mock_rag = Mock()
        mock_rag.count.return_value = 42
        mock_rag.collection_name = "test_collection"
        mock_get_rag.return_value = mock_rag

        manager = DocumentManager()
        stats = manager.get_stats()

        assert stats["total_documents"] == 42
        assert stats["collection_name"] == "test_collection"
