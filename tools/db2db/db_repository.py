import pandas as pd
import db_layer as db
import logging
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import inspect, MetaData, Text
from sqlalchemy.sql.ddl import CreateTable, DDL
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects import mssql

import re

class dbSQL:
    @staticmethod
    def get_dbconfig():
        return db.get_connection_dict()

    @staticmethod
    def get_connection():
        return db.get_connection()
    
    @classmethod
    def disable_constraints(cls):
        pass

    @classmethod
    def enable_constraints(cls):
        pass

    @staticmethod
    def fetch_table_data( table_name: str, rowlimit: int = None)-> pd.DataFrame:
        pass

    @staticmethod
    def get_table_column_names(table_name):
        inspector = inspect( db.get_engine())
        columns = inspector.get_columns(table_name)
        table_columns = [ col.get('name') for col in columns if 'computed' not in col]
        return table_columns

    @staticmethod
    def get_select_all_column_statement(table_name, row_limit=0):
        cols = dbSQL.get_table_column_names( table_name)
        sql = "SELECT "
        sql += ','.join( cols)
        sql += f" FROM {table_name}"
        if row_limit > 0: sql += f" LIMIT {row_limit}"
        return sql

    @classmethod
    def fetch_and_write_in_chunks( cls, table_name: str, callback, row_limit: int = 0, chunk_size: int = 1000)-> int:
        engine = db.get_engine()
        # sql = f"SELECT * FROM {table_name}"
        # Read data from the database in chunks
        sql = cls.get_select_all_column_statement(table_name, row_limit)
        reader = pd.read_sql(sql, con=engine, chunksize=chunk_size)
        # Iterate over the chunks and write to files in chunks
        file_counter = 1
        for df_chunk in reader:
            callback( table_name, df_chunk, file_counter, chunk_size)
            file_counter += 1
        # Close the SQLAlchemy engine
        engine.dispose()
        return file_counter

    @staticmethod
    def xget_table_names( pattern:str = None):
        sql = " SELECT CONCAT(TABLE_SCHEMA, '.', TABLE_NAME) AS table_name FROM INFORMATION_SCHEMA.tables WHERE TABLE_TYPE = 'BASE TABLE' "
        sql += f"AND TABLE_NAME LIKE '{pattern}%%'" if pattern is not None else ""
        df = db.db_fetchall(sql)
        return df['table_name'].values.tolist() if df is not None else []
    
    def get_table_names( pattern: str = None) -> list:
        inspector = inspect( db.get_engine())
        tables = inspector.get_table_names()
        retval = [ table for table in tables if pattern is None or re.match( pattern, table, re.IGNORECASE)]
        return retval

    @staticmethod
    def columns_intersect_map( df_columns, table_columns, table_name) -> dict:
        # Convert lists to lowercase
        lowercase_table_cols = [col.lower() for col in table_columns]
        lowercase_df_cols = [col.lower() for col in df_columns]
        # Find the intersection in a case-insensitive manner
        intersection = set(lowercase_table_cols) & set(lowercase_df_cols)
        # Convert the intersection back to the original case
        intersection_map_table_cols = {item.lower() : item for item in table_columns if item.lower() in intersection }
        for df_col in df_columns:
            if intersection_map_table_cols.get(df_col.lower()) is None:
                logging.info( f"{table_name}: column '{df_col}' not found!")
        mapping_cols = { df_col: intersection_map_table_cols.get(df_col.lower()) for df_col in df_columns if intersection_map_table_cols.get(df_col.lower()) is not None}
        return mapping_cols

    @classmethod
    def rename_columns( cls, df, table_name):
        table_columns = dbSQL.get_table_column_names(table_name)
        columns_map = dbSQL.columns_intersect_map( df.columns.tolist(), table_columns, table_name)
        columns_to_rename = { k:v for k,v in columns_map.items() if k != v }
        df.rename( columns=columns_to_rename, inplace=True)
        return df[columns_map.values()]

    @staticmethod
    def make_df_compatible_with_db(engine, df: pd.DataFrame, table_name: str) -> pd.DataFrame:
        return dbSQL.rename_columns( df, table_name)

    @classmethod
    def insert_into_table( cls,df:pd.DataFrame, table_name:str):
        rows_inserted = 0
        conn = db.get_connection()
        conn.autocommit = True
        dfInsert = dbSQL.make_df_compatible_with_db( conn.engine, df, table_name)
        try:
            cls.disable_constraints()
            #engine = db.get_engine()
            dfInsert.to_sql(table_name, conn, if_exists='append',index=False) 
            rows_inserted = len(dfInsert)
            cls.enable_constraints()
            conn.commit()
        except ProgrammingError as pe:
 #           conn.rollback();
            logging.error( 'ProgrammingError ' + str(pe))
        except Exception as ex:
#            conn.rollback()
            logging.error( repr(ex))
        if rows_inserted > 0:
            logging.info( f"write_to_table '{table_name}': {rows_inserted} rows")

    @staticmethod
    def copy_csv_file_to_table( filename: str, table_name: str):
        logging.error('copy_csv_file_to_table - parent class')
        pass

    @staticmethod
    def get_row_count( table_name: str)->pd.DataFrame:
        row_count = -1
        sql = f"SELECT COUNT(*) as ROW_COUNT FROM {table_name};"
        try:
            df = db.db_fetchone(sql)
            return df['row_count'] if df is not None else -1
        except ProgrammingError as pex:
            logging.info(f"Table '{table_name}' does not exist.")
        except Exception as ex:
            logging.error(repr(ex))
        return row_count

    @staticmethod
    def truncate_table( table_name:str):
        sql = "TRUNCATE TABLE {table_name};"
        df = db.db_execute(sql)
        return table_name

    @staticmethod
    def bcp_out(table_name: str, filename: str, dbconfig: dict, rowlimit: str = None):
        pass

    @staticmethod
    def get_meta_data():
        engine = db.get_engine()
        metadata = MetaData()
        metadata.reflect(bind=engine)
        return metadata

    @staticmethod
    def get_table_scripts( pattern, callback):
        engine = db.get_engine()
        metadata = MetaData()
        metadata.reflect(bind=engine)
        for table in metadata.tables:
            if re.match( pattern, table):
                tbl = metadata.tables[table]
                if callback is not None:
                    callback(tbl)

    @staticmethod
    def create_table_script_with_dialect( dialect, metadata, table_name, callback):
        tbl = CreateTable(metadata.tables[table_name])
        sql = tbl.compile( dialect=dialect).statement

        if callback is not None:
            callback( table_name, str(sql))
        return str(sql)

    @staticmethod
    def create_index_script_with_dialect( dialect, metadata, table_name, callback):
        engine = db.get_engine()
        sql = ""
        for index in metadata.tables[table_name].indexes:
            ddl = DDL(index.name)
            sql = ddl.compile(dialect=dialect)
            if callback is not None:
                callback( index.name, str(sql))
        return sql

    @staticmethod
    def read_and_run( filename):
        return db.read_and_run(filename)