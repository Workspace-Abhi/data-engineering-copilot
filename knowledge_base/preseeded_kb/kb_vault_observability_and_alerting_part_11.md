# Observability & Alerting Blueprint Guide - Part 11

This documentation blueprint details core rules, best practices, and recipes for `Observability & Alerting` operations.

### Pattern 31: SLIs/SLOs definitions in Prometheus Alerting Engine
When implementing `SLIs/SLOs definitions` within a `Prometheus Alerting Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Define explicit SLIs and SLOs for pipeline duration, row quality, and ingest delays.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 32: Prometheus alerts in Grafana Monitoring Dashboard
When implementing `Prometheus alerts` within a `Grafana Monitoring Dashboard` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure Prometheus alerting rules to fire alerts when SLA thresholds are breached.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 33: Grafana metric plots in OpenTelemetry Pipeline
When implementing `Grafana metric plots` within a `OpenTelemetry Pipeline` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Build dynamic Grafana metric plots tracing ingest rates and runtime patterns.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

