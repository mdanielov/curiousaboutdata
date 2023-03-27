if OBJECT_ID('tempdb..#temp_tb') IS NOT NULL
drop table #temp_tb

declare @lock_type TABLE(
rsc_type tinyint
,lock_name varchar(200)
)

declare @lock_mode TABLE(
req_mode tinyint
,mode_name varchar(200)
)

declare @lock_status TABLE(
req_status tinyint
,status_name varchar(200)
)

INSERT INTO @lock_type
VALUES(1,' NULL Resource (not used)')
,(2,'Database')
,(3,'File')
,(4,'Index')
,(5,'Table')
,(6,'Page')
,(7,'Key')
,(8,'Extent')
,(9,'RID (Row ID)')
,(10,'Application')

INSERT INTO @lock_mode
VALUES(0,'NULL')
,(1,'Sch-S')
,(2,'Sch-M')
,(3,'S')
,(4,'U')
,(5,'X')
,(6,'IS')
,(7,'IU')
,(8,'IX')
,(9,'SIU')
,(10,'SIX')
,(11,'UIX')
,(12,'BU')
,(13,'RangeS_S')
,(14,'RangeS_U')
,(15,'RangeI_N')
,(16,'RangeI_S')
,(17,'RangeI_U')
,(18,'RangeI_X')
,(19,'RangeX_S')
,(20,'RangeX_U')
,(21,'RangeX_X')

INSERT INTO @lock_status
VALUES(1,'Granted')
,(2,'Converting')
,(3,'Waiting')

select *
INTO #temp_tb
from (
select 
rtrim(p.loginame)  [login]
,cast(s.req_spid as int) As spid
,convert(varchar(30), db_name(s.rsc_dbid)) [db_name]
,s.rsc_indid As indid
,ty.lock_name [Type]
,m.mode_name [Mode]
,st.status_name [Status]
,rsc_text [Resource]
--,substring (s.rsc_text, 1, 16) [Resource]
--,* 
from syslockinfo s with (nolock)
join sysprocesses p with (nolock) on s.req_spid = p.spid
JOIN @lock_type ty ON s.rsc_type =ty.rsc_type
JOIN @lock_mode m ON s.req_mode = m.req_mode
JOIN @lock_status st ON s.req_status = st.req_status
where p.cmd<>'AWAITING COMMAND'
and p.spid <> @@spid
AND p.cmd not in ('CHECKPOINT SLEEP','LOG WRITER','LOCK MONITOR','LAZY WRITER','TASK MANAGER','SIGNAL HANDLER','GHOST CLEANUP',
'CHECKPOINT','XE TIMER','XE DISPATCHER','RESOURCE MONITOR','BRKR TASK','BRKR EVENT HNDLR','TRACE QUEUE TASK','RECOVERY WRITER','UNKNOWN TOKEN','SYSTEM_HEALTH_MO')
) A

select count(1) cnt
,[Type]
,[Mode]
,[status]
,[spid]
from #temp_tb
--where [spid]=232
group by [Type],[Mode]
,[status]
,[spid]

order by 2
