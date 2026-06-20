"""UI module."""
from ui.sidebar import render_sidebar
from ui.chat_tab import render_chat_tab
from ui.sql_tab import render_sql_tab
from ui.databricks_tab import render_databricks_tab
from ui.adf_tab import render_adf_tab
from ui.dataverse_tab import render_dataverse_tab
from ui.jira_tab import render_jira_tab
from ui.meeting_tab import render_meeting_tab
from ui.ppt_tab import render_ppt_tab
from ui.kb_tab import render_kb_tab

# New Advanced/Specialized Tabs
from ui.data_quality_tab import render_data_quality_tab
from ui.dbt_tab import render_dbt_tab
from ui.airflow_tab import render_airflow_tab
from ui.terraform_tab import render_terraform_tab
from ui.governance_tab import render_governance_tab
from ui.cost_tab import render_cost_tab
from ui.migration_tab import render_migration_tab
from ui.observability_tab import render_observability_tab
from ui.catalog_tab import render_catalog_tab
from ui.testing_tab import render_testing_tab
from ui.code_review_tab import render_code_review_tab
from ui.streaming_tab import render_streaming_tab
from ui.mlops_tab import render_mlops_tab

__all__ = [
    "render_sidebar",
    "render_chat_tab",
    "render_sql_tab",
    "render_databricks_tab",
    "render_adf_tab",
    "render_dataverse_tab",
    "render_jira_tab",
    "render_meeting_tab",
    "render_ppt_tab",
    "render_kb_tab",
    
    # Advanced Data Agent Tabs
    "render_data_quality_tab",
    "render_dbt_tab",
    "render_airflow_tab",
    "render_terraform_tab",
    "render_governance_tab",
    "render_cost_tab",
    "render_migration_tab",
    "render_observability_tab",
    "render_catalog_tab",
    "render_testing_tab",
    "render_code_review_tab",
    "render_streaming_tab",
    "render_mlops_tab"
]
