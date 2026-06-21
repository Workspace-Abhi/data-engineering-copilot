# Data Engineering Code Review Blueprint Guide - Part 7

This documentation blueprint details core rules, best practices, and recipes for `Data Engineering Code Review` operations.

### Pattern 19: Compactor reviews in SQLFluff Linter
When implementing `Compactor reviews` within a `SQLFluff Linter` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Confirm that temporary file directories are purged at the end of runs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 20: Style conventions check in Flake8 Python Lint
When implementing `Style conventions check` within a `Flake8 Python Lint` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Review query partition conditions to ensure partition index keys are utilized.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 21: Anti-patterns checks in Spark Query Analyzer
When implementing `Anti-patterns checks` within a `Spark Query Analyzer` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Audit PySpark scripts to detect collect() anti-patterns that trigger executor crashes.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

