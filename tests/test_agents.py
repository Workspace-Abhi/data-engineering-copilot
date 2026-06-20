"""Unit tests for router and SQL agent."""
import pytest
from unittest.mock import Mock, patch

from agents.router import AgentRouter
from agents.sql_agent import SQLAgent


class TestAgentRouter:
    """Test cases for AgentRouter."""

    def test_route_sql_keywords(self):
        """Test routing with SQL keywords."""
        router = AgentRouter()
        router.llm_service = Mock()

        agent, confidence = router.route("How do I write a MERGE statement?")
        assert agent == "sql"
        assert confidence > 0

    def test_route_databricks_keywords(self):
        """Test routing with Databricks keywords."""
        router = AgentRouter()
        router.llm_service = Mock()

        agent, confidence = router.route("How to optimize a Delta table?")
        assert agent == "databricks"

    def test_route_adf_keywords(self):
        """Test routing with ADF keywords."""
        router = AgentRouter()
        router.llm_service = Mock()

        agent, confidence = router.route("Design an ADF pipeline with watermark")
        assert agent == "adf"

    def test_route_low_confidence_uses_llm(self):
        """Test LLM fallback for ambiguous queries."""
        router = AgentRouter()
        router.llm_service = Mock()
        router.llm_service.generate.return_value = "sql"

        agent, confidence = router.route("hello world")
        router.llm_service.generate.assert_called_once()
        assert agent == "sql"


class TestSQLAgent:
    """Test cases for SQLAgent."""

    def test_generate_merge(self):
        """Test MERGE statement generation."""
        agent = SQLAgent()
        agent.llm_service = Mock()

        sql = agent.generate_merge(
            "staging.Customers",
            "dbo.Customers", 
            ["CustomerID"],
            ["Name", "Email"]
        )

        assert "MERGE INTO" in sql
        assert "staging.Customers" in sql
        assert "dbo.Customers" in sql
        assert "WHEN MATCHED" in sql
        assert "WHEN NOT MATCHED" in sql

    def test_generate_cdc(self):
        """Test CDC SQL generation."""
        agent = SQLAgent()
        agent.llm_service = Mock()

        sql = agent.generate_cdc("Orders", "OrderID")

        assert "sp_cdc_enable_db" in sql
        assert "sp_cdc_enable_table" in sql
        assert "cdc.dbo_Orders_CT" in sql

    def test_reconcile_data(self):
        """Test reconciliation query generation."""
        agent = SQLAgent()
        agent.llm_service = Mock()

        sql = agent.reconcile_data(
            "SELECT * FROM Source",
            "SELECT * FROM Target",
            ["ID"]
        )

        assert "SourceCount" in sql
        assert "TargetCount" in sql
        assert "MissingInTarget" in sql
        assert "MissingInSource" in sql


class TestDatabricksAgent:
    """Test cases for DatabricksAgent."""

    def test_generate_scd_type1(self):
        """Test SCD Type 1 PySpark code generation."""
        from agents.databricks_agent import DatabricksAgent
        agent = DatabricksAgent()
        code = agent.generate_scd_type1("customers", ["customer_id"], ["name", "email"])
        assert "merge" in code
        assert "whenMatchedUpdate" in code
        assert "SCD_Type1" in code

    def test_generate_scd_type2(self):
        """Test SCD Type 2 PySpark code generation."""
        from agents.databricks_agent import DatabricksAgent
        agent = DatabricksAgent()
        code = agent.generate_scd_type2("customers", ["customer_id"], ["name", "email"])
        assert "merge" in code
        assert "whenMatchedUpdate" in code
        assert "append" in code
        assert "SCD_Type2" in code

    def test_optimize_delta_table(self):
        """Test delta optimization SQL query generation."""
        from agents.databricks_agent import DatabricksAgent
        agent = DatabricksAgent()
        code = agent.optimize_delta_table("/path/to/customers", ["customer_id"])
        assert "OPTIMIZE" in code
        assert "VACUUM" in code
        assert "ZORDER BY" in code


class TestADFAgent:
    """Test cases for ADFAgent."""

    def test_generate_watermark_pipeline(self):
        """Test watermark pipeline JSON generation."""
        from agents.adf_agent import ADFAgent
        agent = ADFAgent()
        pipeline = agent.generate_watermark_pipeline("SourceTable", "TargetTable")
        assert pipeline["name"] == "IncrementalLoad_SourceTable"
        assert len(pipeline["properties"]["activities"]) == 2
        assert pipeline["properties"]["activities"][0]["name"] == "LookupWatermark"
        assert pipeline["properties"]["activities"][1]["name"] == "CopyIncrementalData"

    def test_generate_expression(self):
        """Test ADF expression generation."""
        from agents.adf_agent import ADFAgent
        agent = ADFAgent()
        expr = agent.generate_expression("current_date")
        assert expr == "@utcnow()"


class TestDataverseAgent:
    """Test cases for DataverseAgent."""

    def test_map_sql_to_dataverse(self):
        """Test mapping SQL table schemas to Dataverse entities."""
        from agents.dataverse_agent import DataverseAgent
        agent = DataverseAgent()
        sql_table = {
            "name": "customers",
            "columns": [
                {"name": "id", "type": "int", "nullable": False},
                {"name": "name", "type": "varchar(100)", "nullable": True}
            ]
        }
        entity = agent.map_sql_to_dataverse(sql_table)
        assert entity["name"] == "customers"
        assert len(entity["fields"]) == 2
        assert entity["fields"][0]["data_type"] == "Whole Number"
        assert entity["fields"][1]["data_type"] == "Single Line of Text"

    def test_generate_ingestion_flow(self):
        """Test M code flow generation for Dataverse."""
        from agents.dataverse_agent import DataverseAgent
        agent = DataverseAgent()
        flow = agent.generate_ingestion_flow("Source", "Target", {"src_col": "tgt_col"})
        assert "RenameColumns" in flow
        assert "LoadToDataverse" in flow


class TestJiraAgent:
    """Test cases for JiraAgent."""

    def test_group_by_theme_no_summary(self):
        """Test group_by_theme fails when Summary column is missing."""
        import pandas as pd
        from agents.jira_agent import JiraAgent
        agent = JiraAgent()
        df = pd.DataFrame({"id": [1, 2]})
        res = agent.group_by_theme(df)
        assert "error" in res


class TestMeetingAgent:
    """Test cases for MeetingAgent."""

    @patch("services.llm_service.OllamaService.generate")
    def test_extract_action_items_parsed(self, mock_generate):
        """Test extract_action_items successfully parses JSON array output."""
        mock_generate.return_value = '[{"description": "Fix login", "owner": "Abhi", "deadline": "2026-06-25", "priority": "High"}]'
        from agents.meeting_agent import MeetingAgent
        agent = MeetingAgent()
        items = agent.extract_action_items("some transcript")
        assert len(items) == 1
        assert items[0]["description"] == "Fix login"
        assert items[0]["owner"] == "Abhi"


class TestPPTAgent:
    """Test cases for PPTAgent."""

    @patch("services.llm_service.OllamaService.generate")
    def test_create_storyline(self, mock_generate):
        """Test create_storyline returns correct dict schema."""
        mock_generate.return_value = "Compelling Storyline"
        from agents.ppt_agent import PPTAgent
        agent = PPTAgent()
        res = agent.create_storyline("Legacy Migration", "executives", ["points"])
        assert res["topic"] == "Legacy Migration"
        assert res["audience"] == "executives"
        assert res["storyline"] == "Compelling Storyline"


class TestDataQualityAgent:
    """Test cases for DataQualityAgent."""

    def test_generate_great_expectations_suite(self):
        """Test GE suite generation."""
        from agents.data_quality_agent import DataQualityAgent
        agent = DataQualityAgent()
        cols = [{"name": "id", "type": "int", "nullable": False}]
        suite = agent.generate_great_expectations_suite("my_table", cols)
        assert "my_table_suite" in suite
        assert "expect_column_values_to_not_be_null" in suite

    def test_generate_soda_checks(self):
        """Test Soda checks generation."""
        from agents.data_quality_agent import DataQualityAgent
        agent = DataQualityAgent()
        cols = [{"name": "id", "type": "int", "nullable": False}]
        checks = agent.generate_soda_checks("my_table", cols)
        assert "checks for my_table:" in checks
        assert "missing_count(id)" in checks


class TestDbtAgent:
    """Test cases for DbtAgent."""

    def test_generate_model(self):
        """Test dbt model generation."""
        from agents.dbt_agent import DbtAgent
        agent = DbtAgent()
        model = agent.generate_model("stg_customers", "raw_customers", ["id", "name"])
        assert "source('raw', 'raw_customers')" in model
        assert "stg_customers" not in model # just target table input

    def test_generate_schema_yml(self):
        """Test dbt schema.yml generation."""
        from agents.dbt_agent import DbtAgent
        agent = DbtAgent()
        cols = [{"name": "id", "nullable": False, "unique": True}]
        yml = agent.generate_schema_yml("my_model", cols)
        assert "name: my_model" in yml
        assert "not_null" in yml
        assert "unique" in yml


class TestAirflowAgent:
    """Test cases for AirflowAgent."""

    def test_generate_dag(self):
        """Test Airflow DAG generation."""
        from agents.airflow_agent import AirflowAgent
        agent = AirflowAgent()
        dag_code = agent.generate_dag("my_dag")
        assert "DAG(" in dag_code
        assert "'my_dag'" in dag_code

    def test_generate_dag_with_sensor(self):
        """Test Airflow DAG with sensor generation."""
        from agents.airflow_agent import AirflowAgent
        agent = AirflowAgent()
        dag_code = agent.generate_dag_with_sensor("my_dag_sensor", "my_sensor")
        assert "FileSensor(" in dag_code
        assert "task_id='my_sensor'" in dag_code


class TestTerraformIaCAgent:
    """Test cases for TerraformIaCAgent."""

    def test_generate_azure_infra(self):
        """Test Azure Terraform generation."""
        from agents.terraform_iac_agent import TerraformIaCAgent
        agent = TerraformIaCAgent()
        tf = agent.generate_azure_infra("my_rg", "West US", "mystorage")
        assert "azurerm_resource_group" in tf
        assert "mystorage" in tf
        assert "West US" in tf

    def test_generate_aws_infra(self):
        """Test AWS Terraform generation."""
        from agents.terraform_iac_agent import TerraformIaCAgent
        agent = TerraformIaCAgent()
        tf = agent.generate_aws_infra("my-bucket")
        assert "aws_s3_bucket" in tf
        assert "my-bucket" in tf


class TestDataGovernanceAgent:
    """Test cases for DataGovernanceAgent."""

    def test_generate_rbac_policy(self):
        """Test RBAC policy generation."""
        from agents.data_governance_agent import DataGovernanceAgent
        agent = DataGovernanceAgent()
        rbac = agent.generate_rbac_policy(["data_analyst"], ["customers"])
        assert "data_analyst" in rbac
        assert "customers" in rbac

    def test_generate_pii_detection_rules(self):
        """Test PII detection rules mapping."""
        from agents.data_governance_agent import DataGovernanceAgent
        agent = DataGovernanceAgent()
        pii = agent.generate_pii_detection_rules(["email", "id"])
        assert "PII" in pii
        assert "Non-PII" in pii


class TestCostOptimizationAgent:
    """Test cases for CostOptimizationAgent."""

    def test_suggest_cluster_sizing(self):
        """Test cluster sizing recommendations."""
        from agents.cost_optimization_agent import CostOptimizationAgent
        agent = CostOptimizationAgent()
        res = agent.suggest_cluster_sizing("ETL", 600)
        assert res["suggested_vm"] == "Standard_E16ds_v4"
        assert res["worker_count"] == 8
        assert res["autoscale"] is True

    def test_suggest_storage_tiering(self):
        """Test storage tiering config generation."""
        from agents.cost_optimization_agent import CostOptimizationAgent
        agent = CostOptimizationAgent()
        tiering = agent.suggest_storage_tiering(90)
        assert "90" in tiering


class TestDataMigrationAgent:
    """Test cases for DataMigrationAgent."""

    def test_generate_migration_assessment(self):
        """Test migration assessment report generation."""
        from agents.data_migration_agent import DataMigrationAgent
        agent = DataMigrationAgent()
        res = agent.generate_migration_assessment("Oracle", "Snowflake", 15)
        assert "Oracle" in res
        assert "Snowflake" in res
        assert "15" in res

    def test_generate_rollback_plan(self):
        """Test rollback plan generation."""
        from agents.data_migration_agent import DataMigrationAgent
        agent = DataMigrationAgent()
        res = agent.generate_rollback_plan("MIG_001")
        assert "MIG_001" in res


class TestObservabilityAgent:
    """Test cases for ObservabilityAgent."""

    def test_generate_sli_slo_definitions(self):
        """Test SLI/SLO markdown table generation."""
        from agents.observability_agent import ObservabilityAgent
        agent = ObservabilityAgent()
        res = agent.generate_sli_slo_definitions("MyPipeline")
        assert "MyPipeline" in res
        assert "Freshness" in res

    def test_generate_alert_rules(self):
        """Test Alert manager YAML generation."""
        from agents.observability_agent import ObservabilityAgent
        agent = ObservabilityAgent()
        res = agent.generate_alert_rules()
        assert "IngestionPipelineFailed" in res


class TestDataCatalogAgent:
    """Test cases for DataCatalogAgent."""

    def test_generate_data_dictionary(self):
        """Test data dictionary generation."""
        from agents.data_catalog_agent import DataCatalogAgent
        agent = DataCatalogAgent()
        cols = [{"name": "id", "type": "int", "is_key": True, "nullable": False}]
        res = agent.generate_data_dictionary("my_table", cols)
        assert "my_table" in res
        assert "`id`" in res

    def test_generate_lineage_definition(self):
        """Test lineage Mermaid definition generation."""
        from agents.data_catalog_agent import DataCatalogAgent
        agent = DataCatalogAgent()
        res = agent.generate_lineage_definition(["src1", "src2"], "tgt")
        assert "src1" in res
        assert "tgt" in res

class TestTestingAgent:
    """Test cases for TestingAgent."""

    def test_generate_sql_unit_test(self):
        """Test SQL unit test assertion block generation."""
        from agents.testing_agent import TestingAgent
        agent = TestingAgent()
        res = agent.generate_sql_unit_test("test1", "SELECT 1", "SELECT 2")
        assert "Expected" in res
        assert "Actual" in res

    def test_generate_mock_data(self):
        """Test mock data insert SQL generation."""
        from agents.testing_agent import TestingAgent
        agent = TestingAgent()
        cols = [{"name": "id", "type": "int"}, {"name": "email", "type": "varchar"}]
        res = agent.generate_mock_data(cols, 3)
        assert "INSERT INTO" in res
        assert "user1@example.com" in res


class TestCodeReviewAgent:
    """Test cases for CodeReviewAgent."""

    def test_review_code_snippet_sql(self):
        """Test sql code review finds select * warning."""
        from agents.code_review_agent import CodeReviewAgent
        agent = CodeReviewAgent()
        res = agent.review_code_snippet("SELECT * FROM customers", "sql")
        assert len(res["findings"]) == 1
        assert res["findings"][0]["severity"] == "Warning"

    def test_review_code_snippet_python(self):
        """Test python code review finds secret warning."""
        from agents.code_review_agent import CodeReviewAgent
        agent = CodeReviewAgent()
        res = agent.review_code_snippet("password = '123'", "python")
        assert len(res["findings"]) == 1
        assert res["findings"][0]["severity"] == "Critical"


class TestApiIntegrationAgent:
    """Test cases for ApiIntegrationAgent."""

    def test_generate_rest_ingestion(self):
        """Test rest ingestion python script generation."""
        from agents.api_integration_agent import ApiIntegrationAgent
        agent = ApiIntegrationAgent()
        res = agent.generate_rest_ingestion("http://api.com")
        assert "fetch_paginated_data" in res
        assert "http://api.com" in res

    def test_generate_webhook_handler(self):
        """Test FastAPI webhook receiver template generation."""
        from agents.api_integration_agent import ApiIntegrationAgent
        agent = ApiIntegrationAgent()
        res = agent.generate_webhook_handler()
        assert "FastAPI" in res
        assert "receive_webhook" in res


class TestStreamingAgent:
    """Test cases for StreamingAgent."""

    def test_generate_spark_streaming_window(self):
        """Test Spark streaming window code generation."""
        from agents.streaming_agent import StreamingAgent
        agent = StreamingAgent()
        res = agent.generate_spark_streaming_window("my_topic")
        assert "readStream" in res
        assert "my_topic" in res

    def test_generate_flink_sql_window(self):
        """Test Flink windowing SQL query generation."""
        from agents.streaming_agent import StreamingAgent
        agent = StreamingAgent()
        res = agent.generate_flink_sql_window()
        assert "sensor_readings" in res
        assert "TUMBLE" in res


class TestMLOpsDataAgent:
    """Test cases for MLOpsDataAgent."""

    def test_generate_feast_definition(self):
        """Test Feast feature store definition generation."""
        from agents.mlops_data_agent import MLOpsDataAgent
        agent = MLOpsDataAgent()
        res = agent.generate_feast_definition()
        assert "FeatureView" in res
        assert "Entity" in res

    def test_generate_drift_detection_check(self):
        """Test drift detection function template generation."""
        from agents.mlops_data_agent import MLOpsDataAgent
        agent = MLOpsDataAgent()
        res = agent.generate_drift_detection_check()
        assert "detect_drift_kolmogorov_smirnov" in res




