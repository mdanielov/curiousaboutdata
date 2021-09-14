use performance_schema;
select 
OBJECT_SCHEMA `DATABASE`
,OBJECT_NAME `TABLE`
,sum(COUNT_STAR) `COUNT_STAR`
,SUM(COUNT_READ) `READ_WAITS`
,SUM(COUNT_WRITE) `WRITE_WAITS`
 from table_lock_waits_summary_by_table where OBJECT_SCHEMA not in ('mysql')
 GROUP BY OBJECT_SCHEMA,OBJECT_NAME ORDER BY COUNT_STAR desc;
 
 