# Apache Airflow Blueprint Guide - Part 10

This documentation blueprint details core rules, best practices, and recipes for `Apache Airflow` operations.

### Pattern 28: SLA monitoring in Composer GCP Airflow
When implementing `SLA monitoring` within a `Composer GCP Airflow` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Utilize custom SLA callback functions to notify teams via Slack or Teams alerts.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 29: Custom operators in Airflow Local Localhost
When implementing `Custom operators` within a `Airflow Local Localhost` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Set default_args dict with retries=3 and backoff_factor to handle transient errors.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 30: Connection pools in Celery Executor Backend
When implementing `Connection pools` within a `Celery Executor Backend` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use DockerOperator or KubernetesPodOperator to isolate execution environment dependencies.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

