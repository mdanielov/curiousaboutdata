SELECT
SCHEMA_NAME,
digest,
digest_text,
round(sum_timer_wait/ 1000000000000, 6) `wait (s)`,
count_star
FROM performance_schema.events_statements_summary_by_digest
where
`DIGEST_TEXT` not like 'SET %'
AND `DIGEST_TEXT` not like 'SHOW %'
AND `DIGEST_TEXT` not like 'use %'
AND `DIGEST_TEXT` not like '%perfromance_schema%'
and `DIGEST_TEXT` not in ('COMMIT', 'START TRANSACTION')
ORDER BY count_star desc;