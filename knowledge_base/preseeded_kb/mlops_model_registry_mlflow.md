# Model Registry and Tracking with MLflow
Log hyper-parameters, metrics, and models during pipeline execution.

```python
import mlflow
mlflow.start_run()
mlflow.log_param("epochs", 10)
mlflow.log_metric("accuracy", 0.95)
mlflow.log_model(model, "model")
mlflow.end_run()
```
