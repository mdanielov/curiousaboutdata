use master;

select 
[db_name]
,[file_type]
,sum([size])  [db_size (MB)]
FROM (
select d.[name] [db_name]
, CASE WHEN m.[type] = 1 THEN 'LOG'
WHEN m.[type] = 0 THEN 'DATA'
ELSE 'OTHER' END [file_type]
,m.size * 8.0 / 1024 [size]
from sys.master_files m JOIN sys.databases d ON d.database_id = m.database_id 
) A 
GROUP BY [db_name],[file_type]

order by 1
