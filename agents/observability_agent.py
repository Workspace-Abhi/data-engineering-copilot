"""Observability Agent for dashboards, alerts, and SLI/SLO definitions."""
from typing import Dict, List, Optional
from config.logging_config import get_logger
from services.llm_service import get_llm_service
from services.rag_service import get_rag_service

logger = get_logger("observability_agent")

class ObservabilityAgent:
    """Specialized agent for data pipeline observability and monitoring."""

    SYSTEM_PROMPT = """You are an expert Data Reliability and Observability Engineer. You specialize in:
- Defining SLI/SLO/SLAs for data quality, freshness, and ingestion volume
- Designing Grafana, Datadog, or Azure Monitor dashboards for data pipelines
- Setting up prometheus alert manager rules and alert triggers
- Implementing pipeline logging, tracing, and lineage metadata capture

Always provide structured SLI/SLO templates and prometheus alert rules."""

    def __init__(self):
        self.llm_service = get_llm_service()
        self.rag_service = get_rag_service()

    def process(self, query: str, context: str = "") -> str:
        """Process an observability-related query."""
        rag_context = self.rag_service.get_context(query, k=3)
        full_prompt = f"""{self.SYSTEM_PROMPT}

Context from knowledge base:
{rag_context}

User Query: {query}

Additional Context: {context}

Provide a comprehensive response with dashboard design or alert config examples where applicable."""

        return self.llm_service.generate(
            full_prompt,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3
        )

    def generate_sli_slo_definitions(self, service_name: str) -> str:
        """Generate SLI/SLO definitions markdown table."""
        table = f"""### SLI/SLO Monitoring Framework for {service_name}

| Indicator (SLI) | Target Metric (SLO) | Measurement Window | Alerting Threshold |
| :--- | :--- | :--- | :--- |
| **Data Freshness** | 99% of records landed within 15 minutes of source generation. | Daily Rolling | > 30 mins delay trigger warning |
| **Pipeline Success Rate**| 99.5% of nightly batch runs complete successfully on first try. | Monthly | Any failure triggers pagerduty |
| **Volume Anomaly** | Daily row count is within +/- 2 standard deviations of 14-day average. | Daily | 3 consecutive anomalies trigger alert |
| **Data Completeness** | Crucial columns (e.g. ID, Key) are 100% free of NULL values. | Per-batch | Hard fail and reject load |
"""
        return table

    def generate_alert_rules(self) -> str:
        """Generate Prometheus alert manager rules YAML configuration."""
        yaml_config = """groups:
  - name: pipeline_alerts
    rules:
      - alert: IngestionPipelineFailed
        expr: adf_pipeline_status{status="Failed"} > 0
        for: 5m
        labels:
          severity: critical
          tier: data_platform
        annotations:
          summary: "ADF Ingestion pipeline {{ $labels.pipeline_name }} failed"
          description: "Data pipeline execution failed, check ADF Monitor logs."

      - alert: DataFreshnessSLAWarning
        expr: time() - last_ingested_timestamp_seconds > 1800
        for: 10m
        labels:
          severity: warning
          tier: data_platform
        annotations:
          summary: "SLA Warning: Data freshness delay detected"
          description: "Target database has not received updates for over 30 minutes."
"""
        return yaml_config


def get_observability_agent() -> ObservabilityAgent:
    """Get Observability agent instance."""
    return ObservabilityAgent()
