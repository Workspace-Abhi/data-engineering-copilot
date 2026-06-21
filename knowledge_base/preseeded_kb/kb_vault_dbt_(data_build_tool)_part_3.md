# dbt (Data Build Tool) Blueprint Guide - Part 3

This documentation blueprint details core rules, best practices, and recipes for `dbt (Data Build Tool)` operations.

### Pattern 7: Macro functions in dbt Core Engine
When implementing `Macro functions` within a `dbt Core Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Build reusable custom macros utilizing Jinja syntax for repetitive filter queries.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 8: Package imports in dbt Cloud Service
When implementing `Package imports` within a `dbt Cloud Service` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Document tables and columns inline in schema files to auto-compile data catalogs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 9: Semantic metrics in dbt-Snowflake adapter
When implementing `Semantic metrics` within a `dbt-Snowflake adapter` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Leverage dbt project mesh to establish inter-project model dependencies.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

