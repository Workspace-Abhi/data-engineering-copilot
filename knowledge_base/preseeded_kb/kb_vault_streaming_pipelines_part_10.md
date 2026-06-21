# Streaming Pipelines Blueprint Guide - Part 10

This documentation blueprint details core rules, best practices, and recipes for `Streaming Pipelines` operations.

### Pattern 28: Watermarking offsets in Confluent Cloud Registry
When implementing `Watermarking offsets` within a `Confluent Cloud Registry` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Leverage Flink DDL to directly connect stream sources to target analytics sinks.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 29: Partition keys selection in Azure Event Hubs
When implementing `Partition keys selection` within a `Azure Event Hubs` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure buffer size thresholds to prevent out-of-memory errors on high-throughput runs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 30: Consumer group offsets in AWS Kinesis Engine
When implementing `Consumer group offsets` within a `AWS Kinesis Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Monitor consumer lag using Prometheus metrics to scale partition allocations.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

