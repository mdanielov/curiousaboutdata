import boto3
from datetime import datetime
# FOR DALC
import pymysql.cursors

#DALC settings
host = "127.0.0.1"
mysql_port = 3306
user = "laravel"
password = "laravel"
db_name = "aws_performance"

connection = pymysql.connect(host=host, port=int(mysql_port), user=user, password=password, database=db_name, charset='utf8mb4')
# END DALC settings

# region_name='us-east-1'
region_name='eu-west-1'
ec2 = boto3.client('ec2', region_name=region_name)
cloudwatch = boto3.client('cloudwatch', region_name=region_name)

# filters for instance information
filters = [{'Name':'tag:Type', 'Values':['Docker']}]

list_of_instances = []

#global variables for stats
Statistic = ['Maximum','Minimum']
Period = 60

def run_exec(qry_text):
    with connection.cursor() as cursor:
        cursor.execute(qry_text)
    connection.commit()

def run_query(qry_text):
    with connection.cursor() as cursor:
        cursor.execute(qry_text)
        return cursor.fetchall()

def getInstances(filters):
    response = ec2.describe_instances(Filters=filters)
    return response

def getInstanceStats(
        IstanceID,
        InstanceDesc,
        MetricName,
        Namespace,
        StartTime,
        EndTime,
        Statistic,
        Period
):
    response = cloudwatch.get_metric_statistics(
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': IstanceID
            }],
        MetricName=MetricName,
        Namespace=Namespace,
        StartTime=StartTime,
        EndTime=EndTime,
        Statistics=Statistic,
        Period=Period)

    for r in response["Datapoints"]:
        # save the data point to DB
        if MetricName == "CPUUtilization":
            qry_str = "INSERT INTO `aws_performance`.`AWS_stats`(" \
                      "`region`,`Instance_id`,`Instance_name`,`rec_time`,`CPU_MAX`,`CPU_MIN`) "\
                      "VALUES(\"{}\",\"{}\",\"{}\",\"{}\",{},{});".format(region_name
                                                                          ,IstanceID
                                                                          ,InstanceDesc
                                                                          ,r["Timestamp"].strftime("%Y-%m-%d %H:%M:%S")
                                                                          ,r["Maximum"]
                                                                          ,r["Minimum"])
        elif MetricName == "DiskWriteOps":
            qry_str = "INSERT INTO `aws_performance`.`AWS_stats`(" \
                      "`region`,`Instance_id`,`Instance_name`,`rec_time`,`IOPS_MAX`,`IOPS_MIN`) " \
                      "VALUES(\"{}\",\"{}\",\"{}\",\"{}\",{},{});".format(region_name
                                                                          , IstanceID
                                                                          , InstanceDesc
                                                                          , r["Timestamp"].strftime("%Y-%m-%d %H:%M:%S")
                                                                          , r["Maximum"]
                                                                          , r["Minimum"])
        else:
            qry_str = ""
            print(MetricName)
        run_exec(qry_str)

def main():
    response = getInstances(filters)
    for r in response['Reservations']:
        for i in r['Instances']:
            for t in i["Tags"]:
                if t.get("Key") == "Name":
                    InstanceName = t["Value"]
                else:
                    InstanceName = ""
        list_of_instances.append([{"InstanceId":i["InstanceId"]},{"InstanceName" : InstanceName}] )

    for insta in list_of_instances:
        InstanceID = insta[0].get("InstanceId")
        InstanceDesc = insta[1].get("InstanceName")
        getInstanceStats(InstanceID
                                      ,InstanceDesc
                                      ,"CPUUtilization"
                                      ,"AWS/EC2"
                                      ,"2020-07-05T2:18:00Z"
                                      ,"2020-07-05T18:18:00Z"
                                      ,Statistic
                                      ,Period)
        getInstanceStats(InstanceID
                                      ,InstanceDesc
                                      ,"DiskWriteOps"
                                      ,"AWS/EC2"
                                      ,"2020-07-05T2:18:00Z"
                                      ,"2020-07-05T18:18:00Z"
                                      , Statistic
                                      ,Period)


if __name__ == "__main__":
    main()
