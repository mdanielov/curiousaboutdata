 USE msdb
GO
DECLARE @id uniqueidentifier, @nm sysname
set @nm='00'

select 
job_name=b.name,
ISNULL((C.active_end_time-C.active_start_time)/60/60,0) [duration],
ISNULL(C.name,'N/A') [schedule_name],
ISNULL(CASE C.freq_type
WHEN 1  THEN 'Once'
WHEN 4  THEN 'Daily'
WHEN 8  THEN 'Weekly'
WHEN 16 THEN 'Monthly'
WHEN 32 THEN 'Monthly relative'
WHEN 64 THEN 'when SQLServerAgent service starts' END,'N/A') [frequency_type],
ISNULL(CASE
WHEN C.freq_type=1 THEN 'N/A'
WHEN C.freq_type=4 THEN 'every '+convert(varchar,C.freq_interval)+' day(s)'
WHEN C.freq_type=8  THEN
CASE
	when C.freq_interval=1   THEN 'Sunday'
	when C.freq_interval=2   THEN 'Monday'
	when C.freq_interval=4   THEN 'Tuesday'
	when C.freq_interval=8   THEN 'Wednesday'
	when C.freq_interval=16  THEN 'Thursday'
	when C.freq_interval=32  THEN 'Friday'
	when C.freq_interval=64  THEN 'Saturday'
		END
WHEN freq_type=16 THEN 'on '+convert(varchar,C.freq_interval)+
				CASE when C.freq_interval=1 THEN'st day' 
				WHEN C.freq_interval=2 THEN 'nd day' 
					ELSE 'th day' END
WHEN C.freq_type=32 THEN
CASE
	when C.freq_interval=1    THEN 'Sunday' 
	when C.freq_interval=2    THEN 'Monday'
	when C.freq_interval=3    THEN 'Tuesday'
	when C.freq_interval=4    THEN 'Wednesday'
	when C.freq_interval=5    THEN 'Thursday'
	when C.freq_interval=6    THEN 'Friday'
	when C.freq_interval=7    THEN 'Saturday'
	when C.freq_interval=8    THEN 'Day'
	when C.freq_interval=9    THEN 'Weekday'
	when C.freq_interval=10   THEN 'Weekend day'
		END
 END,'N/A') [interval],
ISNULL(C.freq_subday_interval,0) [number_of_units],
ISNULL(CASE c.freq_subday_type
WHEN 1 THEN 'At the specified time'
WHEN 2 THEN 'Second(s)'
WHEN 4 THEN 'Minute(s)'
WHEN 8 THEN 'Hour(s)'
	END,'N/A') [frequency_units],
B.enabled [job_enabled],
ISNULL(C.enabled,0) [schedule_enabled]
from sysjobs B
LEFT JOIN sysjobschedules A  on A.job_id = B.job_id
LEFT JOIN sysschedules C on A.schedule_id = C.schedule_id
where 
--a.job_id in (SELECT  job_id from sysjobs where name like @nm+'%')and 
1=1
--AND b.name like '%daily backup%'
--AND a.enabled=1
order by 1
