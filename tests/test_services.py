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

    @patch("services.llm_service.requests.post")
    def test_embed_invalid_response_fallback(self, mock_post):
        """Test embed falls back to hash-based vector when response is None or invalid."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"embedding": None}
        mock_post.return_value = mock_response
        
        service = OllamaService()
        # Force non-simulated mode for testing the requests block
        with patch.object(service, "_is_simulated", return_value=False):
            embeddings = service.embed(["hello"])
            assert len(embeddings) == 1
            assert len(embeddings[0]) == 384  # Falls back to hash-based vector size 384


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
        service.count = Mock(return_value=10)
        service.collection.get.return_value = {"ids": [], "documents": [], "metadatas": []}
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
            n_results=4,
            where=None,
            include=["documents", "metadatas", "distances"]
        )
        assert len(results) == 1
        assert results[0]["content"] == "Doc content"
        assert results[0]["metadata"] == {"source": "test"}
        assert results[0]["distance"] == 0.1

    def test_keyword_search_tf_idf(self):
        """Test simple TF-IDF keyword search returns documents containing matching keywords."""
        service = RAGService(persist_dir="dummy_dir", collection_name="dummy_collection")
        documents = [
            {"id": "doc1", "content": "PySpark SCD Type 2 dimension merge optimization", "metadata": {}},
            {"id": "doc2", "content": "Azure Data Factory watermark copy pipelines", "metadata": {}},
            {"id": "doc3", "content": "SQL Server database CDC change data capture", "metadata": {}}
        ]
        
        # Searching for "SCD" should hit doc1
        results = service._keyword_search("SCD Type 2", documents, k=2)
        assert len(results) >= 1
        assert results[0]["id"] == "doc1"
        
        # Searching for "watermark" should hit doc2
        results_adf = service._keyword_search("watermark", documents, k=2)
        assert len(results_adf) >= 1
        assert results_adf[0]["id"] == "doc2"

    def test_reciprocal_rank_fusion(self):
        """Test RRF ranks documents correctly based on their ranks in both vector and keyword results."""
        service = RAGService(persist_dir="dummy_dir", collection_name="dummy_collection")
        
        vector_res = [
            {"id": "doc_a", "content": "Content A", "metadata": {}},
            {"id": "doc_b", "content": "Content B", "metadata": {}}
        ]
        keyword_res = [
            {"id": "doc_b", "content": "Content B", "metadata": {}},
            {"id": "doc_c", "content": "Content C", "metadata": {}}
        ]
        
        # doc_b is present in both at high ranks, so it should fuse to rank 1
        merged = service._reciprocal_rank_fusion(vector_res, keyword_res, k=3)
        assert len(merged) == 3
        assert merged[0]["id"] == "doc_b"


class TestChunkingParentChild:
    """Test cases for Parent-Child chunking."""

    def test_chunk_document_parent_child(self):
        """Test that chunk_document generates child chunks referencing the parent text."""
        from utils.chunking import chunk_document
        
        doc_text = "This is a long document about data engineering. " * 30  # ~1500 chars
        chunks = chunk_document(doc_text, "text")
        
        assert len(chunks) > 0
        for chunk in chunks:
            assert "text" in chunk
            assert "parent_text" in chunk
            assert "parent_index" in chunk
            assert "This is a long document" in chunk["parent_text"]

