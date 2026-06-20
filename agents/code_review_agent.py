"""Code Review Agent for detecting anti-patterns, style issues, and security concerns."""
from typing import Dict, List, Optional
from config.logging_config import get_logger
from services.llm_service import get_llm_service
from services.rag_service import get_rag_service

logger = get_logger("code_review_agent")

class CodeReviewAgent:
    """Specialized agent for data code review (SQL, Spark, Python)."""

    SYSTEM_PROMPT = """You are an expert Data Engineering Technical Lead and Code Reviewer. You specialize in:
- Reviewing SQL queries, PySpark, Python, and dbt models
- Spotting data pipeline anti-patterns (e.g. data skew, broadcast join misses, missing partition pruning)
- Detecting security issues (plain-text credentials, SQL injection vulnerabilities)
- Enforcing style rules, formatting, and standard architectures

Always provide structured reviews with specific file lines, impact descriptions, and fix recommendations."""

    def __init__(self):
        self.llm_service = get_llm_service()
        self.rag_service = get_rag_service()

    def process(self, query: str, context: str = "") -> str:
        """Process a code review related query."""
        rag_context = self.rag_service.get_context(query, k=3)
        full_prompt = f"""{self.SYSTEM_PROMPT}

Context from knowledge base:
{rag_context}

User Query: {query}

Additional Context: {context}

Provide a comprehensive response with code review comments and fixes where applicable."""

        return self.llm_service.generate(
            full_prompt,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3
        )

    def review_code_snippet(self, code: str, language: str = "python") -> Dict:
        """Review code snippet for common bugs/violations."""
        findings = []

        if language == "sql":
            if "select *" in code.lower():
                findings.append({
                    "severity": "Warning",
                    "category": "Performance",
                    "description": "Use of 'SELECT *' is a bad practice in production queries. It can cause network bottlenecks.",
                    "fix": "Specify column names explicitly."
                })
            if "join" in code.lower() and "on" not in code.lower():
                findings.append({
                    "severity": "Critical",
                    "category": "Syntax",
                    "description": "Implicit join syntax without an ON clause can cause unwanted Cartesian products.",
                    "fix": "Rewrite using explicit INNER/LEFT JOIN and ON condition."
                })
        else:
            if "password =" in code.lower() or "secret =" in code.lower():
                findings.append({
                    "severity": "Critical",
                    "category": "Security",
                    "description": "Plaintext secret or credential variable detected in source code.",
                    "fix": "Load secrets from environment variables or key vault integrations."
                })
            if ".collect()" in code.lower():
                findings.append({
                    "severity": "Warning",
                    "category": "Performance",
                    "description": "Call to 'DataFrame.collect()' will pull all data onto the driver node, potentially causing OutOfMemory errors.",
                    "fix": "Use show(), take(), or write output directly to a sink instead of collecting to driver."
                })

        return {
            "language": language,
            "findings": findings if findings else [{"severity": "Info", "category": "General", "description": "No immediate anti-patterns detected.", "fix": "N/A"}]
        }


def get_code_review_agent() -> CodeReviewAgent:
    """Get Code Review agent instance."""
    return CodeReviewAgent()
