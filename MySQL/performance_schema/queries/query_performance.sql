#set @@global.show_compatibility_56=ON;
use performance_schema;
select * from (
SELECT 
`SQL_TEXT`
,	 `THREAD_ID`
,    `EVENT_ID`
,    `END_EVENT_ID`
,    `EVENT_NAME`
,    `SOURCE`
,date_sub(now(),INTERVAL (select VARIABLE_VALUE from information_schema.global_status where variable_name='UPTIME')-`TIMER_START`*10e-13 second) `TIMER_START`
,date_sub(now(),INTERVAL (select VARIABLE_VALUE from information_schema.global_status where variable_name='UPTIME')-`TIMER_END`*10e-13 second) `TIMER_END`
,ROUND((`timer_end`-`timer_start`)/1000000000, 2) AS `tot_exec_ms`
,ROUND(`timer_wait`/1000000000, 2)  `wait_ms`
,	 ROUND(`lock_time`/1000000000, 2)  `lock_wait_ms`
,    `DIGEST`
,    `DIGEST_TEXT`
,    `CURRENT_SCHEMA`
,    `OBJECT_TYPE`
,    `OBJECT_SCHEMA`
,    `OBJECT_NAME`
,    `OBJECT_INSTANCE_BEGIN`
,    `MYSQL_ERRNO`
,    `RETURNED_SQLSTATE`
,    `MESSAGE_TEXT`
,    `ERRORS`
,    `WARNINGS`
,    `ROWS_AFFECTED`
,    `ROWS_SENT`
,    `ROWS_EXAMINED`
,    `CREATED_TMP_DISK_TABLES`
,    `CREATED_TMP_TABLES`
,    `SELECT_FULL_JOIN`
,    `SELECT_FULL_RANGE_JOIN`
,    `SELECT_RANGE`
,    `SELECT_RANGE_CHECK`
,    `SELECT_SCAN`
,    `SORT_MERGE_PASSES`
,    `SORT_RANGE`
,    `SORT_ROWS`
,    `SORT_SCAN`
,    `NO_INDEX_USED`
,    `NO_GOOD_INDEX_USED`
,    `NESTING_EVENT_ID`
,    `NESTING_EVENT_TYPE`
FROM `performance_schema`.`events_statements_current`) x
where 1=1
and `SQL_TEXT` is not NULL
and `SQL_TEXT` not in ('COMMIT')
and CURRENT_SCHEMA not in ('performance_schema')
#AND `No_INDEX_USED` = 1
#and tot_exec_ms > 10
#and THREAD_ID = 931712
order by thread_id desc,event_id
limit 10
;
