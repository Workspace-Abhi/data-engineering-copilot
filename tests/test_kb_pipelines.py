"""Unit tests for knowledge base automation pipelines (kb_pipelines)."""
import pytest
from unittest.mock import Mock, patch
from kb_pipelines.confluence_sync import ConfluenceSyncPipeline
from kb_pipelines.github_repo_sync import GitHubRepoSyncPipeline
from kb_pipelines.db_catalog_sync import DbCatalogSyncPipeline
from kb_pipelines.external_docs_crawler import ExternalDocsCrawlerPipeline
from kb_pipelines.incident_postmortem_ingestion import IncidentPostmortemIngestionPipeline
from kb_pipelines.scheduler import PipelineScheduler

class TestConfluenceSync:
    """Test cases for ConfluenceSyncPipeline."""

    def test_clean_html(self):
        """Test HTML cleaning function."""
        pipeline = ConfluenceSyncPipeline("TEST")
        html_input = "<p>Clean <b>HTML</b> &amp; tags</p>"
        assert pipeline.clean_html(html_input) == "Clean HTML & tags"

    @patch("kb_pipelines.confluence_sync.get_rag_service")
    def test_run_sync(self, mock_get_rag):
        """Test confluence synchronizer."""
        mock_rag = Mock()
        mock_get_rag.return_value = mock_rag
        
        pipeline = ConfluenceSyncPipeline("TEST")
        res = pipeline.run_sync()
        assert res["success"] is True
        assert res["pages_synced"] == 2
        assert mock_rag.add_documents.called


class TestGitHubRepoSync:
    """Test cases for GitHubRepoSyncPipeline."""

    def test_parse_python_ast(self):
        """Test AST function extraction."""
        pipeline = GitHubRepoSyncPipeline("my-repo")
        code = "class A:\n  def f(self):\n    pass\n"
        decls = pipeline.parse_python_ast(code)
        assert len(decls) == 2
        assert decls[0]["name"] == "A"
        assert decls[1]["name"] == "f"

    @patch("kb_pipelines.github_repo_sync.get_rag_service")
    def test_handle_webhook_push(self, mock_get_rag):
        """Test repository push webhook indexing."""
        mock_rag = Mock()
        mock_get_rag.return_value = mock_rag
        
        pipeline = GitHubRepoSyncPipeline("my-repo")
        res = pipeline.handle_webhook_push({})
        assert res["success"] is True
        assert res["declarations_found"] == 3
        assert mock_rag.add_documents.called


class TestDbCatalogSync:
    """Test cases for DbCatalogSyncPipeline."""

    @patch("kb_pipelines.db_catalog_sync.get_rag_service")
    def test_sync_catalog(self, mock_get_rag):
        """Test schema catalog synchronization."""
        mock_rag = Mock()
        mock_get_rag.return_value = mock_rag
        
        pipeline = DbCatalogSyncPipeline("prod_db")
        res = pipeline.sync_catalog()
        assert res["success"] is True
        assert res["database"] == "prod_db"
        assert mock_rag.add_documents.called


class TestExternalDocsCrawler:
    """Test cases for ExternalDocsCrawlerPipeline."""

    @patch("kb_pipelines.external_docs_crawler.get_rag_service")
    def test_run_crawler(self, mock_get_rag):
        """Test external document crawler execution."""
        mock_rag = Mock()
        mock_get_rag.return_value = mock_rag
        
        pipeline = ExternalDocsCrawlerPipeline("https://spark.apache.org")
        res = pipeline.run_crawler()
        assert res["success"] is True
        assert res["docs_indexed"] == 1
        assert mock_rag.add_documents.called


class TestIncidentPostmortemIngestion:
    """Test cases for IncidentPostmortemIngestionPipeline."""

    @patch("kb_pipelines.incident_postmortem_ingestion.get_rag_service")
    def test_ingest_pagerduty_postmortem(self, mock_get_rag):
        """Test incident report indexing."""
        mock_rag = Mock()
        mock_get_rag.return_value = mock_rag
        
        pipeline = IncidentPostmortemIngestionPipeline()
        postmortem = {
            "incident_id": "INC-099",
            "title": "Spark OOM on Silver write",
            "root_cause": "BroadCast Join size limit exceeded",
            "resolution": "Set spark.sql.autoBroadcastJoinThreshold to -1"
        }
        res = pipeline.ingest_pagerduty_postmortem(postmortem)
        assert res["success"] is True
        assert res["incident_id"] == "INC-099"
        assert mock_rag.add_documents.called


class TestPipelineScheduler:
    """Test cases for PipelineScheduler."""

    @patch("kb_pipelines.scheduler.json.dump")
    def test_schedule_job(self, mock_json_dump):
        """Test scheduling a job and logging run execution state."""
        scheduler = PipelineScheduler()
        task_mock = Mock(return_value={"success": True})
        
        scheduler.schedule_job("sync_test", "hourly", task_mock)
        assert "sync_test" in scheduler.jobs
        assert scheduler.jobs["sync_test"]["status"] == "Success"
        assert task_mock.called
