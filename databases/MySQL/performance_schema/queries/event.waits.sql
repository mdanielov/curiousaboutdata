use performance_schema;
select 
THREAD_ID	#Thread associated with the event. Together with EVENT_ID uniquely identifies the row.
,EVENT_ID	#Thread's current event number at the start of the event. Together with THREAD_ID uniquely identifies the row.
,END_EVENT_ID	#NULL when the event starts, set to the thread's current event number at the end of the event.
,EVENT_NAME	#Event instrument name and a NAME from the setup_instruments table
,SOURCE	#Name and line number of the source file containing the instrumented code that produced the event.
,TIMER_START/1000000000.0 `TIMER_START_ms`	#Value in picoseconds when the event timing started or NULL if timing is not collected.
,TIMER_END/1000000000.0	`TIMER_END_ms` #Value in picoseconds when the event timing ended, or NULL if the event has not ended or timing is not collected.
,TIMER_WAIT/1000000000.0 `TIMER_WAIT_ms`	#Value in picoseconds of the event's duration or NULL if the event has not ended or timing is not collected.
,SPINS	#Number of spin rounds for a mutex, or NULL if spin rounds are not used, or spinning is not instrumented.
,OBJECT_SCHEMA	#Name of the schema that contains the table for table I/O objects, otherwise NULL for file I/O and synchronization objects.
,OBJECT_NAME	#File name for file I/O objects, table name for table I/O objects, the socket's IP:PORT value for a socket object or NULL for a synchronization object.
,OBJECT_TYPE	#FILE for a file object, TABLE or TEMPORARY TABLE for a table object, or NULL for a synchronization object.
,OBJECT_INSTANCE_BEGIN	#Address in memory of the object.
,INDEX_NAME	#Name of the index, PRIMARY for the primary key, or NULL for no index used.
,NESTING_EVENT_ID	#EVENT_ID of event within which this event nests.
,NESTING_EVENT_TYPE	#Nesting event type. Either statement, stage or wait.
,OPERATION	#Operation type, for example read, write or lock
,NUMBER_OF_BYTES	#Number of bytes that the operation read or wrote, or NULL for table I/O waits.
,FLAGS
 from events_waits_current WHERE EVENT_NAME NOT IN ('idle','wait/io/file/innodb/innodb_data_file','wait/io/file/innodb/innodb_log_file');