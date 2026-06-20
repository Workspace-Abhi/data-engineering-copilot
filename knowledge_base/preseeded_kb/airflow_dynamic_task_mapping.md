# Airflow Dynamic Task Mapping
Generate task runs dynamically based on variables returned at runtime.

```python
@task
def get_files():
    return ["file1.csv", "file2.csv", "file3.csv"]

@task
def process(file):
    print(file)

files = get_files()
process.expand(file=files)
```
