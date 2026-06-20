"""Unit tests for services (llm_service and rag_service)."""
import pytest
from unittest.mock import Mock, patch
from services.llm_service import OllamaService
from services.rag_service import RAGService


class TestOllamaService:
    """Test cases for OllamaService."""

    @patch("services.llm_service.OllamaService.embed")
    def test_embed_single(self, mock_embed):
        """Test embed_single returns a single vector."""
        mock_embed.return_value = [[0.1, 0.2, 0.3]]
        service = OllamaService()
        vector = service.embed_single("hello")
        assert vector == [0.1, 0.2, 0.3]
        mock_embed.assert_called_once_with(["hello"])

    @patch("services.llm_service.OllamaService.embed")
    def test_embed_single_empty(self, mock_embed):
        """Test embed_single handles empty result."""
        mock_embed.return_value = []
        service = OllamaService()
        vector = service.embed_single("hello")
        assert vector == []


class TestRAGService:
    """Test cases for RAGService."""

    @patch("services.rag_service.get_llm_service")
    def test_search_calls_embed_single(self, mock_get_llm):
        """Test RAG search obtains a vector query embedding and queries the database."""
        mock_llm = Mock()
        mock_llm.embed_single.return_value = [0.1, 0.2]
        mock_get_llm.return_value = mock_llm

        service = RAGService(persist_dir="dummy_dir", collection_name="dummy_collection")
        service.collection = Mock()
        service.collection.query.return_value = {
            "documents": [["Doc content"]],
            "metadatas": [[{"source": "test"}]],
            "distances": [[0.1]],
            "ids": [["doc_1"]]
        }

        results = service.search("query text", k=2)
        mock_llm.embed_single.assert_called_once_with("query text")
        service.collection.query.assert_called_once_with(
            query_embeddings=[[0.1, 0.2]],
            n_results=2,
            where=None,
            include=["documents", "metadatas", "distances"]
        )
        assert len(results) == 1
        assert results[0]["content"] == "Doc content"
        assert results[0]["metadata"] == {"source": "test"}
        assert results[0]["distance"] == 0.1
