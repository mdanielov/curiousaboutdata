select 
A.index_id
,B.name [index_name]
,B.is_primary_key
,A.user_seeks
,A.user_scans
,A.user_lookups
,A.user_updates
,A.last_user_seek
,A.last_user_scan
,A.last_user_lookup
,A.last_user_update
,A.system_seeks
,A.system_scans
,A.system_lookups
,A.system_updates
,A.last_system_seek
,A.last_system_scan
,A.last_system_lookup
,A.last_system_update
from sys.dm_db_index_usage_stats A
JOIN sys.indexes B ON A.object_id = B.object_id AND A.index_id = B.index_id
where 
1=1 
AND A.database_id = DB_ID('my_db') 
AND A.object_id = object_id('my_table')
order by index_id