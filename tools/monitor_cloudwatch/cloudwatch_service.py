import config_service as cs
import boto3_service as bs
import metric_repository as mr
import json

def getCloudWatchClient():
    return bs.getClient('cloudwatch')

def getRDSInstances( ):
    b_rds = bs.getClient('rds')
    DBInstanceFilter = json.loads(cs.config.get('PARMS','RDS_INSTANCE_FILTERS'))
    dbInstances = bs.getDBInstances(b_rds, DBInstanceFilter)

    return dbInstances

def processInstanceMetrics( b_client, instance, func):
    mr.insert_instance( instance, cs.config.get('AWS','REGION'), cs.config.get('AWS','INSTANCE_TYPE') )
    for metric in cs.config['METRICS']:
        if( int(cs.config.get('METRICS',metric)) == 1):
            func( b_client,
                instance,
                cs.config.get('AWS','INSTANCE_TYPE'),
                metric,
                cs.config.get('PARMS','DATE_FROM'),
                cs.config.get('PARMS','DATE_TO'),
                int(cs.config.get('PARMS','PERIOD'))
                )


def processInstanceMetricStatistics( b_client, instance, instance_type, metric, start_time, end_time, period):
    response = getMetricsStatsByDateRange( b_client, instance, instance_type, metric, start_time, end_time, period)
    processMetricsResponse( instance, response)

def getMetricsStatsByDateRange( b_client, instance, instance_type, metric, start_time, end_time, period):
    response = bs.getMetricStats(
        b_client,
        instance,
        metric,
        "AWS/"+instance_type,
        start_time,
        end_time,
        ['Maximum','Minimum'],
        period)

    return response

def processMetricsResponse( instance, response):
    metric = response["Label"]
    for datapoint in response["Datapoints"]:
        storeMetricStats( instance, metric, datapoint)
        printInstanceMetric(instance, metric, datapoint)

def storeMetricStats( instance, metric, datapoint):
    mr.insert_instance_metrics( instance
        , metric
        , datapoint["Maximum"]
        , datapoint["Minimum"]
        , datapoint["Unit"]
        , datapoint["Timestamp"]
        )

def printInstanceMetric( instance, metric, datapoint):
        print("{}] {} {} Max: {} Min: {} Units: {}".format(instance, metric, datapoint["Timestamp"], datapoint["Maximum"], datapoint["Minimum"], datapoint["Unit"]))


#----------------
# Pagination
#---------------
def processInstanceMetricData( b_client, instance, instance_type, metric, start_time, end_time, period):
    paginator = b_client.get_paginator('get_metric_data')
    metricDataQueries = getMetricDataQuery( instance, instance_type, metric, start_time, end_time, period)
    operation_parameters = {
        'MetricDataQueries': metricDataQueries,
        'StartTime':start_time,
        'EndTime':end_time,
        'ScanBy':'TimestampAscending',
        'PaginationConfig':{
            'MaxItems': 500,
            'PageSize': 500,
        }
    }
    response_iterator = paginator.paginate(**operation_parameters)
    processPaginatedMetricData( instance, metric, response_iterator)


def getMetricDataQuery( instance, instance_type, metric, start_time, end_time, period):
    statistics = ['Minimum', 'Maximum']
    metricDataQuery = [ \
        {
            'Id': metric.lower()+ stat, \
            'MetricStat': {\
                'Metric': {\
                    'Namespace': "AWS/"+instance_type,\
                    'MetricName': metric,\
                    'Dimensions': [{ 'Name': 'DBInstanceIdentifier', 'Value': instance } ]\
                },\
                'Period': period,\
                'Stat': stat\
            }\
        } for stat in statistics ]
    return metricDataQuery

def processPaginatedMetricData( instance, metric, response_iterator):
    for response in response_iterator:
        datapoints = processPaginateMetricsResponse( metric, response)
        for datapoint in datapoints:
            storeMetricStats( instance, metric, datapoint)
            printInstanceMetric(instance, metric, datapoint)

metricUnits = {
    "CPUUtilization": {"Units": "Percent"},
    "DatabaseConnections": {"Units": "Count"},
    "DiskQueueDepth": {"Units": "Count"},
    "FreeableMemory": {"Units": "Bytes"},
    "FreeStorageSpace": {"Units": "Bytes"},
    "ReadIOPS": {"Units": "Count/Second"},
    "WriteIOPS": {"Units": "Count/Second"},
    "ReadLatency": {"Units": "Seconds"},
    "WriteLatency": {"Units": "Seconds"},
    "DDLLatency": {"Units": "Count/Second"},
    "SelectLatency": {"Units": "Milliseconds"},
    "InsertLatency": {"Units": "Milliseconds"},
    "DeleteLatency": {"Units": "Milliseconds"},
    "UpdateLatency": {"Units": "Milliseconds"},
    "Deadlocks": {"Units": "Count/Second"},
    "BufferCacheHitRatio": {"Units": "Percent"},
    "Queries": {"Units": "Count/Second"},
    "ReplicaLag": {"Units": "Seconds"}
}

def processPaginateMetricsResponse( metric, response):
    datapointMax = response['MetricDataResults'][0]
    datapointMin = response['MetricDataResults'][1]
    datapoint = [ { 'Timestamp': datapointMax['Timestamps'][idx], \
        'Maximum': maxval, \
        'Minimum': datapointMin['Values'][idx], \
        'Unit': metricUnits[metric]['Units'] \
        } for idx, maxval in enumerate(datapointMax['Values'])]

    return datapoint

#.strftime("%Y-%m-%d %H:%M:%S.%f")
