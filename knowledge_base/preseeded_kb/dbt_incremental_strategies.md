# Incremental Table Strategies in dbt
Optimize builds by updating tables incrementally instead of rebuilding.

```sql
{{ config(
    materialized='incremental',
    unique_key='event_id',
    incremental_strategy='merge'
) }}
select * from {{ ref('stg_events') }}
{% if is_incremental() %}
  where event_time >= (select max(event_time) from {{ this }})
{% endif %}
```
