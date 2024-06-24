select P.*
,T.myFrame.value('(./@procname)[1]', 'varchar(120)') [procname]
,T.myFrame.value('(./@sqlhandle)[1]', 'varchar(max)') [sqlhandle]
FROM (
select
E.report_id
,E.Event_TimeStampt
,E.event_data
,E.[database_name]
,E.[deadlock_cycle_id]
,E.[server_name]
,T.myProcess.value('(./@id)[1]', 'varchar(200)') [ProcessID]
,T.myProcess.value('(./@waitresource)[1]', 'varchar(600)') [waitresource]
,T.myProcess.value('(./@lockMode)[1]', 'varchar(60)') [lockMode]
,T.myProcess.value('(./@hostname)[1]', 'varchar(120)') [hostname]
,T.myProcess.value('(./inputbuf)[1]', 'varchar(max)') [inputbuf]
,T.myProcess.value('(./@isolationlevel)[1]', 'varchar(60)') [isolationlevel]
,T.myProcess.value('(./@loginname)[1]', 'varchar(60)') [loginname]
,T.myProcess.value('(./@status)[1]', 'varchar(60)') [status]
,T.myProcess.query('.') Q
from (
select
base.report_id
,T.myEvent.value('(@timestamp)[1]', 'datetime2') AS Event_TimeStampt
,base.event_data
,T.myEvent.value('(./data[@name="deadlock_cycle_id"]/value)[1]', 'INT') [deadlock_cycle_id]
,T.myEvent.value('(./data[@name="server_name"]/value)[1]', 'sysname') AS [server_name]
,T.myEvent.value('(./data[@name="database_name"]/value)[1]', 'sysname') AS [database_name]
,T.myEvent.query('./data/value/deadlock') as dead_frg
FROM (
				select top 5 ROW_NUMBER() OVER (order by timestamp_utc desc) as [report_id]
				,CAST(event_data as XML) event_data
				FROM sys.fn_xe_telemetry_blob_target_read_file('dl', NULL, NULL, NULL)
				WHERE object_name = 'database_xml_deadlock_report'
) base
CROSS APPLY base.event_data.nodes('/event') AS T(myEvent)
) E
CROSS APPLY E.dead_frg.nodes('/deadlock/process-list/process') AS T(myProcess)
) P
CROSS APPLY P.Q.nodes('/process/executionStack/frame') AS T(myFrame)