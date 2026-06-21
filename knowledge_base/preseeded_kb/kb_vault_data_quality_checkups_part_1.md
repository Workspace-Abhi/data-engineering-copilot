# Data Quality Checkups Blueprint Guide - Part 1

This documentation blueprint details core rules, best practices, and recipes for `Data Quality Checkups` operations.

### Pattern 1: Expectation suites in Great Expectations Suite
When implementing `Expectation suites` within a `Great Expectations Suite` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Create Great Expectations suites to validate null values, ranges, and types on ingest.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 2: Soda core check files in Soda Core Check Engine
When implementing `Soda core check files` within a `Soda Core Check Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Define Soda Core check files containing declarative checks for data profile monitoring.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 3: Schema drift checks in Pandas Validation Engine
When implementing `Schema drift checks` within a `Pandas Validation Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure automated schema drift checks to catch unexpected column addition/deletions.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

