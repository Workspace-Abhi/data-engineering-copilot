# Setting Service Level Agreements (SLAs) in Airflow
Receive email/Slack alerts when tasks exceed target runtimes.

```python
task = EmptyOperator(
    task_id="critical_task",
    sla=timedelta(minutes=30)
)
```
