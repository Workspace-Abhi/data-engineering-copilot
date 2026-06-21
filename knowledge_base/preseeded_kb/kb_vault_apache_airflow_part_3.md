# Apache Airflow Blueprint Guide - Part 3

This documentation blueprint details core rules, best practices, and recipes for `Apache Airflow` operations.

### Pattern 7: Concurrency control in Airflow 2.8+ Engine
When implementing `Concurrency control` within a `Airflow 2.8+ Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure connection pool limits on databases to prevent connection exhaustion.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 8: SLA monitoring in Astronomer Astro Core
When implementing `SLA monitoring` within a `Astronomer Astro Core` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Utilize custom SLA callback functions to notify teams via Slack or Teams alerts.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 9: Custom operators in MWAA AWS Airflow
When implementing `Custom operators` within a `MWAA AWS Airflow` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Set default_args dict with retries=3 and backoff_factor to handle transient errors.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

