import pyodbc
import pandas.io.sql as pdsql


# mssql_db_layer
#
# DB Layer for MSSQL
#------------------------
import os
import sys

def db_connector( func):
    def with_connection_(*args, **kwargs):
        conn = None
        connString = os.getenv('CONNECTION_STRING')
        if connString is None or connString == "":
            raise NameError("Connection string does not exist.")
        try:
            conn=pyodbc.connect( connString)
            return func( conn, *args, **kwargs)
        except Exception as e:
            print( sys.exc_info()[1])
            raise e
        finally:
            if conn:
                conn.close()
    return with_connection_
  
@db_connector
def execute(conn, sql, args=None):
    try:
        curs = conn.cursor()
        if args is None:
            curs.execute( sql)
        else:
            curs.execute( sql, args)
        conn.commit()
    except Exception as ex:
        print( sys.exc_info()[1])
        raise ex

@db_connector
def fetchall(conn, sql, args=None):
    if args is None:
        return pdsql.read_sql( sql, conn)
    sql_params = args if isinstance(args, list) else [args]
    try:
        return  pdsql.read_sql( sql, conn, params=sql_params)
    except Exception as ex:
        print( sys.exc_info()[1])
        raise ex
