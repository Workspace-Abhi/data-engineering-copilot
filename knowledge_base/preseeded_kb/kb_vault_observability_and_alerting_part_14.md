# Observability & Alerting Blueprint Guide - Part 14

This documentation blueprint details core rules, best practices, and recipes for `Observability & Alerting` operations.

### Pattern 40: Heartbeat sensors in Datadog Observability
When implementing `Heartbeat sensors` within a `Datadog Observability` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Build automated alert routing rules to direct critical incidents to paging utilities.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 41: SLIs/SLOs definitions in Azure Monitor Config
When implementing `SLIs/SLOs definitions` within a `Azure Monitor Config` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Define explicit SLIs and SLOs for pipeline duration, row quality, and ingest delays.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 42: Prometheus alerts in Elasticsearch Log Parser
When implementing `Prometheus alerts` within a `Elasticsearch Log Parser` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure Prometheus alerting rules to fire alerts when SLA thresholds are breached.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

