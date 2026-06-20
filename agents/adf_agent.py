"""ADF Agent for pipeline design, expressions, and watermark patterns."""
from typing import Dict, List, Optional
from config.logging_config import get_logger
from services.llm_service import get_llm_service
from services.rag_service import get_rag_service

logger = get_logger("adf_agent")

class ADFAgent:
    """Specialized agent for Azure Data Factory tasks."""

    SYSTEM_PROMPT = """You are an expert Azure Data Factory (ADF) Engineer. You specialize in:
- Pipeline design and architecture
- Data Flow transformations and expressions
- Copy Activity configurations and optimizations
- Watermark patterns for incremental loads
- Parameterization and dynamic content
- Integration Runtime setup and management
- Linked Service configurations
- Trigger scheduling and monitoring

Always provide JSON pipeline definitions and expression syntax.
Include best practices for performance and reliability."""

    def __init__(self):
        self.llm_service = get_llm_service()
        self.rag_service = get_rag_service()

    def process(self, query: str, context: str = "") -> str:
        """Process an ADF-related query."""
        rag_context = self.rag_service.get_context(query, k=3)

        full_prompt = f"""{self.SYSTEM_PROMPT}

Context from knowledge base:
{rag_context}

User Query: {query}

Additional Context: {context}

Provide a comprehensive response with ADF JSON definitions and expressions where applicable."""

        response = self.llm_service.generate(
            full_prompt,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3
        )

        return response

    def generate_watermark_pipeline(self, source_table: str, target_table: str,
                                    watermark_column: str = "ModifiedDate",
                                    source_connection: str = "SourceSQL",
                                    target_connection: str = "TargetSQL") -> Dict:
        """Generate a watermark-based incremental load pipeline."""

        pipeline_json = {
            "name": f"IncrementalLoad_{source_table}",
            "properties": {
                "activities": [
                    {
                        "name": "LookupWatermark",
                        "type": "Lookup",
                        "dependsOn": [],
                        "policy": {
                            "timeout": "0.12:00:00",
                            "retry": 0,
                            "retryIntervalInSeconds": 30
                        },
                        "typeProperties": {
                            "source": {
                                "type": "AzureSqlSource",
                                "sqlReaderQuery": f"SELECT MAX({watermark_column}) AS WatermarkValue FROM {target_table}"
                            },
                            "dataset": {
                                "referenceName": target_connection,
                                "type": "DatasetReference"
                            }
                        }
                    },
                    {
                        "name": "CopyIncrementalData",
                        "type": "Copy",
                        "dependsOn": [
                            {
                                "activity": "LookupWatermark",
                                "dependencyConditions": ["Succeeded"]
                            }
                        ],
                        "policy": {
                            "timeout": "0.12:00:00",
                            "retry": 0
                        },
                        "typeProperties": {
                            "source": {
                                "type": "AzureSqlSource",
                                "sqlReaderQuery": {
                                    "value": f"SELECT * FROM {source_table} WHERE {watermark_column} > '@{{activity('LookupWatermark').output.firstRow.WatermarkValue}}'",
                                    "type": "Expression"
                                }
                            },
                            "sink": {
                                "type": "AzureSqlSink",
                                "writeBehavior": "upsert",
                                "upsertSettings": {
                                    "keys": ["ID"]
                                }
                            }
                        },
                        "inputs": [
                            {
                                "referenceName": source_connection,
                                "type": "DatasetReference"
                            }
                        ],
                        "outputs": [
                            {
                                "referenceName": target_connection,
                                "type": "DatasetReference"
                            }
                        ]
                    }
                ]
            }
        }

        return pipeline_json

    def generate_expression(self, expression_type: str, **kwargs) -> str:
        """Generate ADF dynamic expressions."""
        expressions = {
            "current_date": "@utcnow()",
            "format_date": "@formatDateTime(utcnow(), 'yyyy-MM-dd')",
            "pipeline_name": "@pipeline().Pipeline",
            "run_id": "@pipeline().RunId",
            "trigger_time": "@pipeline().TriggerTime",
            "parameter": "@pipeline().parameters.paramName",
            "concat": "@concat('prefix', variables('varName'))",
            "if_condition": "@if(equals(variables('var'), 'value'), 'true_result', 'false_result')",
            "coalesce": "@coalesce(activity('Lookup').output.firstRow.Value, 'default')",
            "string_interpolation": "@concat('File_', formatDateTime(utcnow(), 'yyyyMMdd'), '.csv')",
            "folder_path": "@concat('raw/', formatDateTime(utcnow(), 'yyyy/MM/dd'))"
        }

        return expressions.get(expression_type, "Expression not found")

    def generate_copy_activity(self, source_type: str, sink_type: str,
                                source_config: Dict, sink_config: Dict) -> Dict:
        """Generate a copy activity configuration."""
        copy_activity = {
            "name": f"Copy_{source_type}_to_{sink_type}",
            "type": "Copy",
            "typeProperties": {
                "source": {
                    "type": source_type,
                    **source_config
                },
                "sink": {
                    "type": sink_type,
                    **sink_config
                }
            }
        }
        return copy_activity


def get_adf_agent() -> ADFAgent:
    """Get ADF agent instance."""
    return ADFAgent()
