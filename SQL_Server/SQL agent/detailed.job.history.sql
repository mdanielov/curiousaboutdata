USE MSDB
GO
declare @n int = 1

SELECT	--top 50
	distinct
	name,
	job_id,
	[status],
	step_id,
	runtime,
	duration,
	CONVERT(DATE,rundate) rundate,
	runtime AS start_time,
	duration,
	[message],
	[command],
	CASE WHEN schedule_id is null THEN 'NoSchedule' ELSE 'YesSchedule' END [HasSchedule]
FROM	(	
select 
j.[name]
,j.[job_id]
,j.[enabled]
,b.[database_name]
,b.[step_name]
,b.[step_id]
,b.[command]
,Hist.[Status]
,Hist.[duration]
,Hist.[rundate]
,Hist.[runtime]
,Hist.[message]
,s.schedule_id
FROM 
sysjobs j  JOIN
sysjobsteps b ON j.job_id=b.job_id
LEFT OUTER JOIN dbo.sysjobschedules s ON j.job_id = s.job_id
OUTER APPLY
(select top  (@n)
CASE run_status
WHEN 0 THEN 'FAIL'
WHEN 1 THEN 'SUCCESS'
ELSE 'UNKNOWN' END [Status]
,run_status
,[message]
,step_id
,CAST(STR(run_date, 8, 0) AS DATETIME) AS rundate
,CAST(STUFF(STUFF(REPLACE(STR(run_time, 6), ' ', '0'), 3, 0, ':'), 6, 0, ':') AS time(0)) AS runtime
,CAST(STUFF(STUFF(REPLACE(STR(run_duration, 6), ' ', '0'), 3, 0, ':'), 6, 0, ':') AS time(0)) AS duration 
from msdb..sysjobhistory jh where jh.job_id=j.job_id and b.step_id = jh.step_id
--and step_id <>0
--and jh.run_status = 0 -- this filters out successful jobs. comment it out if you want to see them all
order by run_date desc, step_id, run_time) Hist
) A
order by [name],[step_id]
--select * from sysjobs