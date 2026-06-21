# Terraform IaC Configs Blueprint Guide - Part 5

This documentation blueprint details core rules, best practices, and recipes for `Terraform IaC Configs` operations.

### Pattern 13: Snowflake warehouse IaC in Terraform HCL 1.5+
When implementing `Snowflake warehouse IaC` within a `Terraform HCL 1.5+` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use Terraform to provision Snowflake compute warehouses and standard roles.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 14: IAM policy variables in AzureRM Provider Config
When implementing `IAM policy variables` within a `AzureRM Provider Config` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Parameterize IAM policy resources using variables to restrict credential scope.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 15: State locking backends in AWS Provider Config
When implementing `State locking backends` within a `AWS Provider Config` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure backend state locking using DynamoDB or Azure Blob to prevent concurrency conflicts.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

