if OBJECT_ID('tempdb..#tbl_deadlocks') is not null
DROP TABLE #tbl_deadlocks

if OBJECT_ID('tempdb..#tbl_events') is not null
DROP TABLE #tbl_events

if OBJECT_ID('tempdb..#tbl_process_list') is not null
DROP TABLE #tbl_process_list

if OBJECT_ID('tempdb..#tbl_process_frame') is not null
DROP TABLE #tbl_process_frame

create table #tbl_deadlocks (dl_id bigint identity
,event_data XML)

CREATE TABLE #tbl_events(
[e_id] bigint identity
,[dl_id] bigint
,[event_data] XML
,[Event_TimeStampt] datetime2
,[deadlock_cycle_id] INT
,[server_name] sysname
,[database_name] sysname
,[victimProcess] varchar(120)
,[dl_frg] XML
)

CREATE TABLE #tbl_process_list
(
[p_id] bigint identity
,[dl_id] bigint
,[e_id] bigint
,[ProcessID] varchar(200)
,[waitresource] varchar(600)
,[lockMode] varchar(60)
,[hostname] varchar(120)
,[inputbuf] varchar(max)
,[isolationlevel] varchar(60)
,[loginname]  varchar(60)
,[status] varchar(60)
,[Q] XML
)

CREATE TABLE #tbl_process_frame
(
[f_id] bigint identity
,[p_id] bigint
,[procname] varchar(120)
,[sqlhandle] varbinary(64)
,[frame_text] varchar(max)
)

--initial list of the deadlock XML from the system function
INSERT #tbl_deadlocks(event_data)
select top 50 CAST(event_data as XML) event_data
				FROM sys.fn_xe_telemetry_blob_target_read_file('dl', NULL, NULL, NULL)
				WHERE object_name = 'database_xml_deadlock_report'
				ORDER BY  timestamp_utc desc

--parse the XML to get the basic even data and isolate the deadlock XML
INSERT #tbl_events([dl_id],[event_data],[Event_TimeStampt],[deadlock_cycle_id],[server_name],[database_name],[victimProcess],[dl_frg])
select
base.dl_id
,base.event_data
,T.myEvent.value('(@timestamp)[1]', 'datetime2') AS Event_TimeStampt
,T.myEvent.value('(./data[@name="deadlock_cycle_id"]/value)[1]', 'INT') [deadlock_cycle_id]
,T.myEvent.value('(./data[@name="server_name"]/value)[1]', 'sysname') AS [server_name]
,T.myEvent.value('(./data[@name="database_name"]/value)[1]', 'sysname') AS [database_name]
,T.myEvent.value('(./data/value/deadlock/victim-list/victimProcess/@id)[1]', 'varchar(120)') [victimProcess]
,T.myEvent.query('./data/value/deadlock') as [dl_frg]
FROM #tbl_deadlocks base
CROSS APPLY base.event_data.nodes('/event') AS T(myEvent)

--parse the process list
INSERT #tbl_process_list ([dl_id],[e_id],[ProcessID],[waitresource],[lockMode],[hostname],[inputbuf],[isolationlevel],[loginname],[status],[Q])
select
E.[dl_id]
,E.e_id
,T.myProcess.value('(./@id)[1]', 'varchar(200)') [ProcessID]
,T.myProcess.value('(./@waitresource)[1]', 'varchar(600)') [waitresource]
,T.myProcess.value('(./@lockMode)[1]', 'varchar(60)') [lockMode]
,T.myProcess.value('(./@hostname)[1]', 'varchar(120)') [hostname]
,T.myProcess.value('(./inputbuf)[1]', 'varchar(max)') [inputbuf]
,T.myProcess.value('(./@isolationlevel)[1]', 'varchar(60)') [isolationlevel]
,T.myProcess.value('(./@loginname)[1]', 'varchar(60)') [loginname]
,T.myProcess.value('(./@status)[1]', 'varchar(60)') [status]
,T.myProcess.query('.') Q
from #tbl_events E
CROSS APPLY E.[dl_frg].nodes('/deadlock/process-list/process') AS T(myProcess)


--get the frame
INSERT #tbl_process_frame([p_id],[procname],[sqlhandle],[frame_text])
SELECT 
P.p_id
,T.myFrame.value('(./@procname)[1]', 'varchar(120)') [procname]
,CAST(T.myFrame.value('(./@sqlhandle)[1]', 'varchar(max)')as varbinary(64)) [sqlhandle]
,T.myFrame.value('(.)[1]', 'varchar(max)') [frame_text]
from #tbl_process_list P
CROSS APPLY P.Q.nodes('/process/executionStack/frame') AS T(myFrame)

update #tbl_process_frame set procname = NULL where procname = 'unknown'
update #tbl_process_frame set frame_text = NULL where frame_text like '%unknown%'

--select E.dl_id
--, E.Event_TimeStampt
--,e.victimProcess
--,P.ProcessID
--,p.lockMode
--,p.hostname
--,p.inputbuf
--,p.isolationlevel
--,p.loginname
--,p.status
--from #tbl_process_list P
--JOIN #tbl_events E ON P.e_id = E.e_id order by 2 desc


select 
 E.dl_id
,p.p_id
,e.event_data
, E.Event_TimeStampt
,e.victimProcess
,P.ProcessID
,p.lockMode
,p.hostname
,COALESCE(f.frame_text,f.procname,p.inputbuf) [What_is_runnning]
,p.inputbuf
,f.procname
,f.frame_text
,p.isolationlevel
,p.loginname
,p.status
from #tbl_process_list P
JOIN #tbl_events E ON P.e_id = E.e_id
JOIN #tbl_process_frame F ON P.p_id = F.p_id
where 
1=1
AND (f.procname not in ('filtered')OR f.procname is null)
AND p.inputbuf not like '%filtered%'
AND p.inputbuf not like '%DistributorStores_Releases%' 
AND p.inputbuf not like '%@p6 int,@p7 bigint,@p0%'
AND p.inputbuf not like '%@p4 int,@p5 bigint,@p0%'
AND p.inputbuf not like '%@p3 int,@p4 bigint,@p0%'
AND p.inputbuf not like '%INSERT ![dbo!].![Tracks!]%' ESCAPE '!'
AND p.inputbuf not like '%INSERT ![dbo!].![Contacts!]%' ESCAPE '!'
AND p.inputbuf not like '%Proc ![Database Id = 13 Object Id = 402100473!]%' ESCAPE '!'
AND p.inputbuf not like '%![Images!]%' ESCAPE '!'
AND p.inputbuf not like '%![Artists!]%' ESCAPE '!'
AND (f.procname not like '%TR_DistributorStores_Releases_UPDATE_FirstDeliveryDate%' OR f.procname is null)
AND (f.procname not like '%SP_DeleteStatement%' OR f.procname is null)
AND (f.frame_text not like '%sp_CopyIndexes%' OR f.frame_text is null)
AND (f.procname not like '%sp_CopyIndexes%' OR f.procname is null)
AND (f.procname not like '%SP_SplitStatement%' OR f.procname is null)
AND (f.frame_text not like '%SP_SwitchOneTableData%' OR f.frame_text is null)
AND (f.frame_text not like '%sp_cci_tuple_mover%' OR f.frame_text is null)

order by 4 desc

/*
SELECT 
P.p_id
,p.ProcessID
,T.myFrame.value('(./@procname)[1]', 'varchar(120)') [procname]
,CAST(T.myFrame.value('(./@sqlhandle)[1]', 'varchar(max)')as varbinary(64)) [sqlhandle]
,T.myFrame.value('(.)[1]', 'varchar(max)') [frame_text]
,p.Q
from #tbl_process_list p
CROSS APPLY P.Q.nodes('/process/executionStack/frame') AS T(myFrame)
where p.p_id = 2

select * from #tbl_process_frame p 
where p.p_id = 2
and (p.procname not in ('filtered','adhoc') OR p.procname is null)

*/
