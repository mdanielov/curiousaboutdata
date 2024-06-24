select round(( 100 * total_exec_time / sum(total_exec_time) over ())::numeric, 2) percent,
             round(total_exec_time::numeric, 2) as total,
             calls,
             round(mean_exec_time::numeric, 2) as mean,
			 round(max_exec_time::numeric, 2) as max,
             round(stddev_exec_time::numeric, 2) as stddev_exec_time,
             substring(query, 1, 40) as query
			 ,*
from pg_stat_statements where query like '%transport_id%';

--to reset stats:
--select pg_stat_statements_reset();
--if you need to set up this view:
--https://kaleman.netlify.app/getting-query-performance-stats-with-pg
