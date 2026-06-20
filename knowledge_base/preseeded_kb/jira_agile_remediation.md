# Jira Scrum Remediation Planning & Estimation Templates

This document details scrum engineering strategies for mapping Jira backlogs into organized sprints and workload capacities.

---

## 1. Issue Prioritization Matrix

Jira tickets must be triaged based on business impact and engineering complexity to decide active sprint targets.

| Jira Priority | Complexity (Story Points) | Target Sprint | Remediation Action |
| :--- | :--- | :--- | :--- |
| 🔴 **Highest** | 1 - 3 | Immediate | Run hotfix pipeline update. |
| 🟡 **High** | 5 - 8 | Next Sprint | Re-index tables, adjust watermark offsets. |
| 🟢 **Medium** | 3 - 5 | Within 2 Sprints | Add unit testing coverage, refactor helpers. |
| 🔵 **Low** | 1 - 2 | Backlog | Adjust logger output rotations. |

---

## 2. Sprint Capacity Remediation Planning

When ingestion issues trigger backlog remediation, compute total sprint load using the **Team Capacity Equation**:

$$\text{Sprint Capacity} = (\text{Developer Count} \times \text{Available Days}) \times \text{Focus Factor}$$

### Backlog Workload Planning Template
```markdown
## Remediation Plan: Core Data Migration
- **Workstream Owner**: @DevManager
- **Remediation Goal**: Resolve legacy CSV parsing failures.
- **Estimated Points**: 18 Story Points (across 3 tasks)

### Tasks
1. **[Core Parser]** Resolve date formatting issues in `utils/file_parser.py` (5 SP)
2. **[Ingestion]** Update ADF lookup queries to skip trailing empty rows (8 SP)
3. **[Testing]** Write mock verification scripts and unit tests (5 SP)
```
