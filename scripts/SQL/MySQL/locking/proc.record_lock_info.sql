
DELIMITER //
CREATE PROCEDURE `record_lock_info` ( )
BEGIN
INSERT INTO `performance_watch`.`lock_watcher`
(
`trx_id`,
`trx_state`,
`trx_started`,
`trx_requested_lock_id`,
`trx_wait_started`,
`trx_weight`,
`trx_mysql_thread_id`,
`trx_query`,
`trx_operation_state`,
`trx_tables_in_use`,
`trx_tables_locked`,
`trx_lock_structs`,
`trx_lock_memory_bytes`,
`trx_rows_locked`,
`trx_rows_modified`,
`trx_concurrency_tickets`,
`trx_isolation_level`,
`trx_unique_checks`,
`trx_foreign_key_checks`,
`trx_last_foreign_key_error`,
`trx_adaptive_hash_latched`,
#`trx_adaptive_hash_timeout`,
`trx_is_read_only`,
`trx_autocommit_non_locking`)
select * from INFORMATION_SCHEMA.INNODB_TRX;

INSERT INTO `performance_watch`.`map_locks`
(`requesting_trx_id`,
`requested_lock_id`,
`blocking_trx_id`,
`blocking_lock_id`)
select * from INFORMATION_SCHEMA.INNODB_LOCK_WAITS;

END //

DELIMITER ; 