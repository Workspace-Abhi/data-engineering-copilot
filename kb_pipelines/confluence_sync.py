"""Confluence Sync pipeline for ingestion of confluence pages into the knowledge base."""
import html
from typing import Dict, List, Optional
from config.logging_config import get_logger
from services.rag_service import get_rag_service

logger = get_logger("confluence_sync")

class ConfluenceSyncPipeline:
    """Synchronizes Confluence spaces with the RAG vector database."""

    def __init__(self, space_key: str):
        self.space_key = space_key
        self.rag_service = get_rag_service()

    def clean_html(self, html_content: str) -> str:
        """Strip HTML tags for indexable clean text."""
        import re
        clean = re.compile('<.*?>')
        text = re.sub(clean, '', html_content)
        return html.unescape(text).strip()

    def run_sync(self) -> Dict:
        """Simulate Confluence space crawl and parsing sync."""
        logger.info(f"Starting Confluence sync for space {self.space_key}...")
        
        # Simulated confluence pages crawled
        mock_pages = [
            {
                "id": "conf_101",
                "title": "Data Lake Naming Conventions",
                "body": "<p>All raw files must land in <b>raw-landing/</b> and silver delta tables must reside in <b>processed-silver/</b>.</p>"
            },
            {
                "id": "conf_102",
                "title": "OAuth Authorization Flow Guide",
                "body": "<p>Ensure client credentials are fetched from <i>Azure Key Vault</i> secret references.</p>"
            }
        ]

        synced_count = 0
        for page in mock_pages:
            cleaned_text = f"Title: {page['title']}\nContent: {self.clean_html(page['body'])}"
            doc_id = f"confluence_{self.space_key}_{page['id']}"
            
            # Add to vector store
            self.rag_service.add_documents(
                documents=[cleaned_text],
                metadatas=[{"source": f"confluence_{page['title']}", "space": self.space_key, "type": "confluence"}],
                ids=[doc_id]
            )
            synced_count += 1
            
        return {
            "success": True,
            "space": self.space_key,
            "pages_synced": synced_count
        }


def get_confluence_sync(space_key: str) -> ConfluenceSyncPipeline:
    """Get Confluence Sync instance."""
    return ConfluenceSyncPipeline(space_key)
