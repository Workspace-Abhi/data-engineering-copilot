# Azure Data Factory (ADF) Blueprint Guide - Part 5

This documentation blueprint details core rules, best practices, and recipes for `Azure Data Factory (ADF)` operations.

### Pattern 13: Activity batching in ADF Pipeline V2
When implementing `Activity batching` within a `ADF Pipeline V2` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure Self-Hosted Integration Runtime (SHIR) auto-scale groups to manage ingestion bandwidth.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 14: SHIR scalability in Synapse Pipeline Engine
When implementing `SHIR scalability` within a `Synapse Pipeline Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Parameterize linked services connection string to point dynamically to database environments.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 15: Retry triggers in Azure Data Factory SHIR
When implementing `Retry triggers` within a `Azure Data Factory SHIR` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Set secure input/output check flags to conceal API keys or secrets in logs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

