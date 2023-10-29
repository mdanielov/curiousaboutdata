--server memory
select
(physical_memory_in_use_kb/1024) as [Memory_usedby_Sqlserver_MB]
,(locked_page_allocations_kb/1024 )as [Locked_pages_used_Sqlserver_MB]
,(total_virtual_address_space_kb/1024 )as [Total_VAS_in_MB]
,process_physical_memory_low
,process_virtual_memory_low
from sys. dm_os_process_memory