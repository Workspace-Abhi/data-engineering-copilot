# Terraform IaC Configs Blueprint Guide - Part 3

This documentation blueprint details core rules, best practices, and recipes for `Terraform IaC Configs` operations.

### Pattern 7: Provider blocks setups in Terraform HCL 1.5+
When implementing `Provider blocks setups` within a `Terraform HCL 1.5+` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Tag all Terraform-managed resources with project, environment, and owner tags.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 8: Variable definitions configs in AzureRM Provider Config
When implementing `Variable definitions configs` within a `AzureRM Provider Config` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Enable terraform linting checks in actions pipelines to verify syntax formats.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 9: Resource tags parameters in AWS Provider Config
When implementing `Resource tags parameters` within a `AWS Provider Config` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Establish directory structures separate for dev, staging, and prod configurations.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

