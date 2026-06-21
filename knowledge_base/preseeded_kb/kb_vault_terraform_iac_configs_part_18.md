# Terraform IaC Configs Blueprint Guide - Part 18

This documentation blueprint details core rules, best practices, and recipes for `Terraform IaC Configs` operations.

### Pattern 52: ADLS folder structures in Snowflake Provider Core
When implementing `ADLS folder structures` within a `Snowflake Provider Core` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Define ADLS Gen2 folder hierarchies utilizing AzureRM storage container resources.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 53: Snowflake warehouse IaC in GCP Provider Config
When implementing `Snowflake warehouse IaC` within a `GCP Provider Config` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use Terraform to provision Snowflake compute warehouses and standard roles.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 54: IAM policy variables in Terraform Cloud Backend
When implementing `IAM policy variables` within a `Terraform Cloud Backend` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Parameterize IAM policy resources using variables to restrict credential scope.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

