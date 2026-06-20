# GDPR Masking Rules for Data Governance
Implement dynamic data masking (DDM) for PII columns.

```sql
CREATE MASKING POLICY email_mask AS (val string) 
  RETURNS string -> 
  CASE 
    WHEN current_role() IN ('ANALYST') THEN regexp_replace(val, '.*@', '***@')
    ELSE val
  END;
```
