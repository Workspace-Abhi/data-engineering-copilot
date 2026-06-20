"""Pipeline query plan profiler for detecting data skew and bottlenecks."""
from typing import Dict, List, Optional
from config.logging_config import get_logger

logger = get_logger("pipeline_profiler")

class PipelineProfilerService:
    """Analyzes execution plans and profiles queries for bottleneck discovery."""

    def profile_explain_plan(self, explain_output: str, dialect: str = "spark") -> Dict:
        """Parse execution explain output and locate bottlenecks."""
        logger.info(f"Profiling {dialect} explain plan...")
        
        bottlenecks = []
        recommendations = []
        
        explain_lower = explain_output.lower()
        
        if dialect == "spark":
            if "cartesianproduct" in explain_lower:
                bottlenecks.append("Cartesian Product join detected in plan.")
                recommendations.append("Convert implicit join to explicit join or use broadcast join if one table is small.")
            if "exchange" in explain_lower:
                bottlenecks.append("Heavy shuffle Exchange operations detected.")
                recommendations.append("Consider bucketizing source datasets or optimizing partition counts.")
        elif dialect == "sql":
            if "table scan" in explain_lower or "index scan" in explain_lower:
                bottlenecks.append("Table scan / Index scan operations detected.")
                recommendations.append("Create non-clustered indexes on columns used in join or where clauses.")
            if "hash match" in explain_lower:
                bottlenecks.append("Hash Match join operation detected.")
                recommendations.append("Consider optimizing statistics or rewriting query using subqueries.")

        return {
            "dialect": dialect,
            "has_bottlenecks": len(bottlenecks) > 0,
            "bottlenecks": bottlenecks if bottlenecks else ["No high-risk operations detected in query plan."],
            "recommendations": recommendations if recommendations else ["Query plan looks optimal."]
        }


def get_pipeline_profiler() -> PipelineProfilerService:
    """Get pipeline profiler instance."""
    return PipelineProfilerService()
