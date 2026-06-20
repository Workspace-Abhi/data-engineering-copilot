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
