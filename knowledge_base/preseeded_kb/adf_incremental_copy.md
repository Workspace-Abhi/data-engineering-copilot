# Azure Data Factory Incremental Copy & Dynamic Expressions

Incremental data ingestion (Delta load) retrieves only modified or new rows from the source datastore since the last ingestion run.

---

## Watermark-Based Copy Pipelines

A watermark pipeline maintains a configuration table in the target database to store the last processed timestamp.

### Pipeline Layout Flow
```
[Lookup Last Watermark] --------\
                                 ====> [Copy Activity] ===> [Update Watermark Table]
[Lookup Max Current Watermark] --/
```

### 1. Lookup Old Watermark Activity
Reads the last timestamp from the target control table:
```sql
SELECT WatermarkValue FROM dbo.WatermarkControl WHERE TableName = '@{pipeline().parameters.TableName}'
```

### 2. Lookup New Watermark Activity
Reads the maximum timestamp currently present in the source table:
```sql
SELECT MAX(ModifiedDate) AS MaxWatermark FROM dbo.SourceCustomers
```

### 3. Copy Activity
Reads the delta data from the source and writes it to the target:
- **Source SQL Query**:
  ```sql
  SELECT * FROM dbo.SourceCustomers 
  WHERE ModifiedDate > '@{activity('LookupOldWatermark').output.firstRow.WatermarkValue}'
    AND ModifiedDate <= '@{activity('LookupNewWatermark').output.firstRow.MaxWatermark}'
  ```

### 4. Update Control Table Activity
Runs a stored procedure or SQL script to update the control table:
```sql
UPDATE dbo.WatermarkControl 
SET WatermarkValue = '@{activity('LookupNewWatermark').output.firstRow.MaxWatermark}' 
WHERE TableName = '@{pipeline().parameters.TableName}'
```

---

## Dynamic Expressions Guidelines

Expressions in ADF are prefixed with `@` and enclosed in curly braces if nested in strings.

### Concat Year/Month/Day Folders
Dynamically parameterize raw output file folders in ADLS Gen2:
```json
@concat('raw/customers/year=', formatDateTime(utcnow(), 'yyyy'), '/month=', formatDateTime(utcnow(), 'MM'), '/day=', formatDateTime(utcnow(), 'dd'))
```

### If-Condition Expression
Return a fallback connection string if a parameter value is empty:
```json
@if(empty(pipeline().parameters.CustomConnectionString), 'DefaultConnectionString', pipeline().parameters.CustomConnectionString)
```

### Coalesce Parameter Values
Return the first non-null argument parameter:
```json
@coalesce(pipeline().parameters.OverrideBatchSize, '1000')
```
