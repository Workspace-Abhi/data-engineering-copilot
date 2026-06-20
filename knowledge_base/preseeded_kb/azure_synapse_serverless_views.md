# SQL Serverless Views in Azure Synapse Analytics
Query Parquet or CSV files directly in Data Lake Gen2.

```sql
CREATE VIEW stg_sales AS
SELECT * FROM OPENROWSET(
    BULK 'https://mylake.dfs.core.windows.net/sales/*.parquet',
    FORMAT = 'PARQUET'
) AS [result];
```
