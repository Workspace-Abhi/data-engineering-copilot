"""Testing Agent for generating SQL unit tests, integration tests, and mock data."""
from typing import Dict, List, Optional
import json
from config.logging_config import get_logger
from services.llm_service import get_llm_service
from services.rag_service import get_rag_service

logger = get_logger("testing_agent")

class TestingAgent:
    """Specialized agent for data test generation, SQL unit tests, and mock datasets."""

    SYSTEM_PROMPT = """You are an expert Data Testing Engineer. You specialize in:
- Generating mock datasets (CSV, JSON, SQL inserts) with realistic distributions
- Writing SQL unit tests and assertion checks for pipeline transformations
- Designing integration tests for ETL/ELT flows
- Setting up test fixtures and test environments for dbt, Spark, and SQL databases

Always provide runnable test scripts and mock data payloads."""

    def __init__(self):
        self.llm_service = get_llm_service()
        self.rag_service = get_rag_service()

    def process(self, query: str, context: str = "") -> str:
        """Process a data testing related query."""
        rag_context = self.rag_service.get_context(query, k=3)
        full_prompt = f"""{self.SYSTEM_PROMPT}

Context from knowledge base:
{rag_context}

User Query: {query}

Additional Context: {context}

Provide a comprehensive response with test scripts or mock data templates where applicable."""

        return self.llm_service.generate(
            full_prompt,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3
        )

    def generate_sql_unit_test(self, test_name: str, expected_query: str, actual_query: str) -> str:
        """Generate a SQL validation comparison unit test."""
        test_sql = f"""-- Unit Test: {test_name}
WITH Expected AS (
    {expected_query}
),
Actual AS (
    {actual_query}
),
Mismatches AS (
    (SELECT * FROM Expected EXCEPT SELECT * FROM Actual)
    UNION ALL
    (SELECT * FROM Actual EXCEPT SELECT * FROM Expected)
)
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN 'PASS'
        ELSE 'FAIL'
    END AS TestResult,
    COUNT(*) AS MismatchCount
FROM Mismatches;
"""
        return test_sql

    def generate_mock_data(self, columns: List[Dict], row_count: int = 5) -> str:
        """Generate mock INSERT statements."""
        import random
        col_names = [col.get("name", "") for col in columns]
        inserts = []

        for i in range(1, row_count + 1):
            vals = []
            for col in columns:
                col_name = col.get("name", "")
                col_type = col.get("type", "varchar").lower()
                if "int" in col_type:
                    vals.append(str(i))
                elif "float" in col_type or "decimal" in col_type:
                    vals.append(f"{i * 1.5:.2f}")
                elif "email" in col_name.lower():
                    vals.append(f"'user{i}@example.com'")
                else:
                    vals.append(f"'Mock_{col_name}_{i}'")
            
            inserts.append(f"({', '.join(vals)})")

        mock_sql = f"INSERT INTO temp_mock_table ({', '.join(col_names)})\nVALUES\n"
        mock_sql += ",\n".join(inserts) + ";"
        return mock_sql


def get_testing_agent() -> TestingAgent:
    """Get Testing agent instance."""
    return TestingAgent()
