# Airflow DAG Authoring Best Practices
Learn how to write production-ready Apache Airflow DAGs.

## Key Rules
- **Idempotency**: Running the same DAG run multiple times must produce the same result.
- **Task Atomicity**: Each task should do exactly one thing (e.g., extract data, or copy data, not both).
- **Avoid Top-Level Code**: Do not make database calls or complex computations outside of operators.

```python
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime

with DAG(
    dag_id="airflow_best_practices_v1",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")
    start >> end
```
