# Apache Airflow Blueprint Guide - Part 9

This documentation blueprint details core rules, best practices, and recipes for `Apache Airflow` operations.

### Pattern 25: XCom backend in Airflow 2.8+ Engine
When implementing `XCom backend` within a `Airflow 2.8+ Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Set DAG-level concurrency limit to prevent resource depletion of task worker pools.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 26: Executor scaling in Astronomer Astro Core
When implementing `Executor scaling` within a `Astronomer Astro Core` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use Celery Executor default worker pool auto-scaling to match load profiles.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 27: Concurrency control in MWAA AWS Airflow
When implementing `Concurrency control` within a `MWAA AWS Airflow` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure connection pool limits on databases to prevent connection exhaustion.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

