select * from (
select top 100 
qs.creation_time
,qs.last_execution_time
,qs.execution_count
,tp.query_plan 
,qs.plan_handle
,qt.dbid
,qt.objectid
--,tx.query_plan
, SUBSTRING(qt.text, (qs.statement_start_offset/2)+1,((CASE qs.statement_end_offset WHEN -1 THEN DATALENGTH(qt.text) ELSE qs.statement_end_offset  END - qs.statement_start_offset)/2) + 1) AS statement_text
,cast (tx.query_plan AS XML) [test]
--,qs.*
from sys.dm_exec_query_stats (nolock) qs
CROSS APPLY sys.dm_exec_sql_text (qs.sql_handle) AS qt
OUTER APPLY sys.dm_exec_query_plan(qs.plan_handle) tp 
OUTER APPLY sys.dm_exec_text_query_plan(qs.plan_handle,qs.statement_start_offset,qs.statement_end_offset) tx
where 1=1
--AND qt.dbid=db_id('mydb')
--AND qt.objectid=object_id('my_object_name')
--AND qt.objectid =  288398966
--AND qs.creation_time < 'my_timestamp'
order by qs.creation_time desc
) X
--where 
where statement_text like '%parententerpriseid %'
order by last_execution_time desc

