# Azure Data Factory (ADF) Blueprint Guide - Part 18

This documentation blueprint details core rules, best practices, and recipes for `Azure Data Factory (ADF)` operations.

### Pattern 52: Pagination rules in Mapping Data Flow Engine
When implementing `Pagination rules` within a `Mapping Data Flow Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement pagination rules on REST API calls utilizing HTTP headers or query parameters.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 53: Activity batching in ADF Copy Activity
When implementing `Activity batching` within a `ADF Copy Activity` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure Self-Hosted Integration Runtime (SHIR) auto-scale groups to manage ingestion bandwidth.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 54: SHIR scalability in Linked Service Core
When implementing `SHIR scalability` within a `Linked Service Core` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Parameterize linked services connection string to point dynamically to database environments.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

