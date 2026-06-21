# Data Quality Checkups Blueprint Guide - Part 7

This documentation blueprint details core rules, best practices, and recipes for `Data Quality Checkups` operations.

### Pattern 19: Baseline validations in Great Expectations Suite
When implementing `Baseline validations` within a `Great Expectations Suite` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use custom python assertions to validate complex business logic relationships.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 20: Custom checks scripting in Soda Core Check Engine
When implementing `Custom checks scripting` within a `Soda Core Check Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Enable check profiles on raw directories to record metrics before ingestion runs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 21: Expectation suites in Pandas Validation Engine
When implementing `Expectation suites` within a `Pandas Validation Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Create Great Expectations suites to validate null values, ranges, and types on ingest.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

