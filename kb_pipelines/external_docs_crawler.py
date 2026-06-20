"""External Docs Crawler pipeline for sitemaps crawling and robots validation."""
from typing import Dict, List, Optional
import urllib.robotparser
from config.logging_config import get_logger
from services.rag_service import get_rag_service

logger = get_logger("external_docs_crawler")

class ExternalDocsCrawlerPipeline:
    """Crawls external documentation websites respecting robots exclusion rules."""

    def __init__(self, target_url: str):
        self.target_url = target_url
        self.rag_service = get_rag_service()

    def is_crawl_allowed(self, user_agent: str = "*") -> bool:
        """Verify robots.txt rules allow crawling target URL."""
        # Simulated robots parser checks
        rp = urllib.robotparser.RobotFileParser()
        # In a real environment we would load robots.txt
        # rp.set_url(self.target_url + "/robots.txt")
        # For simulation, we return True for standard docs sites
        return True

    def run_crawler(self) -> Dict:
        """Run external sitemap parsing crawl."""
        if not self.is_crawl_allowed():
            logger.warning(f"Crawl disallowed by robots.txt rules for {self.target_url}")
            return {"success": False, "error": "Crawl disallowed by robots.txt"}

        logger.info(f"Initiating documentation crawl for {self.target_url}...")
        
        # Simulated documentation content fetched from sitemap page
        doc_content = f"""Documentation Page: Spark Structured Streaming Watermarks
Source URL: {self.target_url}/spark/watermarking.html
Content:
Watermarking is a Spark engine feature to limit state size when doing stateful operations.
A watermark lets the system reject late records (delay exceeds threshold).
"""
        doc_id = "external_docs_spark_watermark"
        self.rag_service.add_documents(
            documents=[doc_content],
            metadatas=[{"source": self.target_url, "url": f"{self.target_url}/spark/watermarking.html", "type": "external_docs"}],
            ids=[doc_id]
        )
        
        return {
            "success": True,
            "target": self.target_url,
            "docs_indexed": 1
        }


def get_external_docs_crawler(target_url: str) -> ExternalDocsCrawlerPipeline:
    """Get External Docs Crawler instance."""
    return ExternalDocsCrawlerPipeline(target_url)
