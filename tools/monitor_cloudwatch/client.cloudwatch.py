import boto3

import os
import datetime
import configparser
import json

import metric_repository as mr

config=configparser.RawConfigParser()
config.optionxform=str
config.read( 'settings.ini')
os.environ['CONNECTION_STRING'] = config['DATABASE']['CONNECTION_STRING']
# ACCESS_KEY=r"access_key"
# SECRET_KEY=r"secret_key"

# region_name="us-east-1"

def getClient(client_type):
    ret_client = boto3.client(
        client_type,
        aws_access_key_id=config['AWS']['ACCESS_KEY'],
        aws_secret_access_key=config['AWS']['SECRET_KEY'],
        region_name=config['AWS']['REGION']
        )

    return ret_client

def getDBInstances(b_client, filters=None):
    if filters:
        response =  b_client.describe_db_instances(Filters=[filters])
    else:
        response = b_client.describe_db_instances()
    return response


def getEC2Instances(b_client, *filters):
    if filters:
        # response =  b_client.describe_instances(Filters=filters)
        instanceIDs = filters[0]["InstanceIds"].split(",")
        response =  b_client.describe_instances(InstanceIds = instanceIDs)
        # response =  b_client.describe_instances(InstanceIds=["i-0669e2050f31f1364",])
    else:
        response = b_client.describe_instances()
    return response


def processInstance( b_client, instance):
    mr.insert_instance( instance, config['AWS']['REGION'], config['AWS']['INSTANCE_TYPE'] )
    for metric in config['METRICS']:
        if( int(config['METRICS'][metric]) == 1):
            processInstanceMetric( b_client,
                instance,
                config['AWS']['INSTANCE_TYPE'],
                metric,
                config['PARMS']['DATE_FROM'],
                config['PARMS']['DATE_TO'],
                int(config['PARMS']['PERIOD']),
                config['AWS']['INSTANCE_TYPE']
                )

def processInstanceMetric( b_client, instance, instance_type, metric, start_time, end_time, period, itype):
    response = getMetricsStatsByDateRange( b_client, instance, instance_type, metric, start_time, end_time, period,itype)
    processMetricsResponse( instance, response)

def getMetricsStatsByDateRange( b_client, instance, instance_type, metric_name, start_time, end_time, period, itype):
    response = getMetricStats(
        b_client,
        instance,
        metric_name,
        "AWS/"+instance_type,
        start_time,
        end_time,
        ['Maximum','Minimum'],
        period
        , itype)

    return response

def getMetricStats(
        b_client,
        InstanceID,
        MetricName,
        Namespace,
        StartTime,
        EndTime,
        Statistic,
        Period,
        itype
        ):
    if itype == "rds":
        filter = [
            {
                'Name': 'DBInstanceIdentifier',
                'Value': InstanceID
            }]
    elif itype == "EC2":
        filter = [
                {
                    'Name': 'InstanceId',
                    'Value': InstanceID
                }]
    else:
        print("Unknown instance type: {}".format(itype))

    response = b_client.get_metric_statistics(
        Dimensions=filter,
        MetricName=MetricName,
        Namespace=Namespace,
        StartTime=StartTime,
        EndTime=EndTime,
        Statistics=Statistic,
        Period=Period)

    return response

def processMetricsResponse( instance, response):
    metric = response["Label"]
    for datapoint in response["Datapoints"]:
        storeMetricStats( instance, metric, datapoint)
        print("{} {} {} {} {}".format(metric, datapoint["Timestamp"], datapoint["Maximum"], datapoint["Minimum"], datapoint["Unit"]))

def storeMetricStats( instance, metric, datapoint):
    mr.insert_instance_metrics( instance
        , metric
        , datapoint["Maximum"]
        , datapoint["Minimum"]
        , datapoint["Unit"]
        , datapoint["Timestamp"]
        )

def main():
    i_type = "ec2"
    b_cloudwatch = getClient('cloudwatch')
    b_instance = getClient(i_type)
    if i_type == "ec2":
        processEC2(b_instance, b_cloudwatch)
    elif i_type == "rds":
        processRDS(b_instance, b_cloudwatch)
    else:
        print("Unknown instance type: {}".format(i_type))

def processRDS(b_rds, b_cloudwatch):
    DBInstanceFilter = json.loads(config['PARMS']['RDS_INSTANCE_FILTERS'])
    dbInstances = getDBInstances(b_rds, DBInstanceFilter)
    for dbInstance in dbInstances['DBInstances']:
        processInstance( b_cloudwatch, dbInstance['DBInstanceIdentifier'])  

def processEC2(b_ec2, b_cloudwatch):
    ec2InstanceFilter = config['PARMS']['EC2_INSTANCE_FILTERS']
    Ec2args = dict(e.split('=') for e in ec2InstanceFilter.split(', '))
    ec2Instances = getEC2Instances(b_ec2, Ec2args)
    for r in ec2Instances['Reservations']:
        for ec2Instance in r['Instances']:
            processInstance( b_cloudwatch, ec2Instance['InstanceId'])   
                        

if __name__ == "__main__":
    main()