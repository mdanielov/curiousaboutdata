use performance_watch;

CREATE TABLE `map_locks` (
  `map_lock_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `record_date` datetime DEFAULT current_timestamp(),
  `requesting_trx_id` varchar(18) NOT NULL DEFAULT '',
  `requested_lock_id` varchar(81) NOT NULL DEFAULT '',
  `blocking_trx_id` varchar(18) NOT NULL DEFAULT '',
  `blocking_lock_id` varchar(81) NOT NULL DEFAULT '',
  PRIMARY KEY (`map_lock_id`)
) ENGINE=InnoDB ;

