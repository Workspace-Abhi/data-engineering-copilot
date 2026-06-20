# Scaling Tasks via Airflow KubernetesPodOperator
Run heavy data tasks inside isolated Kubernetes Pods.

```python
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

task = KubernetesPodOperator(
    name="run-spark-job",
    image="apache/spark:latest",
    cmds=["spark-submit", "job.py"],
    task_id="spark_pod",
)
```
