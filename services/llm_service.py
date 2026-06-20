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

    def _extract_vars(self, prompt: str) -> Dict:
        """Helper to dynamically parse source/target/keys variables from prompt for simulation."""
        import re
        
        # Dialect extraction
        dialect = "SQL Server"
        dialects = ["mysql", "postgresql", "oracle", "snowflake", "bigquery", "sqlserver"]
        for d in dialects:
            if d in prompt.lower():
                dialect = d.capitalize()
                if dialect == "Sqlserver":
                    dialect = "SQL Server / Synapse"
                break
                
        # Parse table names/paths (regex matching /mnt/... or schema.table or plain name)
        tables = re.findall(r'(?:[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+|/[a-zA-Z0-9_/-]+|[a-zA-Z0-9_]+_table|[a-zA-Z0-9_]+_path)', prompt)
        source = "/mnt/staging/customers"
        target = "/mnt/delta/customers"
        
        # Try to find specific inputs
        if len(tables) >= 2:
            source = tables[0]
            target = tables[1]
        elif len(tables) == 1:
            target = tables[0]
            source = tables[0] + "_stg"
            
        # Parse key columns
        keys = ["customer_id"]
        key_match = re.search(r'(?:key_columns|key_cols|keys?|primary_keys?|key_fields?):\s*([a-zA-Z0-9_, ]+)', prompt, re.IGNORECASE)
        if key_match:
            keys = [k.strip() for k in key_match.group(1).split(",")]
            
        # Parse tracking/update columns
        update_cols = ["name", "email", "status", "updated_at"]
        update_match = re.search(r'(?:update_cols|update_columns|track_cols|columns|cols):\s*([a-zA-Z0-9_, ]+)', prompt, re.IGNORECASE)
        if update_match:
            update_cols = [c.strip() for c in update_match.group(1).split(",")]

        return {
            "dialect": dialect,
            "source": source,
            "target": target,
            "keys": keys,
            "update_cols": update_cols
        }

    def _simulated_generate(self, prompt: str, system_prompt: str = None) -> str:
        """Generate a high-fidelity dynamic mock response for data engineering agents."""
        prompt_lower = prompt.lower()
        sys_prompt_lower = (system_prompt or "").lower()
        
        # Extract variables from prompt dynamically
        v = self._extract_vars(prompt)
        join_cond = " AND ".join([f"T.{k} = S.{k}" for k in v["keys"]])
        updates_set = ", ".join([f"T.{col} = S.{col}" for col in v["update_cols"]])
        cols_list = ", ".join(v["keys"] + v["update_cols"])
        s_cols_list = ", ".join([f"S.{col}" for col in v["keys"] + v["update_cols"]])

        # 1. SQL Agent
        if "sql" in sys_prompt_lower or "sql" in prompt_lower or "reconcile" in prompt_lower:
            if "validate" in prompt_lower:
                return f"""### SQL Query Validation Report

*   **Dialect**: {v["dialect"]}
*   **Status**: ⚠️ Validation Completed (with Warnings)

#### 🔍 Analysis Summary

| Severity | Category | Description | Recommendation |
| :--- | :--- | :--- | :--- |
| ⚠️ **Warning** | Performance | Column `ModifiedDate` is used in filtering without a proper index. | Create a non-clustered index on `ModifiedDate`. |
| ⚠️ **Warning** | Performance | Inefficient outer join detected on source table `{v["source"]}`. | Convert to an `INNER JOIN` if nullable rows are not required. |
| 🟢 **Info** | Style | Lowercase SQL keywords detected. | Capitalize SELECT, WHERE, FROM to keep SQL code tidy. |

#### 💡 Optimized Query Recommendation

```sql
SELECT 
    c.{v["keys"][0] if v["keys"] else "ID"},
    c.{v["update_cols"][0] if v["update_cols"] else "Name"}
FROM {v["source"]} AS c
WHERE c.ModifiedDate >= '2026-01-01';
```"""
            elif "reconcile" in prompt_lower:
                return f"""### Data Reconciliation Query Generated

Here is a reconciliation template dynamically built to match rows and detect mismatches between `{v["source"]}` and `{v["target"]}`:

```sql
-- Reconciliation query for {v["target"]}
WITH SourceCount AS (
    SELECT COUNT(*) AS SourceTotal FROM (SELECT * FROM {v["source"]}) AS S
),
TargetCount AS (
    SELECT COUNT(*) AS TargetTotal FROM (SELECT * FROM {v["target"]}) AS T
),
MissingInTarget AS (
    SELECT S.{v["keys"][0]}
    FROM (SELECT * FROM {v["source"]}) AS S
    LEFT JOIN (SELECT * FROM {v["target"]}) AS T ON S.{v["keys"][0]} = T.{v["keys"][0]}
    WHERE T.{v["keys"][0]} IS NULL
),
MissingInSource AS (
    SELECT T.{v["keys"][0]}
    FROM (SELECT * FROM {v["target"]}) AS T
    LEFT JOIN (SELECT * FROM {v["source"]}) AS S ON S.{v["keys"][0]} = T.{v["keys"][0]}
    WHERE S.{v["keys"][0]} IS NULL
)
SELECT 'Source Total' AS Metric, CAST(SourceTotal AS VARCHAR) AS Value FROM SourceCount
UNION ALL
SELECT 'Target Total' AS Metric, CAST(TargetTotal AS VARCHAR) AS Value FROM TargetCount
UNION ALL
SELECT 'Missing in Target (Orphaned)' AS Metric, CAST(COUNT(*) AS VARCHAR) AS Value FROM MissingInTarget
UNION ALL
SELECT 'Missing in Source (Stale)' AS Metric, CAST(COUNT(*) AS VARCHAR) AS Value FROM MissingInSource;
```"""
            else:
                return f"""### Dynamic SQL MERGE Query Generated

Here is an optimized MERGE statement generated dynamically to upsert changes from `{v["source"]}` into target `{v["target"]}`:

```sql
-- MERGE Statement targeting {v["target"]}
MERGE INTO {v["target"]} AS T
USING {v["source"]} AS S
    ON {join_cond}
WHEN MATCHED THEN
    UPDATE SET 
        {updates_set},
        T.ModifiedDate = GETDATE()
WHEN NOT MATCHED BY TARGET THEN
    INSERT ({cols_list}, ModifiedDate)
    VALUES ({s_cols_list}, GETDATE());
```"""

        # 2. Databricks Agent
        elif "databricks" in sys_prompt_lower or "pyspark" in prompt_lower or "spark" in prompt_lower or "scd" in prompt_lower:
            if "scd type 2" in prompt_lower or "scd2" in prompt_lower:
                return f"""### PySpark SCD Type 2 Template (History Tracking)

The PySpark script below dynamically performs an **SCD Type 2 History Merge** from source `{v["source"]}` into Delta target `{v["target"]}` using key columns `{v["keys"]}`.

```python
from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_date, lit, col

spark = SparkSession.builder.appName("SCD_Type2").getOrCreate()

# Target Delta table
target_table = DeltaTable.forPath(spark, "{v["target"]}")

# Incoming Source updates
source_df = spark.read.format("delta").load("{v["source"]}")

# Expire current matching records
expire_cond = "{" AND ".join([f'target.{k} = source.{k}' for k in v["keys"]])} AND target.is_current = true"
target_table.alias("target").merge(
    source_df.alias("source"),
    expire_cond
).whenMatchedUpdate(set={{
    "end_date": "current_date() - 1",
    "is_current": "lit(false)"
}}).execute()

# Insert new active records
new_records = source_df \\
    .withColumn("start_date", current_date()) \\
    .withColumn("end_date", lit(None).cast("date")) \\
    .withColumn("is_current", lit(True))

new_records.write.format("delta").mode("append").save("{v["target"]}")
print("SCD Type 2 Dynamic Merge Completed!")
```"""
            elif "scd type 1" in prompt_lower or "scd1" in prompt_lower:
                set_mapping = ", ".join([f'"{c}": "source.{c}"' for c in v["update_cols"]])
                return f"""### PySpark SCD Type 1 Template (Direct Overwrite)

The PySpark script below dynamically performs an **SCD Type 1 Overwrite Merge** from source `{v["source"]}` into Delta target `{v["target"]}`.

```python
from delta.tables import DeltaTable
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SCD_Type1").getOrCreate()

# Execute Merge Operation
target_table = DeltaTable.forPath(spark, "{v["target"]}")
source_df = spark.read.format("delta").load("{v["source"]}")

join_cond = "{" AND ".join([f'target.{k} = source.{k}' for k in v["keys"] if v["keys"]])}"

target_table.alias("target") \\
    .merge(source_df.alias("source"), join_cond) \\
    .whenMatchedUpdate(set={{{set_mapping}}}) \\
    .whenNotMatchedInsertAll() \\
    .execute()
```"""
            else:
                return f"""### Dynamic Delta Table Optimization Query

Optimize target Delta path `{v["target"]}` to cluster records:

```sql
OPTIMIZE delta.`{v["target"]}`
ZORDER BY ({v["keys"][0] if v["keys"] else "customer_id"});
```

*   **Vacuum command** to delete older transaction files:
```sql
VACUUM delta.`{v["target"]}` RETAIN 168 HOURS;
```"""

        # 3. ADF Agent
        elif "adf" in sys_prompt_lower or "azure data factory" in prompt_lower or "pipeline" in prompt_lower:
            return f"""### Azure Data Factory Watermark Pipeline for {v["target"]}

Dynamic incremental metadata pipeline configuration mapping `{v["source"]}` columns:

```json
{{
  "name": "Incremental_{v["target"].split("/")[-1].split(".")[-1]}",
  "properties": {{
    "activities": [
      {{
        "name": "LookupOldWatermark",
        "type": "Lookup",
        "typeProperties": {{
          "source": {{
            "type": "AzureSqlSource",
            "sqlReaderQuery": "SELECT LastValue FROM dbo.WatermarkTable WHERE TableName = '{v["target"]}'"
          }}
        }}
      }},
      {{
        "name": "LookupNewWatermark",
        "type": "Lookup",
        "typeProperties": {{
          "source": {{
            "type": "AzureSqlSource",
            "sqlReaderQuery": "SELECT MAX({v["update_cols"][-1] if v["update_cols"] else "ModifiedDate"}) FROM {v["source"]}"
          }}
        }}
      }},
      {{
        "name": "CopyIncrementalData",
        "type": "Copy",
        "dependsOn": [
          {{ "activity": "LookupOldWatermark", "dependencyConditions": ["Succeeded"] }},
          {{ "activity": "LookupNewWatermark", "dependencyConditions": ["Succeeded"] }}
        ],
        "typeProperties": {{
          "source": {{
            "type": "AzureSqlSource",
            "sqlReaderQuery": {{
              "value": "SELECT * FROM {v["source"]} WHERE {v["update_cols"][-1] if v["update_cols"] else "ModifiedDate"} > '@{{activity('LookupOldWatermark').output.firstRow.LastValue}}' AND {v["update_cols"][-1] if v["update_cols"] else "ModifiedDate"} <= '@{{activity('LookupNewWatermark').output.firstRow.MaxWatermark}}'",
              "type": "Expression"
            }}
          }},
          "sink": {{ "type": "AzureSqlSink" }}
        }}
      }}
    ]
  }}
}}
```"""

        # 4. Dataverse Agent
        elif "dataverse" in sys_prompt_lower or "dataverse" in prompt_lower or "mapping" in prompt_lower:
            field_mappings_md = ""
            for key in v["keys"]:
                field_mappings_md += f"| `{key}` | `cr234_{key.lower()}` | Single Line of Text (Key) | Primary Key |\n"
            for col in v["update_cols"]:
                field_mappings_md += f"| `{col}` | `cr234_{col.lower()}` | Single Line of Text | Field |\n"

            return f"""### Dynamic Microsoft Dataverse Entity Schema Mappings

#### 📋 Mapping Details for target `{v["target"]}`:

| Source Column | Dataverse Column | Dataverse Type | Logical Name |
| :--- | :--- | :--- | :--- |
{field_mappings_md}

#### 🐍 Python SDK Ingestion script (OData Alternate Keys)
```python
import requests
import json

# alternate key patch url
url = "https://yourorg.crm.dynamics.com/api/data/v9.2/cr234_customers(cr234_id='{v["keys"][0] if v["keys"] else "customer_id"}')"
payload = {{
    "cr234_name": "Dynamic Acme Corp",
    "cr234_status": 841200000
}}

headers = {{
    "Authorization": "Bearer TOKEN_STRING",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "OData-MaxVersion": "4.0",
    "OData-Version": "4.0"
}}

response = requests.patch(url, headers=headers, data=json.dumps(payload))
print("Dataverse PATCH Status:", response.status_code)
```"""

        # 5. Jira Agent
        elif "jira" in sys_prompt_lower or "jira" in prompt_lower or "ticket" in prompt_lower or "issue" in prompt_lower:
            return """### Jira Issue Technical Analysis & Remediation Plan

*   **Identified Workstream**: Core Data Pipeline Migration
*   **Complexity Estimate**: 🟢 Medium (5 Story Points)

#### 🔧 Step-by-Step Remediation Plan

1.  **Step 1: Raw Parser Schema Update**
    Modify `utils/file_parser.py` to allow optional dates and handle blank rows by configuring the pandas engine to ignore trailing empty lines.
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

Here is a structured storyline script designed for C-level presentation.

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
                embedding = data.get("embedding")
                if embedding is None or not isinstance(embedding, list):
                    raise ValueError(f"Ollama returned invalid embedding: {data}")
                embeddings.append(embedding)
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
        if result and result[0] is not None:
            return result[0]
        return []





# ──────────────────────────────────────────────────────────────────────────────
# Unified LLM Service — routes to Ollama / OpenAI / Gemini / Anthropic
# ──────────────────────────────────────────────────────────────────────────────

class UnifiedLLMService:
    """
    Single interface that delegates to the provider selected in the sidebar.
    Falls back to OllamaService simulation if the provider call fails.
    """

    def __init__(self, provider: str, model: str, api_key: str = ""):
        self.provider   = provider   # "ollama" | "openai" | "gemini" | "anthropic"
        self.model      = model
        self.api_key    = api_key
        self._ollama    = OllamaService()   # kept for embeddings + fallback simulation

    # ------------------------------------------------------------------
    def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False,
    ) -> str:
        """Generate a response using the active provider."""
        try:
            if self.provider == "ollama":
                return self._ollama.generate(
                    prompt, system_prompt=system_prompt,
                    temperature=temperature, max_tokens=max_tokens,
                )
            elif self.provider == "openai":
                return self._openai_generate(prompt, system_prompt, temperature, max_tokens)
            elif self.provider == "gemini":
                return self._gemini_generate(prompt, system_prompt, temperature, max_tokens)
            elif self.provider == "anthropic":
                return self._anthropic_generate(prompt, system_prompt, temperature, max_tokens)
            else:
                return self._ollama.generate(prompt, system_prompt=system_prompt)
        except Exception as e:
            logger.error(f"[{self.provider}] generate failed: {e}")
            # Graceful fallback to simulation
            return self._ollama._simulated_generate(prompt, system_prompt)

    # ------------------------------------------------------------------
    def _openai_generate(self, prompt: str, system_prompt: str,
                         temperature: float, max_tokens: int) -> str:
        """Call OpenAI Chat Completions API."""
        try:
            from openai import OpenAI
        except ImportError:
            return "❌ OpenAI package not installed. Run: `pip install openai`"

        if not self.api_key:
            return "❌ No OpenAI API key provided. Enter it in the sidebar or set OPENAI_API_KEY in .env"

        client = OpenAI(api_key=self.api_key)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""

    # ------------------------------------------------------------------
    def _gemini_generate(self, prompt: str, system_prompt: str,
                         temperature: float, max_tokens: int) -> str:
        """Call Google Gemini API."""
        try:
            import google.generativeai as genai
        except ImportError:
            return "❌ Google Generative AI package not installed. Run: `pip install google-generativeai`"

        if not self.api_key:
            return "❌ No Google API key provided. Enter it in the sidebar or set GOOGLE_API_KEY in .env"

        genai.configure(api_key=self.api_key)
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt

        gen_config = genai.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        model = genai.GenerativeModel(model_name=self.model, generation_config=gen_config)
        response = model.generate_content(full_prompt)
        return response.text or ""

    # ------------------------------------------------------------------
    def _anthropic_generate(self, prompt: str, system_prompt: str,
                             temperature: float, max_tokens: int) -> str:
        """Call Anthropic Claude API."""
        try:
            import anthropic
        except ImportError:
            return "❌ Anthropic package not installed. Run: `pip install anthropic`"

        if not self.api_key:
            return "❌ No Anthropic API key provided. Enter it in the sidebar or set ANTHROPIC_API_KEY in .env"

        client = anthropic.Anthropic(api_key=self.api_key)
        kwargs = dict(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        if system_prompt:
            kwargs["system"] = system_prompt

        message = client.messages.create(**kwargs)
        return message.content[0].text if message.content else ""

    # ------------------------------------------------------------------
    # Embeddings always go through Ollama (local)
    def embed(self, texts: List[str]) -> List[List[float]]:
        return self._ollama.embed(texts)

    def embed_single(self, text: str) -> List[float]:
        return self._ollama.embed_single(text)


# ──────────────────────────────────────────────────────────────────────────────
# Factory — reads active provider/model/key from session state each call
# ──────────────────────────────────────────────────────────────────────────────

def get_llm_service() -> UnifiedLLMService:
    """
    Return a UnifiedLLMService configured from st.session_state.
    NOT cached with @st.cache_resource so provider switches take effect immediately.
    """
    provider  = st.session_state.get("ai_provider", "ollama")
    model_cfg = st.session_state.get("model_config", {})

    from config.providers import PROVIDERS
    default_model = PROVIDERS.get(provider, {}).get("default_model", OLLAMA_MODEL)
    model    = model_cfg.get("model", default_model)
    api_key  = st.session_state.get(f"api_key_{provider}", "")

    return UnifiedLLMService(provider=provider, model=model, api_key=api_key)
