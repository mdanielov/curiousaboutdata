use msdb

select j.name,hist.* from dbo.sysjobs J
CROSS APPLY
(select top 1
CASE run_status
WHEN 0 THEN 'FAIL'
WHEN 1 THEN 'SUCCESS'
ELSE 'UNKNOWN' END [Status]
,run_status
,message
,CAST(STR(run_date, 8, 0) AS DATETIME) AS rundate
,CAST(STUFF(STUFF(REPLACE(STR(run_time, 6), ' ', '0'), 3, 0, ':'), 6, 0, ':') AS time(0)) AS runtime
,CAST(STUFF(STUFF(REPLACE(STR(run_duration, 6), ' ', '0'), 3, 0, ':'), 6, 0, ':') AS time(0)) AS duration 
from msdb..sysjobhistory where job_id=j.job_id) Hist
where 1=1
and enabled=1 --comment this out if you want to see schedules for disabled jobs
and run_status = 0 -- this filters out successful jobs. comment it out if you want to see them all
order by 5