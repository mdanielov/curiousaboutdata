# 
import db_layer as db

def insert_instance( instance, region, instance_type):
    sql = """
    INSERT IGNORE INTO instance( instance_id, region, instance_type)
    VALUES( ?, ?, ?);
"""
    db.execute( sql, [instance, region, instance_type])
    return

def insert_instance_metrics( instance, metric_name, max_value, min_value, unit, rec_time):
    sql = """
    INSERT INTO instance_metrics( instance_id, metric_name, max_value, min_value, unit, rec_time)
    SELECT ?, ?, ?, ?, ?, ?
    WHERE NOT EXISTS (SELECT 1 FROM instance_metrics WHERE instance_id = ? AND metric_name = ? AND rec_time = ?)
"""
    timestamp = rec_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    db.execute( sql, [instance, metric_name, max_value, min_value, unit, timestamp, instance, metric_name, timestamp])
    return

def get_instance_metrics_by_instance_metric( instance, metric_name):
    sql = """
    SELECT instance_id
        , metric_name
        , max_value
        , min_value
        , unit
        , rec_time
    FROM instance_metrics
    WHERE instance_id = %s AND metric_name = %s
"""
    return db.fetchall( sql, [instance, metric_name])
