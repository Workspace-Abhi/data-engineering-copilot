# Terraform IaC Configs Blueprint Guide - Part 7

This documentation blueprint details core rules, best practices, and recipes for `Terraform IaC Configs` operations.

### Pattern 19: Resource tags parameters in Terraform HCL 1.5+
When implementing `Resource tags parameters` within a `Terraform HCL 1.5+` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Establish directory structures separate for dev, staging, and prod configurations.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 20: Lifecycle policies IaC in AzureRM Provider Config
When implementing `Lifecycle policies IaC` within a `AzureRM Provider Config` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure lifecycle policy rules inside Terraform to prevent accidental resource deletes.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 21: S3 bucket setups in AWS Provider Config
When implementing `S3 bucket setups` within a `AWS Provider Config` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure AWS S3 bucket resources with versioning and encryption blocks enabled.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

