# dbt (Data Build Tool) Blueprint Guide - Part 20

This documentation blueprint details core rules, best practices, and recipes for `dbt (Data Build Tool)` operations.

### Pattern 58: Package imports in dbt-Databricks adapter
When implementing `Package imports` within a `dbt-Databricks adapter` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Document tables and columns inline in schema files to auto-compile data catalogs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 59: Semantic metrics in dbt-BigQuery adapter
When implementing `Semantic metrics` within a `dbt-BigQuery adapter` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Leverage dbt project mesh to establish inter-project model dependencies.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 60: Source declarations in dbt-Postgres adapter
When implementing `Source declarations` within a `dbt-Postgres adapter` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use run_results.json logs to analyze query execution bottlenecks in staging.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

