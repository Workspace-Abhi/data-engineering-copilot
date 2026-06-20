"""Incident Postmortem Ingestion pipeline for tracking PagerDuty / OpsGenie incidents."""
from typing import Dict, List, Optional
from config.logging_config import get_logger
from services.rag_service import get_rag_service

logger = get_logger("incident_postmortem_ingestion")

class IncidentPostmortemIngestionPipeline:
    """Ingests postmortem incident reports for quick retrieval during pipeline outages."""

    def __init__(self):
        self.rag_service = get_rag_service()

    def ingest_pagerduty_postmortem(self, postmortem: Dict) -> Dict:
        """Parse PagerDuty incidents and index postmortem recommendations."""
        incident_id = postmortem.get("incident_id", "")
        title = postmortem.get("title", "")
        root_cause = postmortem.get("root_cause", "")
        resolution = postmortem.get("resolution", "")
        
        logger.info(f"Ingesting incident {incident_id}: {title}...")
        
        indexed_text = f"""Incident Report: {title}
ID: {incident_id}
Root Cause: {root_cause}
Resolution / Fix Action: {resolution}
"""
        doc_id = f"incident_{incident_id}"
        self.rag_service.add_documents(
            documents=[indexed_text],
            metadatas=[{"source": f"incident_{incident_id}", "incident_id": incident_id, "type": "incident_postmortem"}],
            ids=[doc_id]
        )
        
        return {
            "success": True,
            "incident_id": incident_id,
            "status": "Ingested"
        }


def get_incident_ingestion() -> IncidentPostmortemIngestionPipeline:
    """Get Incident Postmortem Ingestion instance."""
    return IncidentPostmortemIngestionPipeline()
