# dbt (Data Build Tool) Blueprint Guide - Part 4

This documentation blueprint details core rules, best practices, and recipes for `dbt (Data Build Tool)` operations.

### Pattern 10: Source declarations in dbt-Databricks adapter
When implementing `Source declarations` within a `dbt-Databricks adapter` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use run_results.json logs to analyze query execution bottlenecks in staging.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 11: Staging configurations in dbt-BigQuery adapter
When implementing `Staging configurations` within a `dbt-BigQuery adapter` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure incremental models using merge strategy on Snowflake and Databricks platforms.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 12: Incremental strategies in dbt-Postgres adapter
When implementing `Incremental strategies` within a `dbt-Postgres adapter` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Write custom schema validation tests inside schema.yml files to verify business keys.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

