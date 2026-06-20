"""Databricks Agent for PySpark, Delta Lake, SCD Type 1/2."""
from typing import Dict, List, Optional
from config.logging_config import get_logger
from services.llm_service import get_llm_service
from services.rag_service import get_rag_service

logger = get_logger("databricks_agent")

class DatabricksAgent:
    """Specialized agent for Databricks/PySpark tasks."""

    SYSTEM_PROMPT = """You are an expert Databricks and PySpark Data Engineer. You specialize in:
- PySpark DataFrame operations and transformations
- Delta Lake table management and optimization
- Slowly Changing Dimensions (SCD) Type 1 and Type 2
- Spark performance tuning and optimization
- Databricks Unity Catalog and governance
- Structured Streaming pipelines
- Auto Loader and Delta Live Tables

Always provide production-ready PySpark code with comments.
Include optimization hints and best practices."""

    def __init__(self):
        self.llm_service = get_llm_service()
        self.rag_service = get_rag_service()

    def process(self, query: str, context: str = "") -> str:
        """Process a Databricks-related query."""
        rag_context = self.rag_service.get_context(query, k=3)

        full_prompt = f"""{self.SYSTEM_PROMPT}

Context from knowledge base:
{rag_context}

User Query: {query}

Additional Context: {context}

Provide a comprehensive response with PySpark/Delta Lake code examples where applicable."""

        response = self.llm_service.generate(
            full_prompt,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3
        )

        return response

    def generate_scd_type1(self, table_name: str, key_columns: List[str], 
                           update_columns: List[str]) -> str:
        """Generate SCD Type 1 (overwrite) PySpark code."""
        key_condition = " AND ".join([f"target.{col} = source.{col}" for col in key_columns])
        update_expr = ", ".join([f"target.{col} = source.{col}" for col in update_columns])

        code = f"""from delta.tables import DeltaTable
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SCD_Type1").getOrCreate()

# Load target Delta table
target_table = DeltaTable.forPath(spark, "/path/to/{table_name}")

# Source DataFrame (your incoming data)
source_df = spark.read.format("delta").load("/path/to/source")

# Perform SCD Type 1 - Overwrite existing records
(target_table.alias("target")
    .merge(
        source_df.alias("source"),
        "{key_condition}"
    )
    .whenMatchedUpdate(set={{
        {", ".join([f'"{col}": "source.{col}"' for col in update_columns])}
    }})
    .whenNotMatchedInsert(values={{
        {", ".join([f'"{col}": f"source.{col}"' for col in key_columns + update_columns])}
    }})
    .execute()
)

print(f"SCD Type 1 merge completed for {table_name}")
"""
        return code

    def generate_scd_type2(self, table_name: str, key_columns: List[str],
                           tracking_columns: List[str], 
                           effective_date_col: str = "effective_date",
                           end_date_col: str = "end_date",
                           is_current_col: str = "is_current") -> str:
        """Generate SCD Type 2 (history tracking) PySpark code."""
        key_condition = " AND ".join([f"target.{col} = source.{col}" for col in key_columns])

        code = f"""from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_date, lit

spark = SparkSession.builder.appName("SCD_Type2").getOrCreate()

# Load target Delta table with history
target_table = DeltaTable.forPath(spark, "/path/to/{table_name}")

# Source DataFrame with new data
source_df = spark.read.format("delta").load("/path/to/source")

# Step 1: Close existing records that have changed
(target_table.alias("target")
    .merge(
        source_df.alias("source"),
        "{key_condition} AND target.{is_current_col} = true"
    )
    .whenMatchedUpdate(set={{
        "{end_date_col}": "current_date() - 1",
        "{is_current_col}": "lit(false)"
    }})
    .execute()
)

# Step 2: Insert new records (both new and changed)
new_records = source_df.withColumn("{effective_date_col}", current_date())                        .withColumn("{end_date_col}", lit(None).cast("date"))                        .withColumn("{is_current_col}", lit(True))

new_records.write.format("delta").mode("append").save("/path/to/{table_name}")

print(f"SCD Type 2 merge completed for {table_name}")
"""
        return code

    def optimize_delta_table(self, table_path: str, zorder_columns: List[str] = None) -> str:
        """Generate Delta table optimization code."""
        zorder_clause = f"ZORDER BY ({', '.join(zorder_columns)})" if zorder_columns else ""

        code = f"""from delta.tables import DeltaTable
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("DeltaOptimize").getOrCreate()

# Optimize the Delta table
delta_table = DeltaTable.forPath(spark, "{table_path}")

# Run OPTIMIZE to compact small files
spark.sql('''
    OPTIMIZE delta.`{table_path}`
    {zorder_clause}
''')

# Run VACUUM to remove old versions (keep 7 days)
delta_table.vacuum(168)  # 168 hours = 7 days

# Show table history
history = delta_table.history()
history.show()

print("Delta table optimization completed")
"""
        return code


def get_databricks_agent() -> DatabricksAgent:
    """Get Databricks agent instance."""
    return DatabricksAgent()
