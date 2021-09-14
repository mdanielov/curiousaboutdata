create database performance_watch;
use performance_watch;
CREATE TABLE `lock_watcher` (
  `watcher_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `record_date` datetime DEFAULT current_timestamp(),
  `trx_id` varchar(18) NOT NULL DEFAULT '',
  `trx_state` varchar(13) NOT NULL DEFAULT '',
  `trx_started` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `trx_requested_lock_id` varchar(81) DEFAULT NULL,
  `trx_wait_started` datetime DEFAULT NULL,
  `trx_weight` bigint(21) unsigned NOT NULL DEFAULT 0,
  `trx_mysql_thread_id` bigint(21) unsigned NOT NULL DEFAULT 0,
  `trx_query` varchar(1024) DEFAULT NULL,
  `trx_operation_state` varchar(64) DEFAULT NULL,
  `trx_tables_in_use` bigint(21) unsigned NOT NULL DEFAULT 0,
  `trx_tables_locked` bigint(21) unsigned NOT NULL DEFAULT 0,
  `trx_lock_structs` bigint(21) unsigned NOT NULL DEFAULT 0,
  `trx_lock_memory_bytes` bigint(21) unsigned NOT NULL DEFAULT 0,
  `trx_rows_locked` bigint(21) unsigned NOT NULL DEFAULT 0,
  `trx_rows_modified` bigint(21) unsigned NOT NULL DEFAULT 0,
  `trx_concurrency_tickets` bigint(21) unsigned NOT NULL DEFAULT 0,
  `trx_isolation_level` varchar(16) NOT NULL DEFAULT '',
  `trx_unique_checks` int(1) NOT NULL DEFAULT 0,
  `trx_foreign_key_checks` int(1) NOT NULL DEFAULT 0,
  `trx_last_foreign_key_error` varchar(256) DEFAULT NULL,
  `trx_adaptive_hash_latched` INT(1) NULL,
  `trx_is_read_only` int(1) NOT NULL DEFAULT 0,
  `trx_autocommit_non_locking` int(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`watcher_id`)
) ENGINE=InnoDB;

CREATE TABLE `map_locks` (
  `map_lock_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `record_date` datetime DEFAULT current_timestamp(),
  `requesting_trx_id` varchar(18) NOT NULL DEFAULT '',
  `requested_lock_id` varchar(81) NOT NULL DEFAULT '',
  `blocking_trx_id` varchar(18) NOT NULL DEFAULT '',
  `blocking_lock_id` varchar(81) NOT NULL DEFAULT '',
  PRIMARY KEY (`map_lock_id`)
) ENGINE=InnoDB ;


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

CREATE  EVENT `record_locks` ON SCHEDULE EVERY 15 SECOND DISABLE DO call record_lock_info();
alter event record_locks enable;
    