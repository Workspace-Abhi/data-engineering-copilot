"""SQL Agent for validation, reconciliation, CDC, and MERGE operations."""
from typing import Dict, List, Optional
from config.logging_config import get_logger
from services.llm_service import get_llm_service
from services.rag_service import get_rag_service

logger = get_logger("sql_agent")

class SQLAgent:
    """Specialized agent for SQL-related tasks."""

    SYSTEM_PROMPT = """You are an expert SQL Data Engineer. You specialize in:
- SQL query validation and optimization
- Data reconciliation between sources
- Change Data Capture (CDC) patterns
- MERGE statement generation
- Schema design and normalization
- Performance tuning and indexing

Always provide production-ready SQL with comments explaining the logic.
Use best practices for the specific database platform when mentioned."""

    def __init__(self):
        self.llm_service = get_llm_service()
        self.rag_service = get_rag_service()

    def process(self, query: str, context: str = "") -> str:
        """Process a SQL-related query."""
        # Get RAG context
        rag_context = self.rag_service.get_context(query, k=3)

        full_prompt = f"""{self.SYSTEM_PROMPT}

Context from knowledge base:
{rag_context}

User Query: {query}

Additional Context: {context}

Provide a comprehensive response with SQL code examples where applicable."""

        response = self.llm_service.generate(
            full_prompt,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3
        )

        return response

    def validate_query(self, sql: str, dialect: str = "sqlserver") -> Dict:
        """Validate a SQL query for syntax and best practices."""
        prompt = f"""Validate the following {dialect} SQL query. Check for:
1. Syntax correctness
2. Performance issues
3. Security concerns (SQL injection risks)
4. Best practices adherence
5. Missing indexes or optimizations

SQL Query:
```sql
{sql}
```

Provide a structured analysis with severity levels (Critical/Warning/Info)."""

        response = self.llm_service.generate(prompt, system_prompt=self.SYSTEM_PROMPT, temperature=0.2)
        return {"validation": response, "sql": sql}

    def generate_merge(self, source_table: str, target_table: str, key_columns: List[str], 
                       update_columns: List[str], insert_columns: List[str] = None) -> str:
        """Generate a MERGE statement."""
        key_join = " AND ".join([f"S.{col} = T.{col}" for col in key_columns])
        update_set = ", ".join([f"T.{col} = S.{col}" for col in update_columns])

        if insert_columns is None:
            insert_columns = update_columns + key_columns

        insert_cols = ", ".join(insert_columns)
        insert_vals = ", ".join([f"S.{col}" for col in insert_columns])

        merge_sql = f"""MERGE INTO {target_table} AS T
USING {source_table} AS S
    ON {key_join}
WHEN MATCHED THEN
    UPDATE SET {update_set}
WHEN NOT MATCHED BY TARGET THEN
    INSERT ({insert_cols})
    VALUES ({insert_vals});
"""
        return merge_sql

    def generate_cdc(self, table_name: str, key_column: str = "ID") -> str:
        """Generate CDC tracking SQL."""
        cdc_sql = f"""-- Enable CDC on the database
EXEC sys.sp_cdc_enable_db;
GO

-- Enable CDC on the table
EXEC sys.sp_cdc_enable_table
    @source_schema = N'dbo',
    @source_name = N'{table_name}',
    @role_name = NULL,
    @supports_net_changes = 1;
GO

-- Query CDC changes
SELECT 
    sys.fn_cdc_map_lsn_to_time(__.$start_lsn) AS ChangeTime,
    CASE __.$operation
        WHEN 1 THEN 'DELETE'
        WHEN 2 THEN 'INSERT'
        WHEN 3 THEN 'UPDATE (Before)'
        WHEN 4 THEN 'UPDATE (After)'
    END AS ChangeType,
    *
FROM cdc.dbo_{table_name}_CT AS __
WHERE sys.fn_cdc_map_lsn_to_time(__.$start_lsn) >= DATEADD(hour, -1, GETDATE())
ORDER BY __.$start_lsn;
"""
        return cdc_sql

    def reconcile_data(self, source_query: str, target_query: str, key_columns: List[str]) -> str:
        """Generate data reconciliation query."""
        key_join = " AND ".join([f"S.{col} = T.{col}" for col in key_columns])

        reconcile_sql = f"""-- Data Reconciliation Report
WITH SourceCount AS (
    SELECT COUNT(*) AS SourceTotal FROM ({source_query}) AS S
),
TargetCount AS (
    SELECT COUNT(*) AS TargetTotal FROM ({target_query}) AS T
),
MissingInTarget AS (
    SELECT S.*
    FROM ({source_query}) AS S
    LEFT JOIN ({target_query}) AS T ON {key_join}
    WHERE T.{key_columns[0]} IS NULL
),
MissingInSource AS (
    SELECT T.*
    FROM ({target_query}) AS T
    LEFT JOIN ({source_query}) AS S ON {key_join}
    WHERE S.{key_columns[0]} IS NULL
)
SELECT 
    'Source Total' AS Metric, CAST(SourceTotal AS VARCHAR) AS Value FROM SourceCount
UNION ALL
SELECT 
    'Target Total' AS Metric, CAST(TargetTotal AS VARCHAR) AS Value FROM TargetCount
UNION ALL
SELECT 
    'Missing in Target' AS Metric, CAST(COUNT(*) AS VARCHAR) AS Value FROM MissingInTarget
UNION ALL
SELECT 
    'Missing in Source' AS Metric, CAST(COUNT(*) AS VARCHAR) AS Value FROM MissingInSource;
"""
        return reconcile_sql


def get_sql_agent() -> SQLAgent:
    """Get SQL agent instance."""
    return SQLAgent()
