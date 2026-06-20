"""Data Quality Agent for Great Expectations suites and Soda checks."""
from typing import Dict, List, Optional
import json
from config.logging_config import get_logger
from services.llm_service import get_llm_service
from services.rag_service import get_rag_service

logger = get_logger("data_quality_agent")

class DataQualityAgent:
    """Specialized agent for data quality checks, GE, and Soda configurations."""

    SYSTEM_PROMPT = """You are an expert Data Quality Engineer. You specialize in:
- Data quality profiling and validation
- Great Expectations (GE) suite design and configurations
- Soda Core check YAML configurations
- Data profiling and anomaly detection
- Establishing Data Quality SLA/SLOs
- Designing data validation gates in CI/CD pipelines

Always provide production-ready Great Expectations JSON or Python code and Soda YAML configurations."""

    def __init__(self):
        self.llm_service = get_llm_service()
        self.rag_service = get_rag_service()

    def process(self, query: str, context: str = "") -> str:
        """Process a data quality related query."""
        rag_context = self.rag_service.get_context(query, k=3)
        full_prompt = f"""{self.SYSTEM_PROMPT}

Context from knowledge base:
{rag_context}

User Query: {query}

Additional Context: {context}

Provide a comprehensive response with Great Expectations or Soda configuration examples where applicable."""

        return self.llm_service.generate(
            full_prompt,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3
        )

    def generate_great_expectations_suite(self, table_name: str, columns: List[Dict]) -> str:
        """Generate a Great Expectations JSON expectation suite."""
        expectations = []
        for col in columns:
            col_name = col.get("name", "")
            col_type = col.get("type", "").lower()
            nullable = col.get("nullable", True)

            # Standard type mapping
            if "int" in col_type or "float" in col_type or "decimal" in col_type or "numeric" in col_type:
                expectations.append({
                    "expectation_type": "expect_column_values_to_be_of_type",
                    "kwargs": {
                        "column": col_name,
                        "type_": "numeric"
                    }
                })
            else:
                expectations.append({
                    "expectation_type": "expect_column_values_to_be_of_type",
                    "kwargs": {
                        "column": col_name,
                        "type_": "string"
                    }
                })

            if not nullable:
                expectations.append({
                    "expectation_type": "expect_column_values_to_not_be_null",
                    "kwargs": {
                        "column": col_name
                    }
                })

        suite = {
            "expectation_suite_name": f"{table_name}_suite",
            "meta": {
                "great_expectations_version": "0.15.50"
            },
            "expectations": expectations,
            "data_asset_type": "Dataset"
        }
        return json.dumps(suite, indent=2)

    def generate_soda_checks(self, table_name: str, columns: List[Dict]) -> str:
        """Generate Soda Core checks YAML configuration."""
        yaml_lines = [
            f"checks for {table_name}:",
            "  - row_count > 0"
        ]

        for col in columns:
            col_name = col.get("name", "")
            col_type = col.get("type", "").lower()
            nullable = col.get("nullable", True)

            if not nullable:
                yaml_lines.append(f"  - missing_count({col_name}) == 0")

            if "int" in col_type or "float" in col_type:
                # Add sample numeric bounds/validation
                yaml_lines.append(f"  - min({col_name}) >= 0")
            elif "email" in col_name.lower():
                yaml_lines.append(f"  - invalid_count({col_name}) == 0:")
                yaml_lines.append(f"      valid format: email")

        return "\n".join(yaml_lines)


def get_data_quality_agent() -> DataQualityAgent:
    """Get Data Quality agent instance."""
    return DataQualityAgent()
