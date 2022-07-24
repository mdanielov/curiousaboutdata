use msdb

declare @n int = 3

select j.name,hist.* from dbo.sysjobs J
CROSS APPLY
(select top  (@n)
CASE run_status
WHEN 0 THEN 'FAIL'
WHEN 1 THEN 'SUCCESS'
ELSE 'UNKNOWN' END [Status]
,run_status
,message
,step_id
,CAST(STR(run_date, 8, 0) AS DATETIME) AS rundate
,CAST(STUFF(STUFF(REPLACE(STR(run_time, 6), ' ', '0'), 3, 0, ':'), 6, 0, ':') AS time(0)) AS runtime
,CAST(STUFF(STUFF(REPLACE(STR(run_duration, 6), ' ', '0'), 3, 0, ':'), 6, 0, ':') AS time(0)) AS duration 
from msdb..sysjobhistory jh where jh.job_id=j.job_id
and step_id <>0
and jh.run_status = 0 -- this filters out successful jobs. comment it out if you want to see them all
order by run_date desc, step_id, run_time) Hist
where 1=1
and enabled=1 --comment this out if you want to see schedules for disabled jobs
order by j.name