
select count(1) [cnt]
,CONVERT(DATE,start_time) DT
FROM sys.event_log
WHERE event_type = 'deadlock'
GROUP BY CONVERT(DATE,start_time)
ORDER BY 2 desc;