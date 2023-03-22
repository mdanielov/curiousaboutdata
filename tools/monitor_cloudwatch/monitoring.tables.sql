use aws_performance;

SET foreign_key_checks = 0;
DROP TABLE IF EXISTS `instance_metrics`;
SET foreign_key_checks = 1;
DROP TABLE IF EXISTS `instance`;

CREATE TABLE `instance` (
`instance_id` varchar(60) NOT NULL
, `region` varchar(20) NOT NULL
, `instance_type` varchar (60) NOT NULL # RDS or EC2
, PRIMARY KEY (instance_Id)
) ENGINE=InnoDB;

CREATE TABLE `instance_metrics` (
`metric_id` BIGINT NOT NULL AUTO_INCREMENT
,`instance_id` varchar(60)
,`metric_name` varchar(120)
,`max_value` decimal(36,2)
,`min_value` decimal(36,2)
,`unit` varchar(60)
,`rec_time` datetime
,PRIMARY KEY(`metric_id`)
,FOREIGN KEY (`instance_id`) REFERENCES instance(`instance_id`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `metric_units`;

CREATE TABLE `metric_units` (
`id` INT NOT NULL AUTO_INCREMENT
,`metric_name` varchar(120)
,`units` varchar(60)
,PRIMARY KEY(`id`)
) ENGINE=InnoDB;

INSERT INTO `metric_units`( metric_name, units)
VALUES
    ( 'CPUUtilization', 'Percent'),
    ( 'DatabaseConnections', 'Count'),
    ( 'DiskQueueDepth', 'Count'),
    ( 'FreeableMemory', 'Bytes'),
    ( 'FreeStorageSpace', 'Bytes'),
    ( 'ReadIOPS', 'Count/Second'),
    ( 'WriteIOPS', 'Count/Second'),
    ( 'ReadLatency', 'Seconds'),
    ( 'WriteLatency', 'Seconds'),
    ( 'DDLLatency', 'Count/Second'),
    ( 'SelectLatency', 'Milliseconds'),
    ( 'InsertLatency', 'Milliseconds'),
    ( 'DeleteLatency', 'Milliseconds'),
    ( 'UpdateLatency', 'Milliseconds'),
    ( 'Deadlocks', 'Count/Second'),
    ( 'BufferCacheHitRatio', 'Percent'),
    ( 'Queries', 'Count/Second')
;
