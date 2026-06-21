# Streaming Pipelines Blueprint Guide - Part 14

This documentation blueprint details core rules, best practices, and recipes for `Streaming Pipelines` operations.

### Pattern 40: Consumer group offsets in Confluent Cloud Registry
When implementing `Consumer group offsets` within a `Confluent Cloud Registry` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Monitor consumer lag using Prometheus metrics to scale partition allocations.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 41: Spark Streaming in Azure Event Hubs
When implementing `Spark Streaming` within a `Azure Event Hubs` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Integrate Kafka Schema Registry to validate Avro schemas and detect schema breaks.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 42: Kafka Schema Registry in AWS Kinesis Engine
When implementing `Kafka Schema Registry` within a `AWS Kinesis Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement watermarking thresholds in streaming window queries to discard late-arriving events.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

