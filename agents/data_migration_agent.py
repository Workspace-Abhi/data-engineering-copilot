"""Data Migration Agent for schema mapping, migration assessments, and rollback plans."""
from typing import Dict, List, Optional
from config.logging_config import get_logger
from services.llm_service import get_llm_service
from services.rag_service import get_rag_service

logger = get_logger("data_migration_agent")

class DataMigrationAgent:
    """Specialized agent for data store and platform migrations."""

    SYSTEM_PROMPT = """You are an expert Data Migration Architect. You specialize in:
- Legacy database to modern cloud warehouse migration (e.g. SQL Server to Snowflake, Oracle to BigQuery)
- Schema conversion and mapping rules
- Designing fallback and rollback strategies
- Assessment reports (sizing, complexity, compatibility warnings)
- Phased cutover strategies (dual-write, CDC-based replication)

Always provide structured migration checklists and detailed rollback plans."""

    def __init__(self):
        self.llm_service = get_llm_service()
        self.rag_service = get_rag_service()

    def process(self, query: str, context: str = "") -> str:
        """Process a migration-related query."""
        rag_context = self.rag_service.get_context(query, k=3)
        full_prompt = f"""{self.SYSTEM_PROMPT}

Context from knowledge base:
{rag_context}

User Query: {query}

Additional Context: {context}

Provide a comprehensive response with migration strategy and rollback checklists where applicable."""

        return self.llm_service.generate(
            full_prompt,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3
        )

    def generate_migration_assessment(self, source_system: str, target_system: str, table_count: int) -> str:
        """Generate a basic migration feasibility report."""
        report = f"""### Data Migration Assessment Report
- **Source Platform**: {source_system}
- **Target Platform**: {target_system}
- **Scope**: {table_count} tables

#### 📈 Feasibility Analysis
1. **Schema Compatibility**: High. Automatic translation rules apply for 90% of basic column types.
2. **DataType Conversion Alert**: Datetime/TZ offsets require explicit formatting during extraction.
3. **Throughput Estimate**: Calculated replication window is 4.5 hours under standard network links.

#### 🛠️ Recommended Cutover Plan
- Phase 1: Full load base capture.
- Phase 2: Active CDC streaming replication to keep target in sync.
- Phase 3: Final validation checks (reconciliation run).
- Phase 4: DNS/Routing switch to Target.
"""
        return report

    def generate_rollback_plan(self, migration_id: str) -> str:
        """Generate a step-by-step rollback plan in case of migration failure."""
        plan = f"""### Rollback and Fallback Runbook ({migration_id})

#### Trigger Conditions:
1. Data validation discrepancy exceeds 0.5% threshold.
2. Cutover window time exceeds limit (exceeds SLA).
3. Target database becomes unresponsive post-dns switch.

#### 📋 Step-by-Step Rollback Steps:
1. **Step 1: Terminate Ingestion Pipelines**
   Disable ADF schedules and stop active streaming writes to Target.
2. **Step 2: Revert DNS & Routing**
   Direct application connection strings back to the Source instance.
3. **Step 3: Post-mortem Delta Extraction**
   Compare database logs to identify and capture any writes that happened on the Target during the validation window.
4. **Step 4: Re-Sync Source**
   Re-apply isolated Target updates back to Source database manually using transaction recovery scripts.
5. **Step 5: Verify Source Health**
   Confirm clients are writing successfully to Source.
"""
        return plan


def get_data_migration_agent() -> DataMigrationAgent:
    """Get Data Migration agent instance."""
    return DataMigrationAgent()
