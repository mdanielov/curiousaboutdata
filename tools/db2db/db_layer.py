# mssql_db_layer
#
# DB Layer for SQLAlchemy
# ------------------------
import os
import sys
import re
from pandas import DataFrame
import pandas.io.sql as pdsql
import sqlalchemy as sa
from sqlalchemy.sql import text
from sqlalchemy.exc import ProgrammingError
import psycopg2
import logging
from configparser import ConfigParser

config = ConfigParser()



conn = None
engine = None

# get the db connection elements into a dictionary based on an sqlalchemey string
def connection_dict_form_1(conn_string):
    conn_string_pattern_1 = r"(.+?)://(.+?)/(.+?)\?driver=(.+)"
    m = re.match(conn_string_pattern_1, conn_string)
    retval = None
    if m is not None:
        retval = {"dbtype": m[1], "host": m[2], "dbname": m[3]}
    return retval


def connection_dict_form_2(conn_string):
    conn_string_pattern_2 = r"(.+?)://(.+?):(.+?)@(.+?):(\d+)/(.+)$"
    retval = None
    m = re.match(conn_string_pattern_2, conn_string)
    if m is not None:
        retval = {
            "dbtype": m[1],
            "host": m[4],
            "port": m[5],
            "dbname": m[6],
            "user": m[2],
            "password": m[3],
        }
    return retval


def connection_dict_form_3(conn_string):
    conn_string_pattern_3 = r"(.+?)://(.+?):(.+?)@(.+?)/(.+)$"
    retval = None
    m = re.match(conn_string_pattern_3, conn_string)
    if m is not None:
        retval = {
            "dbtype": m[1],
            "host": m[4],
            "dbname": m[5],
            "user": m[2],
            "password": m[3],
        }
    return retval


def get_connection_dict():
    funcs = (connection_dict_form_1, connection_dict_form_2, connection_dict_form_3)
    config.read('./settings.ini')
    get_settings = config["settings"]
    conn_string = get_settings["CONNECTION_STRING"]
    if conn_string is not None:
        for func in funcs:
            ret_dict = func(conn_string)
            if ret_dict is not None:
                return ret_dict
    return {}


def get_dbtype():
    connection_dict = get_connection_dict()
    return connection_dict.get("dbtype", None)


# ---------------------------
# Called once in the script
# ---------------------------


def get_connection(connString=None):
    global conn
    if not conn:
        if connString is None:
            config.read('./settings.ini')
            get_settings = config["settings"]
            connString = get_settings["CONNECTION_STRING"]#os.getenv("CONNECTION_STRING")
        if connString is None or connString == "":
            raise NameError("Connection string does not exist.")
        try:
            engine = sa.create_engine(connString).execution_options(autocommit=True)
            conn = engine.connect()
        except Exception as e:
            raise e

    return conn

def get_engine(connString=None):
    global engine
    if connString is None:
        config.read('./settings.ini')
        get_settings = config["settings"]
        connString = get_settings['CONNECTION_STRING']#os.getenv("CONNECTION_STRING")
    if connString is None or connString == "":
        raise NameError("Connection string does not exist.")
    try:
        if engine is None:
            engine = sa.create_engine(connString)#.execution_options(autocommit=True)
    except Exception as ex:
        raise ex
    return engine


# ---------------------
# Base functionality
# ---------------------
def conn_execute(conn, sql, args=None):
    result = None
    try:
        if args is None:
            conn.execute(sql)
        else:
            conn.execute(sql, args)
        conn.commit()
    except Exception as ex:
        conn.rollback()
        logging.error(repr(ex))
        raise ex
    finally:
        return result


def conn_read_sql_query(conn, sql, args=None):
    if args is None:
        df = pdsql.read_sql_query(sql, conn)
    else:
        sql_params = args if isinstance(args, list) else [args]
        df = pdsql.read_sql_query(sql, conn, params=sql_params)
    return df


def conn_fetchall(conn, sql, args=None):
    try:
        if args is None:
            retval = pdsql.read_sql(sql, conn)
        else:
            sql_params = args if isinstance(args, list) else [args]
            retval = pdsql.read_sql(sql, conn, params=sql_params)
        return retval
    except Exception as ex:
        logging.error(sys.exc_info()[1])
        raise ex


def conn_fetchone(conn, sql, args=None):
    df = conn_fetchall(conn, sql, args)
    return df.iloc[0] if len(df.index) > 0 else df.head()


def conn_df_to_sql(conn, obj_data, table_name, schema, if_exists="append", args=None):
    df = DataFrame(obj_data)
    df.index = df.index + 1
    df.to_sql(
        name=table_name,
        con=conn,
        schema=schema,
        if_exists=if_exists,
        index=True,
        index_label="id",
        method=None,
    )


def conn_does_exist(sql, args=None):
    try:
        res = conn.execute(sql).one() if args is None else conn.execute(sql, args).one()
        return res[0] == 1 if len(res) > 0 else False
    except Exception as ex:
        logging.error(sys.exc_info()[1])
        raise ex


def conn_read_and_run(conn, filename):
    retval = False
    with open(filename, mode="r", encoding="utf-8") as fp:
        sql = text(fp.read())
    if sql is not None:
        try:
            retval = conn.execute(sql)
            conn.commit()
        except ProgrammingError as pex:
            conn.rollback()
            logging.info( pex.orig)
        except Exception as ex:
            conn.rollback()
            retval = False            
            raise ex
        return retval


# -------------------------------


def db_globalconnector(func):
    def with_connection_(*args, **kwargs):
        global conn
        return func(conn, *args, **kwargs)

    return with_connection_


@db_globalconnector
def execute(conn, sql, args=None):
    return conn_execute( conn, sql, args)

@db_globalconnector
def read_sql_query(conn, sql, args=None):
    if args is None:
        df = pdsql.read_sql_query(sql, conn)
    else:
        sql_params = args if isinstance(args, list) else [args]
        df = pdsql.read_sql_query(sql, conn, params=sql_params)
    return df


@db_globalconnector
def fetchall(conn, sql, args=None):
    return conn_fetchall(conn, sql, args)


@db_globalconnector
def fetchone(conn, sql, args=None):
    return conn_fetchone(conn, sql, args)


@db_globalconnector
def df_to_sql(conn, obj_data, table_name, schema, if_exists="append", args=None):
    return conn_df_to_sql(conn, obj_data, table_name, schema, if_exists, args)


@db_globalconnector
def read_and_run(conn, filename):
    return conn_read_and_run(conn, filename)


def does_exist(conn, sql, args=None):
    return conn_does_exist(conn, sql, args)


##########################
# db connection wrappers
##########################
def db_connector(func):
    def with_connection_(*args, **kwargs):
        conn = None
        connString = os.getenv("CONNECTION_STRING")
        if connString is None or connString == "":
            raise NameError("Connection string does not exist.")
        try:
            engine = sa.create_engine(connString)
            with engine.connect() as conn:
                return func(conn, *args, **kwargs)
        except Exception as e:
            raise e
        finally:
            if not conn.closed:
                logging.info("close connection")
                conn.close()

    return with_connection_


@db_connector
def db_df_to_sql(conn, obj_data, table_name, schema, if_exists="append", args=None):
    conn_df_to_sql(conn, obj_data, table_name, schema, if_exists, args)


# @db_connector
# def get_sql_data_source_name( conn, arg=None, arg2=None):
#     return conn.getinfo(pyodbc.SQL_DATA_SOURCE_NAME)


def does_table_exist(conn, table_name) -> bool:
    sql = "SELECT COUNT(name) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = ?"
    res = conn.execute(sql, [(table_name)]).one()
    return res[0] == 1 if len(res) > 0 else False


@db_connector
def db_read_sql_query(conn, sql, args=None):
    return conn_read_sql_query(conn, sql, args)


@db_connector
def db_fetchall(conn, sql, args=None):
    return conn_fetchall(conn, sql, args)


@db_connector
def db_fetchone(conn, sql, args=None):
    return conn_fetchone(conn, sql, args)


@db_connector
def db_execute(conn, sql, args=None):
    return conn_execute(conn, sql, args)


@db_connector
def db_does_exist(conn, sql, args=None):
    return conn_does_exist(conn, sql, args)


@db_connector
def db_read_and_run(conn, filename):
    read_and_run(conn, filename)


# -----------------------------
# read a sql file and execute
# -----------------------------


# ---------------------
# Postgresql Execute
# ---------------------
def pg_connect():
    conn_dict = get_connection_dict()
    conn = psycopg2.connect(
        host=conn_dict.get("host", "localhost"),
        port=conn_dict.get("port", "5432"),
        dbname=conn_dict.get("dbname", "postgres"),
        user=conn_dict.get("user", "postgres"),
        password=conn_dict.get("password"),
    )
    return conn


def pg_execute(sql):
    conn = pg_connect()
    with conn.cursor() as cursor:
        cursor.execute(sql)
        conn.commit()
    conn.close()
