"""Data Governance Agent for RBAC policy, PII detection rules, and compliance reports."""
from typing import Dict, List, Optional
import json
from config.logging_config import get_logger
from services.llm_service import get_llm_service
from services.rag_service import get_rag_service

logger = get_logger("data_governance_agent")

class DataGovernanceAgent:
    """Specialized agent for data governance, RBAC, PII, and security rules."""

    SYSTEM_PROMPT = """You are an expert Data Governance and Compliance Officer. You specialize in:
- Identifying and masking Personally Identifiable Information (PII)
- Creating Role-Based Access Control (RBAC) and row/column security policies
- Designing data catalog and lineage structures
- Writing audit, data retention, and GDPR/CCPA compliance configurations
- Configuring access controls for databases (SQL, Snowflake, Databricks)

Always provide structured JSON policies, SQL grants, or masking configs."""

    def __init__(self):
        self.llm_service = get_llm_service()
        self.rag_service = get_rag_service()

    def process(self, query: str, context: str = "") -> str:
        """Process a governance-related query."""
        rag_context = self.rag_service.get_context(query, k=3)
        full_prompt = f"""{self.SYSTEM_PROMPT}

Context from knowledge base:
{rag_context}

User Query: {query}

Additional Context: {context}

Provide a comprehensive response with compliance or security configuration examples where applicable."""

        return self.llm_service.generate(
            full_prompt,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3
        )

    def generate_rbac_policy(self, roles: List[str], resources: List[str]) -> str:
        """Generate structured RBAC role and privilege mapping JSON."""
        rbac = {
            "rbac_policy_version": "1.0",
            "roles": {}
        }

        for role in roles:
            privileges = []
            for res in resources:
                privileges.append({
                    "resource": res,
                    "actions": ["SELECT", "READ"] if "analyst" in role.lower() else ["SELECT", "INSERT", "UPDATE", "DELETE", "ALL"]
                })
            rbac["roles"][role] = {
                "privileges": privileges,
                "row_filters": [
                    {
                        "target_table": resources[0] if resources else "all",
                        "filter_clause": "region = CURRENT_USER_REGION()"
                    }
                ] if "analyst" in role.lower() else []
            }

        return json.dumps(rbac, indent=2)

    def generate_pii_detection_rules(self, columns: List[str]) -> str:
        """Generate a dictionary structure mapping potential PII columns to masking actions."""
        pii_rules = {}
        pii_keywords = ["email", "phone", "ssn", "social_security", "salary", "card", "credit_card", "password", "address"]

        for col in columns:
            col_lower = col.lower()
            matched = False
            for kw in pii_keywords:
                if kw in col_lower:
                    matched = True
                    break
            
            if matched:
                if "email" in col_lower:
                    masking_type = "regexp_replace(email, '(?i)([^@]{1,3})[^@]+@([^@]+)', '\\\\1***@\\\\2')"
                elif "phone" in col_lower:
                    masking_type = "mask_last_n(phone_number, 4)"
                else:
                    masking_type = "hash_sha256()"
                pii_rules[col] = {
                    "classification": "PII",
                    "sensitivity": "High",
                    "masking_rule": masking_type
                }
            else:
                pii_rules[col] = {
                    "classification": "Non-PII",
                    "sensitivity": "Low",
                    "masking_rule": "none"
                }

        return json.dumps(pii_rules, indent=2)


def get_data_governance_agent() -> DataGovernanceAgent:
    """Get Data Governance agent instance."""
    return DataGovernanceAgent()
