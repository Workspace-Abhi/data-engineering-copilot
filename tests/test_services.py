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


class TestCodeExecutionEngine:
    """Test cases for CodeExecutionEngine."""

    def test_execute_sql(self):
        """Test safe SQL execution against SQLite in-memory DB."""
        from services.code_execution_engine import CodeExecutionEngine
        sql = "CREATE TABLE test (id INT); INSERT INTO test VALUES (1); SELECT * FROM test;"
        res = CodeExecutionEngine.execute_sql(sql)
        assert res["success"] is True
        assert res["columns"] == ["id"]
        assert res["rows"] == [(1,)]

    def test_execute_python_safe(self):
        """Test sandbox Python execution."""
        from services.code_execution_engine import CodeExecutionEngine
        code = "a = 5\nb = 10\nprint(a + b)"
        res = CodeExecutionEngine.execute_python(code)
        assert res["success"] is True
        assert "15" in res["output"]
        assert res["variables"]["a"] == "5"


class TestGitIntegration:
    """Test cases for GitIntegration."""

    def test_create_branch_simulation(self):
        """Test fallback git branch creation simulation."""
        from services.git_integration import GitIntegrationService
        service = GitIntegrationService()
        res = service.create_branch("feature/test-branch")
        assert res["success"] is True

    def test_commit_changes_simulation(self):
        """Test fallback git commit changes simulation."""
        from services.git_integration import GitIntegrationService
        service = GitIntegrationService()
        res = service.commit_changes("feat: testing commits")
        assert res["success"] is True


class TestDbIntrospector:
    """Test cases for DbIntrospector."""

    def test_introspect_schema(self):
        """Test schema extraction mapping."""
        from services.db_introspector import DbIntrospectorService
        service = DbIntrospectorService()
        res = service.introspect_schema("connection_uri", "snowflake", "customers")
        assert res["success"] is True
        assert res["table_name"] == "customers"
        assert len(res["columns"]) > 0


class TestPipelineProfiler:
    """Test cases for PipelineProfiler."""

    def test_profile_explain_plan_spark(self):
        """Test Spark explain plan parsing for Cartesian Product."""
        from services.pipeline_profiler import PipelineProfilerService
        service = PipelineProfilerService()
        res = service.profile_explain_plan("CartesianProduct join in query execution plan", "spark")
        assert res["has_bottlenecks"] is True
        assert "Cartesian Product" in res["bottlenecks"][0]


class TestMultiModalService:
    """Test cases for MultiModalService."""

    def test_parse_diagram_image(self):
        """Test diagram image parsing converts to Mermaid schema."""
        from services.multi_modal_service import MultiModalService
        service = MultiModalService()
        res = service.parse_diagram_image(b"fake_image_bytes", "er_diagram.png")
        assert "erDiagram" in res


class TestKnowledgeGraph:
    """Test cases for KnowledgeGraphService."""

    def test_find_downstream_dependencies(self):
        """Test dependency tracking traversal."""
        from services.knowledge_graph import KnowledgeGraphService
        graph = KnowledgeGraphService()
        
        # In preseeded graph: raw_customers -> stg_customers -> dim_customers -> fact_sales
        impacted = graph.find_downstream_dependencies("raw_customers")
        assert "stg_customers" in impacted
        assert "dim_customers" in impacted
        assert "fact_sales" in impacted
        assert "raw_customers" not in impacted

    def test_query_relationships(self):
        """Test finding immediate node relationships."""
        from services.knowledge_graph import KnowledgeGraphService
        graph = KnowledgeGraphService()
        rels = graph.query_relationships("stg_customers")
        assert len(rels) >= 2


class TestHybridSearch:
    """Test cases for HybridSearchService."""

    @patch("services.hybrid_search.get_rag_service")
    def test_search_injects_graph_metadata(self, mock_get_rag):
        """Test that hybrid search adds lineage impact details into metadata."""
        mock_rag = Mock()
        mock_rag.search.return_value = [
            {"id": "doc1", "content": "Referencing raw_customers schema", "metadata": {}}
        ]
        mock_get_rag.return_value = mock_rag

        from services.hybrid_search import HybridSearchService
        service = HybridSearchService()
        results = service.search("query")
        
        assert len(results) == 1
        assert "graph_lineage_impact" in results[0]["metadata"]
        assert results[0]["metadata"]["graph_lineage_impact"][0]["entity"] == "raw_customers"


class TestUnifiedLLMService:
    """Test cases for UnifiedLLMService."""

    @patch("services.llm_service.OllamaService.generate")
    def test_ollama_route(self, mock_ollama_gen):
        from services.llm_service import UnifiedLLMService
        mock_ollama_gen.return_value = "Ollama response"
        service = UnifiedLLMService(provider="ollama", model="llama3.2")
        res = service.generate("hello")
        assert res == "Ollama response"
        mock_ollama_gen.assert_called_once_with(
            "hello", system_prompt=None, temperature=0.7, max_tokens=4096
        )

    @patch("openai.resources.chat.completions.Completions.create")
    def test_openai_route(self, mock_openai_create):
        from services.llm_service import UnifiedLLMService
        mock_openai_create.return_value = Mock(choices=[Mock(message=Mock(content="OpenAI response"))])
        service = UnifiedLLMService(provider="openai", model="gpt-4o", api_key="sk-test")
        res = service.generate("hello")
        assert res == "OpenAI response"

    @patch("google.generativeai.GenerativeModel.generate_content")
    def test_gemini_route(self, mock_gemini_gen):
        from services.llm_service import UnifiedLLMService
        mock_gemini_gen.return_value = Mock(text="Gemini response")
        service = UnifiedLLMService(provider="gemini", model="gemini-2.0-flash", api_key="ai-key")
        res = service.generate("hello")
        assert res == "Gemini response"

    @patch("anthropic.resources.messages.Messages.create")
    def test_anthropic_route(self, mock_anthropic_create):
        from services.llm_service import UnifiedLLMService
        mock_anthropic_create.return_value = Mock(content=[Mock(text="Anthropic response")])
        service = UnifiedLLMService(provider="anthropic", model="claude-3-5-sonnet-20241022", api_key="an-key")
        res = service.generate("hello")
        assert res == "Anthropic response"

    @patch("services.llm_service.OllamaService._simulated_generate")
    def test_fallback_on_failure(self, mock_sim):
        from services.llm_service import UnifiedLLMService
        mock_sim.return_value = "Simulated response"
        # Trigger an exception during OpenAI generate to check fallback
        with patch("openai.resources.chat.completions.Completions.create", side_effect=Exception("API Error")):
            service = UnifiedLLMService(provider="openai", model="gpt-4o", api_key="sk-key")
            res = service.generate("hello")
            assert "Simulated response" in res
            assert "[!WARNING]" in res
            assert "openai" in res



