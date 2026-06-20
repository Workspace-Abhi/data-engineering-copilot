"""Agents module."""
from agents.router import AgentRouter, get_router
from agents.sql_agent import SQLAgent, get_sql_agent
from agents.databricks_agent import DatabricksAgent, get_databricks_agent
from agents.adf_agent import ADFAgent, get_adf_agent
from agents.dataverse_agent import DataverseAgent, get_dataverse_agent
from agents.jira_agent import JiraAgent, get_jira_agent
from agents.meeting_agent import MeetingAgent, get_meeting_agent
from agents.ppt_agent import PPTAgent, get_ppt_agent

# Advanced Data Agents (Batch 3)
from agents.data_quality_agent import DataQualityAgent, get_data_quality_agent
from agents.dbt_agent import DbtAgent, get_dbt_agent
from agents.airflow_agent import AirflowAgent, get_airflow_agent
from agents.terraform_iac_agent import TerraformIaCAgent, get_terraform_iac_agent
from agents.data_governance_agent import DataGovernanceAgent, get_data_governance_agent
from agents.cost_optimization_agent import CostOptimizationAgent, get_cost_optimization_agent
from agents.data_migration_agent import DataMigrationAgent, get_data_migration_agent
from agents.observability_agent import ObservabilityAgent, get_observability_agent

# Specialized Agents (Batch 4)
from agents.data_catalog_agent import DataCatalogAgent, get_data_catalog_agent
from agents.testing_agent import TestingAgent, get_testing_agent
from agents.code_review_agent import CodeReviewAgent, get_code_review_agent
from agents.api_integration_agent import ApiIntegrationAgent, get_api_integration_agent
from agents.streaming_agent import StreamingAgent, get_streaming_agent
from agents.mlops_data_agent import MLOpsDataAgent, get_mlops_data_agent

__all__ = [
    "AgentRouter", "get_router",
    "SQLAgent", "get_sql_agent",
    "DatabricksAgent", "get_databricks_agent",
    "ADFAgent", "get_adf_agent",
    "DataverseAgent", "get_dataverse_agent",
    "JiraAgent", "get_jira_agent",
    "MeetingAgent", "get_meeting_agent",
    "PPTAgent", "get_ppt_agent",
    
    # Advanced Data Agents
    "DataQualityAgent", "get_data_quality_agent",
    "DbtAgent", "get_dbt_agent",
    "AirflowAgent", "get_airflow_agent",
    "TerraformIaCAgent", "get_terraform_iac_agent",
    "DataGovernanceAgent", "get_data_governance_agent",
    "CostOptimizationAgent", "get_cost_optimization_agent",
    "DataMigrationAgent", "get_data_migration_agent",
    "ObservabilityAgent", "get_observability_agent",

    # Specialized Agents
    "DataCatalogAgent", "get_data_catalog_agent",
    "TestingAgent", "get_testing_agent",
    "CodeReviewAgent", "get_code_review_agent",
    "ApiIntegrationAgent", "get_api_integration_agent",
    "StreamingAgent", "get_streaming_agent",
    "MLOpsDataAgent", "get_mlops_data_agent"
]
