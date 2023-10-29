SELECT	--top 50
	name,
	runtime,
	duration,
	job_id,
	status,
	step_id,
	CONVERT(DATE,rundate) rundate,
	runtime AS start_time,
	duration,
	message
FROM	(
		SELECT	
		top 100
 J.name
,j.job_id
,CASE JH.run_status
WHEN 0 THEN 'FAIL'
WHEN 1 THEN 'SUCCESS'
ELSE 'UNKNOWN' END [Status]
,JH.step_id
--,JH.step_name
,JH.message
,CAST(STR(run_date, 8, 0) AS DATETIME) AS rundate
,CAST(STUFF(STUFF(REPLACE(STR(run_time, 6), ' ', '0'), 3, 0, ':'), 6, 0, ':') AS time(0)) AS runtime
,CAST(STUFF(STUFF(REPLACE(STR(run_duration, 6), ' ', '0'), 3, 0, ':'), 6, 0, ':') AS time(0)) AS duration
FROM 
    msdb..sysjobhistory jh 
INNER JOIN 
    msdb..sysjobs j 
ON 
    j.job_id = jh.job_id 
WHERE 
1=1
and JH.run_status = 0
and JH.step_id !=0
ORDER BY 
CAST(STR(run_date, 8, 0) AS DATETIME) desc
,CAST(STUFF(STUFF(REPLACE(STR(run_time, 6), ' ', '0'), 3, 0, ':'), 6, 0, ':') AS time(0)) desc
) AS d
--where [message] like '%error%'
order by 
name
,step_id

