"""Terraform IaC Agent for generating AWS, Azure, and GCP data infrastructure."""
from typing import Dict, List, Optional
from config.logging_config import get_logger
from services.llm_service import get_llm_service
from services.rag_service import get_rag_service

logger = get_logger("terraform_iac_agent")

class TerraformIaCAgent:
    """Specialized agent for Terraform Infrastructure-as-Code tasks."""

    SYSTEM_PROMPT = """You are an expert Cloud and Data Infrastructure Architect. You specialize in:
- Writing Terraform configs for AWS (S3, Redshift, EMR, Athena, RDS, MSK)
- Writing Terraform configs for Azure (ADLS Gen2, Databricks, ADF, Synapse, SQL DB)
- Writing Terraform configs for GCP (GCS, BigQuery, Dataproc, Dataflow, Pub/Sub)
- Implementing security best practices (IAM, KMS encryption, private endpoints)
- Structuring modular, dry Terraform code with variables and outputs

Always provide production-ready Terraform (.tf) code with comments explaining resource configurations."""

    def __init__(self):
        self.llm_service = get_llm_service()
        self.rag_service = get_rag_service()

    def process(self, query: str, context: str = "") -> str:
        """Process a Terraform-related query."""
        rag_context = self.rag_service.get_context(query, k=3)
        full_prompt = f"""{self.SYSTEM_PROMPT}

Context from knowledge base:
{rag_context}

User Query: {query}

Additional Context: {context}

Provide a comprehensive response with Terraform configurations where applicable."""

        return self.llm_service.generate(
            full_prompt,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3
        )

    def generate_azure_infra(self, resource_group: str, location: str = "East US", storage_account_name: str = "adlsstorage") -> str:
        """Generate Azure ADLS Gen2 storage resource config."""
        tf_code = f"""# Azure Provider Configuration
provider "azurerm" {{
  features {{}}
}}

# Resource Group
resource "azurerm_resource_group" "rg" {{
  name     = "{resource_group}"
  location = "{location}"
}}

# Storage Account configured for ADLS Gen2 (hierarchical namespace enabled)
resource "azurerm_storage_account" "storage" {{
  name                     = "{storage_account_name}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  is_hns_enabled           = true

  tags = {{
    Environment = "production"
    Department  = "data_engineering"
  }}
}}

# File System (Container) for Lakehouse Bronze zone
resource "azurerm_storage_data_lake_gen2_filesystem" "bronze" {{
  name               = "bronze"
  storage_account_id = azurerm_storage_account.storage.id
}}
"""
        return tf_code

    def generate_aws_infra(self, bucket_name: str) -> str:
        """Generate AWS S3 bucket resources for data lake."""
        tf_code = f"""provider "aws" {{
  region = "us-east-1"
}}

# S3 Bucket for Data Lake raw landing
resource "aws_s3_bucket" "datalake_raw" {{
  bucket = "{bucket_name}"

  tags = {{
    Name        = "Datalake Raw Bucket"
    Environment = "Production"
  }}
}}

# Block Public Access
resource "aws_s3_bucket_public_access_block" "block_public" {{
  bucket = aws_s3_bucket.datalake_raw.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}}

# Enable server-side encryption by default
resource "aws_s3_bucket_server_side_encryption_configuration" "sse" {{
  bucket = aws_s3_bucket.datalake_raw.id

  rule {{
    apply_server_side_encryption_by_default {{
      sse_algorithm = "AES256"
    }}
  }}
}}
"""
        return tf_code

    def generate_gcp_infra(self, project_id: str, bucket_name: str) -> str:
        """Generate GCP GCS bucket resources."""
        tf_code = f"""provider "google" {{
  project = "{project_id}"
  region  = "us-central1"
}}

# GCS Bucket for Raw Datasets
resource "google_storage_bucket" "gcs_raw" {{
  name          = "{bucket_name}"
  location      = "US"
  force_destroy = false

  uniform_bucket_level_access = true

  versioning {{
    enabled = true
  }}
}}
"""
        return tf_code


def get_terraform_iac_agent() -> TerraformIaCAgent:
    """Get Terraform IaC agent instance."""
    return TerraformIaCAgent()
