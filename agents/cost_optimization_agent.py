"""Cost Optimization Agent for cluster sizing, storage tiering, and billing suggestions."""
from typing import Dict, List, Optional
from config.logging_config import get_logger
from services.llm_service import get_llm_service
from services.rag_service import get_rag_service

logger = get_logger("cost_optimization_agent")

class CostOptimizationAgent:
    """Specialized agent for cost optimization and capacity recommendations."""

    SYSTEM_PROMPT = """You are an expert Data FinOps Engineer and Cloud Cost Optimizer. You specialize in:
- Analyzing cloud billing trends and spotting cost anomalies
- Recommending optimal cluster sizing for Spark (Databricks, EMR, Dataproc) and SQL warehouses
- Designing lifecycle policies and storage tiering (Hot, Cool, Cold, Archive)
- Optimizing serverless scaling and idle resource shutdown policies
- Maximizing spot instance utilization

Always provide clear, quantitative cost saving estimates and sizing guidelines."""

    def __init__(self):
        self.llm_service = get_llm_service()
        self.rag_service = get_rag_service()

    def process(self, query: str, context: str = "") -> str:
        """Process a cost optimization query."""
        rag_context = self.rag_service.get_context(query, k=3)
        full_prompt = f"""{self.SYSTEM_PROMPT}

Context from knowledge base:
{rag_context}

User Query: {query}

Additional Context: {context}

Provide a comprehensive response with cost saving calculations and sizing recommendations where applicable."""

        return self.llm_service.generate(
            full_prompt,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3
        )

    def suggest_cluster_sizing(self, workload_type: str, data_size_gb: int) -> Dict:
        """Provide a cluster configuration and cost analysis recommendation."""
        # Simple heuristic sizing
        if data_size_gb < 50:
            vm_size = "Standard_DS3_v2" if workload_type == "ETL" else "Standard_F4s"
            worker_count = 2
            notes = "Small dataset workload. Standard instances sufficient."
        elif data_size_gb < 500:
            vm_size = "Standard_E8ds_v4" if workload_type == "ETL" else "Standard_DS4_v2"
            worker_count = 4
            notes = "Medium workload. Memory-optimized instances suggested for ETL."
        else:
            vm_size = "Standard_E16ds_v4"
            worker_count = 8
            notes = "Large scale processing. Dedicated memory-optimized cluster with autoscale enabled (min 4, max 16)."

        return {
            "workload_type": workload_type,
            "data_size_gb": data_size_gb,
            "suggested_vm": vm_size,
            "worker_count": worker_count,
            "autoscale": data_size_gb >= 500,
            "notes": notes
        }

    def suggest_storage_tiering(self, retention_days: int) -> str:
        """Generate storage tiering lifecycle policies (Azure ADLS / AWS S3 format)."""
        policy = f"""{{
  "rules": [
    {{
      "name": "data_lake_lifecycle_policy",
      "enabled": true,
      "type": "Lifecycle",
      "definition": {{
        "actions": {{
          "baseBlob": {{
            "tierToCool": {{ "daysAfterModificationGreaterThan": 30 }},
            "tierToArchive": {{ "daysAfterModificationGreaterThan": {retention_days} }},
            "delete": {{ "daysAfterModificationGreaterThan": {retention_days + 180} }}
          }}
        }},
        "filters": {{
          "blobTypes": [ "blockBlob" ],
          "prefixMatch": [ "raw-landing/", "processed-silver/" ]
        }}
      }}
    }}
  ]
}}"""
        return policy


def get_cost_optimization_agent() -> CostOptimizationAgent:
    """Get Cost Optimization agent instance."""
    return CostOptimizationAgent()
