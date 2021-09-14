select distinct A.trx_id `blocker_ID`
,B.trx_id `requestor_ID`
,A.trx_rows_locked `rows_locked_by_blocker`
,B.trx_rows_locked `rows_locked_by_requester`
, A.trx_query  `blocker_query`
,B.trx_query `requestor_query`
from
map_locks M
JOIN lock_watcher A ON M.blocking_trx_id = A.trx_id
JOIN lock_watcher B ON M.requesting_trx_id = B.trx_id
where 1=1
# AND A.trx_query like 'insert%' OR B.trx_query like 'insert%'
AND A.trx_rows_locked > 0;