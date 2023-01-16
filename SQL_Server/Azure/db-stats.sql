select 
dtu_limit
,cpu_limit
,primary_group_max_io
,primary_group_max_io
,pool_max_io
,slo_name
,CAST(max_db_memory/1024.0/1024  as decimal (20,2)) max_db_memory
from sys.dm_user_db_resource_governance 
