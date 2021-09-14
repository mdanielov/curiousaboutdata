SELECT 
`DIGEST_TEXT`
,count(1) `num_exec`
,SUM(ROUND((`timer_end`-`timer_start`)/1000000000, 2)) AS `tot_exec_ms`
,SUM(ROUND(`timer_wait`/1000000000, 2))  `wait_ms`
,SUM(ROUND(`lock_time`/1000000000, 2))  `lock_wait_ms`
,    `CURRENT_SCHEMA`
,    `OBJECT_TYPE`
,    `OBJECT_SCHEMA`
,    `OBJECT_NAME`
FROM `performance_schema`.`events_statements_history_long`
WHERE 
1=1
and `SQL_TEXT` is not NULL
and `SQL_TEXT` not like 'SET NAMES%'
and `SQL_TEXT` not like 'use %'
and `SQL_TEXT` not like 'show %'
and `SQL_TEXT` not in ('COMMIT', 'START TRANSACTION')
and CURRENT_SCHEMA not in ('performance_schema')
GROUP BY `DIGEST_TEXT`
,`CURRENT_SCHEMA`
,    `OBJECT_TYPE`
,    `OBJECT_SCHEMA`
,    `OBJECT_NAME`
order by `num_exec` desc