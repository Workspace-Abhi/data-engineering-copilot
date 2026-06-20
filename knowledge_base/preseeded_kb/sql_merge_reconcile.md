# Advanced SQL MERGE Statements, CDC Setup, & Data Reconciliation

This guide provides optimization instructions and templates for high-performance SQL upserting, CDC tracking, and data reconciliation audits.

---

## 1. SQL MERGE Upsert Statements

The `MERGE` statement matches rows in a target table with rows in a source table to run updates and inserts in a single atomic transaction.

### ANSI SQL MERGE Template
```sql
-- MERGE Statement for Customers
MERGE INTO production.Customers AS T
USING staging.Customers AS S
    ON T.CustomerID = S.CustomerID
WHEN MATCHED AND (
    T.Name <> S.Name OR 
    T.Email <> S.Email OR 
    T.ModifiedDate < S.ModifiedDate
) THEN
    UPDATE SET 
        T.Name = S.Name,
        T.Email = S.Email,
        T.ModifiedDate = GETDATE()
WHEN NOT MATCHED BY TARGET THEN
    INSERT (CustomerID, Name, Email, ModifiedDate)
    VALUES (S.CustomerID, S.Name, S.Email, GETDATE())
WHEN NOT MATCHED BY SOURCE THEN
    DELETE; -- Optional: Sync deletion
```

---

## 2. SQL Server Change Data Capture (CDC) Setup

CDC tracks insert, update, and delete actions applied to SQL Server tables, providing clean transaction rows for downstream ETL.

### Enable Database CDC
```sql
USE TargetDatabase;
GO
EXEC sys.sp_cdc_enable_db;
GO
```

### Enable Table CDC
Enable change tracking on the `Customers` table, including specific tracking columns:
```sql
EXEC sys.sp_cdc_enable_table
    @source_schema = N'dbo',
    @source_name   = N'Customers',
    @role_name     = NULL, -- Disable gatekeeping roles
    @supports_net_changes = 1; -- Required for net-change queries
GO
```

---

## 3. Data Reconciliation & Audit Queries

Reconciliation queries audit ingestion processes by checking row discrepancies, orphaned keys, and metrics mismatch.

### Row Mismatch Discovery Template
```sql
WITH SourceRec AS (
    SELECT CustomerID, HASHBYTES('SHA2_256', CONCAT(Name, Email)) AS SourceHash
    FROM staging.Customers
),
TargetRec AS (
    SELECT CustomerID, HASHBYTES('SHA2_256', CONCAT(Name, Email)) AS TargetHash
    FROM production.Customers
)
-- Identify mismatch types
SELECT 
    COALESCE(S.CustomerID, T.CustomerID) AS RecordID,
    CASE 
        WHEN T.CustomerID IS NULL THEN 'Missing In Target (Orphaned Row)'
        WHEN S.CustomerID IS NULL THEN 'Extra In Target (Stale Row)'
        WHEN S.SourceHash <> T.TargetHash THEN 'Data Hash Discrepancy (Value Drift)'
    END AS DiscrepancyReason
FROM SourceRec AS S
FULL OUTER JOIN TargetRec AS T ON S.CustomerID = T.CustomerID
WHERE S.CustomerID IS NULL 
   OR T.CustomerID IS NULL 
   OR S.SourceHash <> T.TargetHash;
```
