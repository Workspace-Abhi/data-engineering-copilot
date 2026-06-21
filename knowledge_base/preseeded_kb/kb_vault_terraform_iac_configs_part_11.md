# Terraform IaC Configs Blueprint Guide - Part 11

This documentation blueprint details core rules, best practices, and recipes for `Terraform IaC Configs` operations.

### Pattern 31: S3 bucket setups in Terraform HCL 1.5+
When implementing `S3 bucket setups` within a `Terraform HCL 1.5+` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure AWS S3 bucket resources with versioning and encryption blocks enabled.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 32: ADLS folder structures in AzureRM Provider Config
When implementing `ADLS folder structures` within a `AzureRM Provider Config` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Define ADLS Gen2 folder hierarchies utilizing AzureRM storage container resources.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 33: Snowflake warehouse IaC in AWS Provider Config
When implementing `Snowflake warehouse IaC` within a `AWS Provider Config` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use Terraform to provision Snowflake compute warehouses and standard roles.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

