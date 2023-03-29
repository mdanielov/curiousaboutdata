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
INSERT #tbl_process_frame([p_id],[procname],[sqlhandle])
SELECT 
P.p_id
,T.myFrame.value('(./@procname)[1]', 'varchar(120)') [procname]
,T.myFrame.value('(./@sqlhandle)[1]', 'varbinary(64)') [sqlhandle]
from #tbl_process_list P
CROSS APPLY P.Q.nodes('/process/executionStack/frame') AS T(myFrame)

select E.dl_id
, E.Event_TimeStampt
,e.victimProcess
,P.* from #tbl_process_list P
JOIN #tbl_events E ON P.e_id = E.e_id
where E.Event_TimeStampt BETWEEN '2023-03-28 13:00:00' AND '2023-03-28 14:00:00'
