"""MLOps Data Agent for feature stores, data drift detection, and data versioning."""
from typing import Dict, List, Optional
from config.logging_config import get_logger
from services.llm_service import get_llm_service
from services.rag_service import get_rag_service

logger = get_logger("mlops_data_agent")

class MLOpsDataAgent:
    """Specialized agent for MLOps data pipelines, Feast feature stores, and drift monitors."""

    SYSTEM_PROMPT = """You are an expert MLOps and Machine Learning Data Engineer. You specialize in:
- Designing offline and online feature stores (Feast, Databricks Feature Store)
- Setting up data drift monitoring metrics (Evidently, PSI/CSI calculations)
- Managing data versioning and lineage configurations (DVC, MLflow data registration)
- Implementing real-time inference data extraction and validation gates

Always provide standard Feast python definitions, DVC command snippets, or drift calculation models."""

    def __init__(self):
        self.llm_service = get_llm_service()
        self.rag_service = get_rag_service()

    def process(self, query: str, context: str = "") -> str:
        """Process an MLOps data related query."""
        rag_context = self.rag_service.get_context(query, k=3)
        full_prompt = f"""{self.SYSTEM_PROMPT}

Context from knowledge base:
{rag_context}

User Query: {query}

Additional Context: {context}

Provide a comprehensive response with Feast configs, DVC commands, or drift monitoring logic where applicable."""

        return self.llm_service.generate(
            full_prompt,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3
        )

    def generate_feast_definition(self) -> str:
        """Generate a basic Feast feature definition file."""
        code = """from datetime import timedelta
from feast import (
    Entity,
    FeatureView,
    Field,
    FileSource,
    Project,
)
from feast.types import Float32, Int64

# Define project name
project = Project(name="user_clicks_analytics", description="User features for recommendation model")

# Entity defining primary key
user = Entity(name="user_id", value_type=Int64, description="Primary key identifying users")

# Data source pointing to parquet files (Offline store)
clicks_source = FileSource(
    path="/data/features/user_clicks.parquet",
    event_timestamp_column="event_timestamp",
    created_timestamp_column="created_timestamp",
)

# Feature view grouping features
user_clicks_view = FeatureView(
    name="user_clicks_features",
    entities=[user],
    ttl=timedelta(days=1),
    schema=[
        Field(name="count_clicks_1h", dtype=Int64),
        Field(name="ctr_ratio", dtype=Float32),
    ],
    online=True,
    source=clicks_source,
    tags={"team": "recommendation"},
)
"""
        return code

    def generate_drift_detection_check(self) -> str:
        """Generate Python code for a simple data drift monitor using KS-test."""
        code = """import numpy as np
from scipy import stats

def detect_drift_kolmogorov_smirnov(baseline_data: np.ndarray, current_data: np.ndarray, alpha: float = 0.05) -> dict:
    \"\"\"
    Compare target baseline feature values with inference batch values using the KS-test.
    If p-value is lower than significance alpha, data drift is detected.
    \"\"\"
    ks_stat, p_value = stats.ks_2samp(baseline_data, current_data)
    drift_detected = p_value < alpha
    
    return {
        "statistic": float(ks_stat),
        "p_value": float(p_value),
        "drift_detected": bool(drift_detected),
        "alpha": alpha,
        "notes": "Null Hypothesis: Baseline and Current data distributions are identical. Reject if p < alpha."
    }
"""
        return code


def get_mlops_data_agent() -> MLOpsDataAgent:
    """Get MLOps Data agent instance."""
    return MLOpsDataAgent()
