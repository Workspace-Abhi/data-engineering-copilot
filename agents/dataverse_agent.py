"""Dataverse Agent for entity mapping, ingestion, and field types."""
from typing import Dict, List, Optional
from config.logging_config import get_logger
from services.llm_service import get_llm_service
from services.rag_service import get_rag_service

logger = get_logger("dataverse_agent")

class DataverseAgent:
    """Specialized agent for Microsoft Dataverse tasks."""

    SYSTEM_PROMPT = """You are an expert Microsoft Dataverse and Power Platform Engineer. You specialize in:
- Entity design and custom table creation
- Field type mapping and data type conversions
- Data ingestion patterns (Dataflows, Azure Synapse Link)
- Business rules and calculated fields
- Relationships and lookup fields
- Plugin development and custom workflows
- Security roles and field-level security
- API integration (Web API, OData)

Always provide accurate Dataverse schema definitions and C# plugin code when needed.
Include Power Platform best practices."""

    def __init__(self):
        self.llm_service = get_llm_service()
        self.rag_service = get_rag_service()

    def process(self, query: str, context: str = "") -> str:
        """Process a Dataverse-related query."""
        rag_context = self.rag_service.get_context(query, k=3)

        full_prompt = f"""{self.SYSTEM_PROMPT}

Context from knowledge base:
{rag_context}

User Query: {query}

Additional Context: {context}

Provide a comprehensive response with Dataverse schema definitions and code examples where applicable."""

        response = self.llm_service.generate(
            full_prompt,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3
        )

        return response

    def map_sql_to_dataverse(self, sql_table: Dict) -> Dict:
        """Map SQL table schema to Dataverse entity."""
        type_mapping = {
            "int": "Whole Number",
            "bigint": "Whole Number",
            "smallint": "Whole Number",
            "tinyint": "Whole Number",
            "decimal": "Decimal Number",
            "numeric": "Decimal Number",
            "float": "Floating Point Number",
            "real": "Floating Point Number",
            "varchar": "Single Line of Text",
            "nvarchar": "Single Line of Text",
            "text": "Multiple Lines of Text",
            "ntext": "Multiple Lines of Text",
            "datetime": "Date and Time",
            "datetime2": "Date and Time",
            "date": "Date Only",
            "time": "Time Only",
            "bit": "Two Options",
            "uniqueidentifier": "Unique Identifier",
            "varbinary": "File",
            "image": "Image",
            "money": "Currency"
        }

        entity = {
            "name": sql_table.get("name", ""),
            "display_name": sql_table.get("name", "").replace("_", " ").title(),
            "description": f"Dataverse entity mapped from {sql_table.get('name', '')}",
            "fields": []
        }

        for col in sql_table.get("columns", []):
            sql_type = col.get("type", "").lower().split("(")[0]
            dv_type = type_mapping.get(sql_type, "Single Line of Text")

            field = {
                "name": col.get("name", ""),
                "display_name": col.get("name", "").replace("_", " ").title(),
                "data_type": dv_type,
                "required": col.get("nullable", True) == False,
                "description": col.get("description", "")
            }
            entity["fields"].append(field)

        return entity

    def generate_ingestion_flow(self, source_entity: str, target_entity: str,
                                mapping: Dict[str, str]) -> str:
        """Generate Power Automate/Dataflow ingestion configuration."""
        transform_steps = []
        for source_col, target_col in mapping.items():
            transform_steps.append(f'    RenameColumn("{source_col}", "{target_col}")')

        flow_config = f"""// Power Query M Code for Dataverse Ingestion
let
    Source = Sql.Database("server", "database"),
    {source_entity} = Source{{[Schema="dbo", Item="{source_entity}"]}}[Data],

    // Transformations
    RenamedColumns = Table.RenameColumns({source_entity}, {{
        {", ".join([f'"{k}", "{v}"' for k, v in mapping.items()])}
    }}),

    // Data type conversions
    ChangedTypes = Table.TransformColumnTypes(RenamedColumns, {{
        {", ".join(['{"' + v + '", type text}' for v in mapping.values()])}
    }}),

    // Load to Dataverse
    LoadToDataverse = Dataverse.Load(
        ChangedTypes,
        "{target_entity}",
        [Upsert = true]
    )
in
    LoadToDataverse
"""
        return flow_config


def get_dataverse_agent() -> DataverseAgent:
    """Get Dataverse agent instance."""
    return DataverseAgent()
