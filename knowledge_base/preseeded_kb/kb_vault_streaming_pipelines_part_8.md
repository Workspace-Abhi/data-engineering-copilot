# Streaming Pipelines Blueprint Guide - Part 8

This documentation blueprint details core rules, best practices, and recipes for `Streaming Pipelines` operations.

### Pattern 22: Kafka Schema Registry in Confluent Cloud Registry
When implementing `Kafka Schema Registry` within a `Confluent Cloud Registry` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement watermarking thresholds in streaming window queries to discard late-arriving events.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 23: Flink DDL setup in Azure Event Hubs
When implementing `Flink DDL setup` within a `Azure Event Hubs` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use stateful deduplication logic utilizing key identifiers to reject duplicate payloads.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 24: Deduplication logic in AWS Kinesis Engine
When implementing `Deduplication logic` within a `AWS Kinesis Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure distributed checkpoints on reliable file stores to ensure state recovery.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

