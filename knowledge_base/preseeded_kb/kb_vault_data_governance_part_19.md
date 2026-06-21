# Data Governance Blueprint Guide - Part 19

This documentation blueprint details core rules, best practices, and recipes for `Data Governance` operations.

### Pattern 55: GDPR compliance schema in Collibra Catalog Engine
When implementing `GDPR compliance schema` within a `Collibra Catalog Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Establish audit columns (created_by, updated_at, run_id) on all target assets.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 56: CCPA privacy protocols in Apache Atlas Lineage
When implementing `CCPA privacy protocols` within a `Apache Atlas Lineage` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Audit database connection access logs to trace unauthorized query patterns.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 57: Auditing columns in Unity Catalog Governance
When implementing `Auditing columns` within a `Unity Catalog Governance` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use lineage mapping tools to trace data lineage from ingestion raw to golden target.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

