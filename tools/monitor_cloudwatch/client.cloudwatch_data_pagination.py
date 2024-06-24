import cloudwatch_service as cs

b_cloudwatch = cs.getCloudWatchClient()
db_rds_instances = cs.getRDSInstances()
for dbInstance in db_rds_instances['DBInstances']:
    cs.processInstanceMetrics( b_cloudwatch, dbInstance['DBInstanceIdentifier'], cs.processInstanceMetricData)
