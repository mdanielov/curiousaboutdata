use master
BEGIN	try
 
select * from 
(select 
SUBSTRING(st.text, (s.stmt_start/2)+1,((CASE s.stmt_end WHEN -1 THEN DATALENGTH(st.text) ELSE s.stmt_end END - s.stmt_start)/2) + 1) [text] 
--1 [text]
,[Program]=CASE WHEN s.program_name like '%SQLAgent%' and s.program_name not in ('SQLAgent - Email Logger','SQLAgent - Generic Refresher','SQLAgent - Alert Engine','SQLAgent - Job invocation engine','SQLAgent - Job Manager') THEN
(select 'SQL job : '+name from msdb..sysjobs where job_id=CAST(convert(binary,ltrim(substring(s.program_name,charindex('0x',s.program_name),(charindex(' ',s.program_name,charindex('0x',s.program_name))-charindex('0x',s.program_name)))),1) AS uniqueidentifier))
ELSE rtrim(s.program_name) END
,rtrim(s.cmd) cmd
,rtrim(s.physical_io) [IO]
,CONVERT(bigint,rtrim(s.cpu)) [CPU]
,rtrim(db_name(s.dbid)) [db]
,rtrim(s.dbid) [db_id]
,convert(int,rtrim(s.spid)) [spid]
,CASE blocked when convert(int,rtrim(s.spid)) THEN -1 ELSE convert(int,rtrim(blocked)) END  [blk]
,rtrim(s.lastwaittype) [WtTpe]
,rtrim(s.loginame) [Login]
,rtrim(s.dbid) [dbid]
,s.WaitType
,rtrim(s.waittime) [WtTme]
,rtrim(s.waitresource) [Resource]
,rtrim(s.hostname) [Host]
from master..sysprocesses s with (nolock)
CROSS APPLY sys.dm_exec_sql_text(s.sql_handle) AS st
/* change the where conditions as you see fit */
where 
1=1 
----and lastwaittype not in ('BROKER_RECEIVE_WAITFOR','SOS_SCHEDULER_YIELD')
----AND lastwaittype in ('PAGEIOLATCH_SH','PAGELATCH_UP')
--spid<>blocked AND 
--and s.dbid=17
--and dbid<>9

--and program_name like '%SQLPro%'
AND cmd<>'AWAITING COMMAND'
--and spid in (260)
--AND spid<>51
and spid <> @@spid
AND cmd not in ('CHECKPOINT SLEEP','LOG WRITER','LOCK MONITOR','LAZY WRITER','TASK MANAGER','SIGNAL HANDLER','GHOST CLEANUP',
'CHECKPOINT','XE TIMER','XE DISPATCHER','RESOURCE MONITOR','BRKR TASK','BRKR EVENT HNDLR','TRACE QUEUE TASK','RECOVERY WRITER','UNKNOWN TOKEN','SYSTEM_HEALTH_MO')
--AND lastwaittype not in ('BROKER_RECEIVE_WAITFOR')
--AND s.waitresource like 'METADATA%'
)A
--order by convert(bigint,IO) desc,spid desc,db desc,WtTme desc
order by blk desc,cpu desc,db desc,WtTme desc
--order by login
END TRY

BEGIN catch
select program_name from master..sysprocesses with (nolock) where program_name like '%SQLAgent%'
END catch

