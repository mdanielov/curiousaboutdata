import boto3
import config_service as cs

def getClient(client_type):
    ret_client = boto3.client(
        client_type,
        aws_access_key_id=cs.config.get('AWS','ACCESS_KEY'),
        aws_secret_access_key=cs.config.get('AWS','SECRET_KEY'),
        region_name=cs.config.get('AWS','REGION')
        )

    return ret_client

def getDBInstances(b_client, filters=None):
    if filters:
        response =  b_client.describe_db_instances(Filters=filters)
    else:
        response = b_client.describe_db_instances()

    return response

def getMetricStats(
        b_client,
        InstanceID,
        MetricName,
        Namespace,
        StartTime,
        EndTime,
        Statistic,
        Period
        ):
    response = b_client.get_metric_statistics(
        Dimensions=[
            {
                'Name': 'DBInstanceIdentifier',
                'Value': InstanceID
            }],
        MetricName=MetricName,
        Namespace=Namespace,
        StartTime=StartTime,
        EndTime=EndTime,
        Statistics=Statistic,
        Period=Period)

    return response

def getPaginatedMetricDataByDateRange( b_client, metric_data_query, start_time, end_time):
    paginator = b_client.get_paginator('get_metric_data')
    operation_parameters = {
        'MetricDataQueries': metric_data_query,
        'StartTime':start_time,
        'EndTime':end_time,
        'ScanBy':'TimestampAscending',
        'PaginationConfig':{
            'MaxItems': 500,
            'PageSize': 500,
        }
    }
    response_iterator = paginator.paginate(**operation_parameters)
    return response_iterator

