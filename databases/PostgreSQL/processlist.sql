select * 
from pg_stat_activity 
where 1=1
and state is not null 
--and state not in ('idle')
and pid !=pg_backend_pid()
;