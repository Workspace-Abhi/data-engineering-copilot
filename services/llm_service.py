"""Ollama LLM integration and embeddings service."""
import os
import json
import requests
from typing import List, Dict, Optional, Generator
import streamlit as st
from config.settings import (
    OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_EMBEDDING_MODEL,
    OLLAMA_TIMEOUT, MAX_TOKENS, TEMPERATURE, TOP_P
)
from config.logging_config import get_logger

logger = get_logger("llm_service")

class OllamaService:
    """Service for interacting with Ollama LLM with simulated fallback support."""

    def __init__(self, model: str = None, base_url: str = None):
        self.base_url = base_url or OLLAMA_BASE_URL
        self.model = model or OLLAMA_MODEL
        self.embedding_model = OLLAMA_EMBEDDING_MODEL
        self.timeout = OLLAMA_TIMEOUT
        logger.info(f"Initialized OllamaService with model: {self.model}")

    def check_connection(self) -> bool:
        """Check if Ollama is running."""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.debug(f"Ollama connection failed: {e}")
            return False

    def list_models(self) -> List[str]:
        """List available models."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            data = response.json()
            return [m["name"] for m in data.get("models", [])]
        except Exception as e:
            logger.debug(f"Failed to list models: {e}")
            return []

    def _is_simulated(self) -> bool:
        """Helper to check if simulated mode should be active."""
        try:
            # Check Streamlit session state
            if st.session_state.get("simulated_mode", False):
                return True
        except Exception:
            # Check environment variable for testing/CLI
            if os.environ.get("SIMULATED_MODE") == "True":
                return True
        # If Ollama is not connected, default to simulated mode to prevent errors
        return not self.check_connection()

    def _simulated_generate(self, prompt: str, system_prompt: str = None) -> str:
        """Generate a high-fidelity mock response for data engineering agents."""
        prompt_lower = prompt.lower()
        sys_prompt_lower = (system_prompt or "").lower()

        # 1. SQL Agent
        if "sql" in sys_prompt_lower or "sql" in prompt_lower or "reconcile" in prompt_lower:
            if "validate" in prompt_lower:
                return """### SQL Query Validation Report

*   **Dialect**: SQL Server / Synapse Analytics
*   **Status**: ⚠️ Validation Completed (with Warnings)

#### 🔍 Analysis Summary

| Severity | Category | Description | Recommendation |
| :--- | :--- | :--- | :--- |
| ⚠️ **Warning** | Performance | Subquery inside `IN` clause can lead to expensive table scans. | Rewrite using `EXISTS` or perform an `INNER JOIN`. |
| ⚠️ **Warning** | Performance | Column `ModifiedDate` is used in filtering without a proper index. | Create a non-clustered index on `ModifiedDate`. |
| 🟢 **Info** | Best Practice | Lowercase SQL keywords detected. | Capitalize SQL statements for style consistency (`select` ➔ `SELECT`). |

#### 💡 Optimized Query Recommendation

```sql
-- Original query optimized for performance and style
SELECT 
    c.CustomerID,
    c.Name,
    c.Email
FROM dbo.Customers AS c
WHERE EXISTS (
    SELECT 1 
    FROM dbo.Orders AS o 
    WHERE o.CustomerID = c.CustomerID 
      AND o.OrderDate >= '2026-01-01'
);
```"""
            elif "reconcile" in prompt_lower:
                return """### Data Reconciliation Query Generated

Here is a robust SQL template to reconcile source and target tables, detecting row mismatches and discrepancy metrics:

```sql
-- Data Reconciliation Report
WITH SourceCount AS (
    SELECT COUNT(*) AS SourceTotal FROM (SELECT * FROM dbo.SourceCustomers) AS S
),
TargetCount AS (
    SELECT COUNT(*) AS TargetTotal FROM (SELECT * FROM dbo.TargetCustomers) AS T
),
MissingInTarget AS (
    SELECT S.CustomerID
    FROM (SELECT * FROM dbo.SourceCustomers) AS S
    LEFT JOIN (SELECT * FROM dbo.TargetCustomers) AS T ON S.CustomerID = T.CustomerID
    WHERE T.CustomerID IS NULL
),
MissingInSource AS (
    SELECT T.CustomerID
    FROM (SELECT * FROM dbo.TargetCustomers) AS T
    LEFT JOIN (SELECT * FROM dbo.SourceCustomers) AS S ON S.CustomerID = T.CustomerID
    WHERE S.CustomerID IS NULL
)
SELECT 'Source Total' AS Metric, CAST(SourceTotal AS VARCHAR) AS Value FROM SourceCount
UNION ALL
SELECT 'Target Total' AS Metric, CAST(TargetTotal AS VARCHAR) AS Value FROM TargetCount
UNION ALL
SELECT 'Missing in Target' AS Metric, CAST(COUNT(*) AS VARCHAR) AS Value FROM MissingInTarget
UNION ALL
SELECT 'Missing in Source' AS Metric, CAST(COUNT(*) AS VARCHAR) AS Value FROM MissingInSource;
```"""
            else:
                return """### SQL MERGE Query Generated

Here is an optimized ANSI SQL MERGE query to upsert data from a staging table into your target production table.

```sql
-- ANSI SQL MERGE Statement
MERGE INTO dbo.Customers AS T
USING staging.Customers AS S
    ON S.CustomerID = T.CustomerID
WHEN MATCHED THEN
    UPDATE SET 
        T.Name = S.Name,
        T.Email = S.Email,
        T.ModifiedDate = GETDATE()
WHEN NOT MATCHED BY TARGET THEN
    INSERT (CustomerID, Name, Email, ModifiedDate)
    VALUES (S.CustomerID, S.Name, S.Email, GETDATE());
```"""

        # 2. Databricks Agent
        elif "databricks" in sys_prompt_lower or "pyspark" in prompt_lower or "spark" in prompt_lower or "scd" in prompt_lower:
            return """### PySpark SCD Type 2 Implementation (Slowly Changing Dimensions)

Here is a production-ready PySpark script to run an **SCD Type 2 (History Tracking)** merge into a Delta Lake table.

```python
from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_date, lit, col

spark = SparkSession.builder \\
    .appName("Delta_SCD_Type2") \\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \\
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \\
    .getOrCreate()

# Target Delta table path
target_path = "/mnt/delta/dim_customers"
target_table = DeltaTable.forPath(spark, target_path)

# Incoming updates
source_df = spark.read.format("delta").load("/mnt/delta/stg_customers")

# Step 1: Close existing records that match but have changes
merge_condition = "target.CustomerID = source.CustomerID AND target.is_current = true"
target_table.alias("target").merge(
    source_df.alias("source"),
    merge_condition
).whenMatchedUpdate(set={
    "end_date": "current_date() - 1",
    "is_current": "lit(false)"
}).execute()

# Step 2: Append new active records
new_records = source_df \\
    .withColumn("effective_date", current_date()) \\
    .withColumn("end_date", lit(None).cast("date")) \\
    .withColumn("is_current", lit(True))

new_records.write.format("delta").mode("append").save(target_path)
print("SCD Type 2 Merge Completed Successfully!")
```

#### ⚡ Delta Table Best Practices
1.  **Z-Ordering**: Apply `OPTIMIZE target_table ZORDER BY (CustomerID)` on frequently queried keys.
2.  **Vacuuming**: Periodic vacuuming cleans up stale files (`deltaTable.vacuum(168)`)."""

        # 3. ADF Agent
        elif "adf" in sys_prompt_lower or "azure data factory" in prompt_lower or "pipeline" in prompt_lower:
            return """### Azure Data Factory Watermark Pipeline Setup

To implement a watermark-based incremental copy in ADF, you require a 3-step pipeline:
1.  **Lookup Old Watermark**: Read the last processed timestamp from the target config.
2.  **Lookup New Watermark**: Read the maximum timestamp currently in the source.
3.  **Copy Data**: Extract rows from source where `WatermarkDate > LastWatermark` and write to target.

#### 🔷 ADF Pipeline Definition Snippet (JSON)

```json
{
  "name": "IncrementalCopyPipeline",
  "properties": {
    "activities": [
      {
        "name": "LookupOldWatermark",
        "type": "Lookup",
        "typeProperties": {
          "source": {
            "type": "AzureSqlSource",
            "sqlReaderQuery": "SELECT LastValue FROM dbo.WatermarkTable WHERE TableName = 'dbo.Customers'"
          },
          "dataset": { "referenceName": "WatermarkDB", "type": "DatasetReference" }
        }
      },
      {
        "name": "CopyData",
        "type": "Copy",
        "dependsOn": [
          { "activity": "LookupOldWatermark", "dependencyConditions": ["Succeeded"] }
        ],
        "typeProperties": {
          "source": {
            "type": "AzureSqlSource",
            "sqlReaderQuery": {
              "value": "SELECT * FROM dbo.Customers WHERE ModifiedDate > '@{activity('LookupOldWatermark').output.firstRow.LastValue}'",
              "type": "Expression"
            }
          },
          "sink": { "type": "AzureSqlSink", "writeBehavior": "upsert" }
        }
      }
    ]
  }
}
```

#### ⚙️ Dynamic Expression Template
To dynamically create a folder path by year/month/day in your sink dataset:
`@concat('raw/customers/', formatDateTime(utcnow(), 'yyyy/MM/dd'))`"""

        # 4. Dataverse Agent
        elif "dataverse" in sys_prompt_lower or "dataverse" in prompt_lower or "mapping" in prompt_lower:
            return """### Microsoft Dataverse Ingestion and Mapping

Here is the recommended field mapping and ingestion script for Dataverse.

#### 📋 Schema Mapping Guide

| Source Column | Dataverse Column | Dataverse Type | Logical Name |
| :--- | :--- | :--- | :--- |
| `CustomerID` | `cr_customerid` | Single Line of Text (Key) | Primary Key |
| `Name` | `cr_name` | Single Line of Text | Name |
| `Email` | `cr_emailaddress` | Email | Email Address |
| `Status` | `cr_statuscode` | Choice (OptionSet) | Status Code |

#### 🐍 Python SDK Ingestion script using MSAL Auth

```python
import requests
import json
from msal import ConfidentialClientApplication

# Auth Configuration
authority_url = "https://login.microsoftonline.com/YOUR_TENANT_ID"
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
resource_url = "https://YOUR_ORG.crm.dynamics.com"

app = ConfidentialClientApplication(client_id, authority=authority_url, client_secret=client_secret)
token_result = app.acquire_token_for_client(scopes=[f"{resource_url}/.default"])
access_token = token_result['access_token']

# API Call to upsert contact
headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "OData-MaxVersion": "4.0",
    "OData-Version": "4.0",
    "Prefer": "return=representation"
}

payload = {
    "cr_name": "John Doe",
    "cr_emailaddress": "john.doe@example.com",
    "cr_statuscode": 841200000 # Option Set value
}

# Upsert (using alternate key)
url = f"{resource_url}/api/data/v9.2/cr_customers(cr_customerid='CUST-100')"
response = requests.patch(url, headers=headers, data=json.dumps(payload))
print(f"Dataverse Response: {response.status_code}")
```"""

        # 5. Jira Agent
        elif "jira" in sys_prompt_lower or "jira" in prompt_lower or "ticket" in prompt_lower or "issue" in prompt_lower:
            return """### Jira Issue Technical Analysis & Remediation Plan

*   **Identified Workstream**: Core Data Pipeline Migration
*   **Complexity Estimate**: 🟢 Medium (5 Story Points)

#### 📝 Issue Breakdown

> **Description Summary**: The ingestion pipeline fails to parse date formats from legacy CSV files when they contain empty trailing rows.

#### 🔧 Step-by-Step Remediation Plan

1.  **Step 1: Raw Parser Schema Update**
    Modify `utils/file_parser.py` to allow optional dates and handle blank rows by configuring the pandas engine to ignore trailing empty lines (`skip_blank_lines=True`).
2.  **Step 2: PySpark Schema Coercion**
    Update the Databricks notebook load step to parse date columns using `to_date(col("date_raw"), "yyyy-MM-dd")` instead of relying on automatic type inference.
3.  **Step 3: Unit Testing Validation**
    Create a mock CSV with variable date layouts and empty lines inside `tests/` and run `pytest` to confirm fix.

#### ⚠️ Risk Assessment
*   **Data Quality**: Coercing invalid dates can introduce `NULL` values.
*   **Mitigation**: Divert rows failing validation to a dead-letter Delta path for curation."""

        # 6. Meeting Agent
        elif "meeting" in sys_prompt_lower or "transcript" in prompt_lower or "meeting" in prompt_lower:
            return """### Meeting Transcript Analysis

*   **Subject**: Azure Migration Alignment & Sprint Planning
*   **Focus**: Pipeline refactoring and Delta Lake migration

#### 📋 Discussion Summary
The team discussed replacing the current ADF Copy Activities with PySpark notebooks in Databricks for better flexibility and Delta Lake features. There is a need to establish SCD Type 2 history tracking for customer profiles.

#### 🔑 Key Decisions
*   **Decision 1**: All raw data files will land in Azure Data Lake Storage (ADLS) Gen2 in Parquet format.
*   **Decision 2**: Python `ConfidentialClientApplication` will be used to ingest processed summaries into Microsoft Dataverse.

#### 📝 Action Items

| Action Item | Owner | Deadline | Priority |
| :--- | :--- | :--- | :--- |
| Write the PySpark template for SCD Type 2 updates | @DataEngLead | 2026-06-25 | 🔥 High |
| Document linked service parameters in ADF | @DevOpsEngineer | 2026-06-28 | 🟡 Medium |
| Create Dataverse choice mappings for customer statuses | @BusinessAnalyst | 2026-06-30 | 🟢 Low |"""

        # 7. PPT Agent
        elif "ppt" in sys_prompt_lower or "deck" in prompt_lower or "ppt" in prompt_lower or "presentation" in prompt_lower:
            return """### Executive PowerPoint Storyline: Legacy Migration

Here is a 5-slide structured storyline script designed for C-level presentation.

---

#### 🛝 Slide 1: The Challenge (Modernizing our Data Architecture)
*   **Visual Concept**: A side-by-side comparison of a congested highway (representing legacy pipelines) vs. a fast multi-lane railway.
*   **Bullet Points**:
    *   Legacy pipelines are brittle and expensive to maintain ($40k/yr licensing overhead).
    *   Batch processing latency (12-hour delays) hampers real-time decision making.
    *   No robust history tracking or audit trail for compliance.

---

#### 🛝 Slide 2: The Solution (Modern Lakehouse with Databricks & ADF)
*   **Visual Concept**: A flow diagram showing ADF acting as orchestrator, feeding into Delta Lake bronze/silver/gold levels.
*   **Bullet Points**:
    *   Leverage 100% cloud-scale compute with Azure Databricks.
    *   Delta Lake format guarantees ACID transactions and instant schema enforcement.
    *   Automated historical logs with SCD Type 2.

---

#### 🛝 Slide 3: Ingestion Framework (ADF & Dataverse Integration)
*   **Visual Concept**: System topology showing source systems ingestion to Lakehouse, with high-value metrics piped back to CRM/Dataverse.
*   **Bullet Points**:
    *   Metadata-driven ADF copy pipelines reduce pipeline build time by 60%.
    *   Dataverse Web API synchronization enables sales team insights in real time.

---

#### 🛝 Slide 4: Migration Timeline & Resources
*   **Visual Concept**: A horizontal Gantt Chart covering a 6-week phased migration.
*   **Bullet Points**:
    *   Weeks 1-2: Core Spark framework build & Watermark patterns.
    *   Weeks 3-4: Legacy code migrations and ETL parallel runs.
    *   Weeks 5-6: Testing, validation, cutover, and handoff.

---

#### 🛝 Slide 5: Expected Business Impact
*   **Visual Concept**: A large dashboard KPI layout showing savings and throughput percentages.
*   **Bullet Points**:
    *   **Cost Savings**: $30k+ annual reduction in database licensing fees.
    *   **Latency**: Reduced from 12 hours to under 15 minutes.
    *   **Operations**: Standardized on Python/Spark for easy engineer hiring and maintenance."""

        # 8. Fallback / Chat
        else:
            return """### Welcome to Data Engineering Copilot!

I am running in **Simulation Mode** because Ollama is currently offline or Simulation Mode is active. I can simulate all 8 specialized data engineering agents.

To exit Simulation Mode:
1.  Download and launch Ollama on your system (`ollama serve`).
2.  Pull the required model: `ollama pull llama3.2` (or your preferred model).
3.  Ensure Ollama is accessible at the host URL configured in the sidebar (`http://localhost:11434`).
4.  Toggle off the **Simulated Mode** switch in the sidebar.

#### 💡 Try these requests:
*   *In the SQL tab*: Try creating a MERGE query or validating SQL.
*   *In the Databricks tab*: Generate SCD Type 1 or Type 2 code.
*   *In Chat*: Ask "How to run an incremental copy in ADF?" and see how the router directs your query to the correct specialized agent!"""

    def generate(
        self, 
        prompt: str, 
        system_prompt: str = None,
        temperature: float = None,
        max_tokens: int = None,
        stream: bool = False
    ) -> str:
        """Generate text completion with simulated fallback."""
        if self._is_simulated():
            return self._simulated_generate(prompt, system_prompt)

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": temperature or TEMPERATURE,
                "top_p": TOP_P,
                "num_predict": max_tokens or MAX_TOKENS
            }
        }

        if system_prompt:
            payload["system"] = system_prompt

        try:
            if stream:
                return self._stream_generate(payload)

            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            return self._simulated_generate(prompt, system_prompt)

    def _stream_generate(self, payload: Dict) -> Generator[str, None, None]:
        """Stream generation."""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                stream=True,
                timeout=self.timeout
            )
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if "response" in data:
                        yield data["response"]
        except Exception as e:
            logger.error(f"Stream generation failed: {e}")
            yield f"Error: {str(e)}"

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = None,
        max_tokens: int = None,
        stream: bool = False
    ) -> str:
        """Chat completion with message history and simulated fallback."""
        if self._is_simulated():
            last_message = messages[-1]["content"] if messages else ""
            return self._simulated_generate(last_message)

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "options": {
                "temperature": temperature or TEMPERATURE,
                "top_p": TOP_P,
                "num_predict": max_tokens or MAX_TOKENS
            }
        }

        try:
            if stream:
                return self._stream_chat(payload)

            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "")
        except Exception as e:
            logger.error(f"Chat failed: {e}")
            last_message = messages[-1]["content"] if messages else ""
            return self._simulated_generate(last_message)

    def _stream_chat(self, payload: Dict) -> Generator[str, None, None]:
        """Stream chat completion."""
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                stream=True,
                timeout=self.timeout
            )
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if "message" in data and "content" in data["message"]:
                        yield data["message"]["content"]
        except Exception as e:
            logger.error(f"Stream chat failed: {e}")
            yield f"Error: {str(e)}"

    def embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings with simulated fallback."""
        if self._is_simulated():
            embeddings = []
            for text in texts:
                import hashlib
                # Generate a deterministic hash-based mock embedding vector of size 384
                h = hashlib.sha256(text.encode()).digest()
                vector = [float(b) / 255.0 for b in h] * 12  # 32 * 12 = 384
                embeddings.append(vector)
            return embeddings

        embeddings = []
        for text in texts:
            try:
                response = requests.post(
                    f"{self.base_url}/api/embeddings",
                    json={"model": self.embedding_model, "prompt": text},
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()
                embeddings.append(data.get("embedding", []))
            except Exception as e:
                logger.error(f"Embedding failed for text: {e}")
                # Fallback to hash-based mock embedding
                import hashlib
                h = hashlib.sha256(text.encode()).digest()
                vector = [float(b) / 255.0 for b in h] * 12
                embeddings.append(vector)
        return embeddings

    def embed_single(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        result = self.embed([text])
        return result[0] if result else []



@st.cache_resource
def get_llm_service() -> OllamaService:
    """Get cached LLM service instance."""
    return OllamaService()
