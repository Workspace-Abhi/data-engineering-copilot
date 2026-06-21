# dbt (Data Build Tool) Blueprint Guide - Part 7

This documentation blueprint details core rules, best practices, and recipes for `dbt (Data Build Tool)` operations.

### Pattern 19: Semantic metrics in dbt Core Engine
When implementing `Semantic metrics` within a `dbt Core Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Leverage dbt project mesh to establish inter-project model dependencies.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 20: Source declarations in dbt Cloud Service
When implementing `Source declarations` within a `dbt Cloud Service` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use run_results.json logs to analyze query execution bottlenecks in staging.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 21: Staging configurations in dbt-Snowflake adapter
When implementing `Staging configurations` within a `dbt-Snowflake adapter` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure incremental models using merge strategy on Snowflake and Databricks platforms.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

