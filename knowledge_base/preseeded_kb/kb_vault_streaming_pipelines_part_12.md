# Streaming Pipelines Blueprint Guide - Part 12

This documentation blueprint details core rules, best practices, and recipes for `Streaming Pipelines` operations.

### Pattern 34: Deduplication logic in Confluent Cloud Registry
When implementing `Deduplication logic` within a `Confluent Cloud Registry` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure distributed checkpoints on reliable file stores to ensure state recovery.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 35: Checkpoint stores in Azure Event Hubs
When implementing `Checkpoint stores` within a `Azure Event Hubs` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Optimize consumer group offset committing intervals to reduce replication lags.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 36: Event time windows in AWS Kinesis Engine
When implementing `Event time windows` within a `AWS Kinesis Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Utilize sliding event time windows to aggregate metrics over continuous intervals.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

