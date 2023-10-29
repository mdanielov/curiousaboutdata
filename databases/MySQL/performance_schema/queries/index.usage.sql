use performance_schema;
select 
OBJECT_TYPE	#TABLE in the case of all indexes.
,OBJECT_SCHEMA	#Schema name.
,OBJECT_NAME	#Table name.
,INDEX_NAME	#Index name, or PRIMARY for the primary index, NULL for no index (inserts are counted in this case).
,COUNT_STAR	#Number of summarized events and the sum of the x_READ and x_WRITE columns.
,SUM_TIMER_WAIT	#Total wait time of the summarized events that are timed.
,MIN_TIMER_WAIT	#Minimum wait time of the summarized events that are timed.
,AVG_TIMER_WAIT	#Average wait time of the summarized events that are timed.
,MAX_TIMER_WAIT	#Maximum wait time of the summarized events that are timed.
,COUNT_READ	#Number of all read operations, and the sum of the equivalent x_FETCH columns.
,SUM_TIMER_READ	#Total wait time of all read operations that are timed.
,MIN_TIMER_READ	#Minimum wait time of all read operations that are timed.
,AVG_TIMER_READ	#Average wait time of all read operations that are timed.
,MAX_TIMER_READ	#Maximum wait time of all read operations that are timed.
,COUNT_WRITE	#Number of all write operations, and the sum of the equivalent x_INSERT, x_UPDATE and x_DELETE columns.
,SUM_TIMER_WRITE	#Total wait time of all write operations that are timed.
,MIN_TIMER_WRITE	#Minimum wait time of all write operations that are timed.
,AVG_TIMER_WRITE	#Average wait time of all write operations that are timed.
,MAX_TIMER_WRITE	#Maximum wait time of all write operations that are timed.
,COUNT_FETCH	#Number of all fetch operations.
,SUM_TIMER_FETCH	#Total wait time of all fetch operations that are timed.
,MIN_TIMER_FETCH	#Minimum wait time of all fetch operations that are timed.
,AVG_TIMER_FETCH	#Average wait time of all fetch operations that are timed.
,MAX_TIMER_FETCH	#Maximum wait time of all fetch operations that are timed.
,COUNT_INSERT	#Number of all insert operations.
,SUM_TIMER_INSERT	#Total wait time of all insert operations that are timed.
,MIN_TIMER_INSERT	#Minimum wait time of all insert operations that are timed.
,AVG_TIMER_INSERT	#Average wait time of all insert operations that are timed.
,MAX_TIMER_INSERT	#Maximum wait time of all insert operations that are timed.
,COUNT_UPDATE	#Number of all update operations.
,SUM_TIMER_UPDATE	#Total wait time of all update operations that are timed.
,MIN_TIMER_UPDATE	#Minimum wait time of all update operations that are timed.
,AVG_TIMER_UPDATE	#Average wait time of all update operations that are timed.
,MAX_TIMER_UPDATE	#Maximum wait time of all update operations that are timed.
,COUNT_DELETE	#Number of all delete operations.
,SUM_TIMER_DELETE	#Total wait time of all delete operations that are timed.
,MIN_TIMER_DELETE	#Minimum wait time of all delete operations that are timed.
,AVG_TIMER_DELETE	#Average wait time of all delete operations that are timed.
,MAX_TIMER_DELETE	#Maximum wait time of all delete operations that are timed.
from performance_schema.table_io_waits_summary_by_index_usage 
where OBJECT_SCHEMA not in ('mysql') 
#AND index_name is not null
and index_name is not NULL 
and index_name not in ('PRIMARY')
AND count_star =0
order by OBJECT_TYPE,OBJECT_SCHEMA,OBJECT_NAME,INDEX_NAME;