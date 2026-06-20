"""Knowledge Base Automation Pipelines module."""
from kb_pipelines.confluence_sync import ConfluenceSyncPipeline, get_confluence_sync
from kb_pipelines.github_repo_sync import GitHubRepoSyncPipeline, get_github_sync
from kb_pipelines.db_catalog_sync import DbCatalogSyncPipeline, get_db_catalog_sync
from kb_pipelines.external_docs_crawler import ExternalDocsCrawlerPipeline, get_external_docs_crawler
from kb_pipelines.incident_postmortem_ingestion import IncidentPostmortemIngestionPipeline, get_incident_ingestion
from kb_pipelines.scheduler import PipelineScheduler, get_scheduler

__all__ = [
    "ConfluenceSyncPipeline", "get_confluence_sync",
    "GitHubRepoSyncPipeline", "get_github_sync",
    "DbCatalogSyncPipeline", "get_db_catalog_sync",
    "ExternalDocsCrawlerPipeline", "get_external_docs_crawler",
    "IncidentPostmortemIngestionPipeline", "get_incident_ingestion",
    "PipelineScheduler", "get_scheduler"
]
