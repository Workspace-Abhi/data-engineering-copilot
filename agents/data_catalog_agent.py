"""Data Catalog Agent for description generation, lineage, and data dictionaries."""
from typing import Dict, List, Optional
import json
from config.logging_config import get_logger
from services.llm_service import get_llm_service
from services.rag_service import get_rag_service

logger = get_logger("data_catalog_agent")

class DataCatalogAgent:
    """Specialized agent for data dictionaries, lineage diagrams, and metadata catalogs."""

    SYSTEM_PROMPT = """You are an expert Data Catalog and Metadata Architect. You specialize in:
- Generating comprehensive descriptions for tables, views, and schemas
- Building data dictionaries with logical names, data types, and descriptions
- Designing data lineage flows and relationship mappings (depends_on, produces)
- Defining metadata taxonomies, tags, and classification schemes

Always provide structured metadata JSON and markdown schemas."""

    def __init__(self):
        self.llm_service = get_llm_service()
        self.rag_service = get_rag_service()

    def process(self, query: str, context: str = "") -> str:
        """Process a data catalog related query."""
        rag_context = self.rag_service.get_context(query, k=3)
        full_prompt = f"""{self.SYSTEM_PROMPT}

Context from knowledge base:
{rag_context}

User Query: {query}

Additional Context: {context}

Provide a comprehensive response with data dictionaries or lineage configurations where applicable."""

        return self.llm_service.generate(
            full_prompt,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3
        )

    def generate_data_dictionary(self, table_name: str, columns: List[Dict]) -> str:
        """Generate markdown representation of a data dictionary."""
        dict_lines = [
            f"### Data Dictionary: {table_name}",
            "",
            "| Column Name | Type | Key | Nullable | Description | Business Term |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |"
        ]

        for col in columns:
            name = col.get("name", "")
            col_type = col.get("type", "varchar")
            is_key = "Yes" if col.get("is_key", False) else "No"
            nullable = "Yes" if col.get("nullable", True) else "No"
            desc = col.get("description", f"Internal field {name}")
            term = name.replace("_", " ").title()
            dict_lines.append(f"| `{name}` | {col_type} | {is_key} | {nullable} | {desc} | {term} |")

        return "\n".join(dict_lines)

    def generate_lineage_definition(self, source_tables: List[str], target_table: str) -> str:
        """Generate Mermaid code block illustrating source-to-target lineage flow."""
        mermaid_lines = [
            "graph LR",
            "    subgraph Sources"
        ]

        for src in source_tables:
            mermaid_lines.append(f"        {src}[Table: {src}]")

        mermaid_lines.append("    end")
        mermaid_lines.append(f"    target[{target_table}]")

        for src in source_tables:
            mermaid_lines.append(f"    {src} -->|ETL Transform| target")

        return "\n".join(mermaid_lines)


def get_data_catalog_agent() -> DataCatalogAgent:
    """Get Data Catalog agent instance."""
    return DataCatalogAgent()
