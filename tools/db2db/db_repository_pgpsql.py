from pandas import DataFrame
from sqlalchemy import Text
from sqlalchemy.dialects import postgresql
import db_layer as db
from db_repository import dbSQL
import logging

class dbPGSQL(dbSQL):

    @classmethod
    def disable_constraints(cls):
        disable_constraints = Text("SET CONSTRAINTS ALL DEFERRED")
        db.get_engine().execute(disable_constraints)

    @classmethod
    def enable_constraints(cls):
        enable_constraints = Text("SET CONSTRAINTS ALL IMMEDIATE")
        db.get_engine().execute(enable_constraints)

    @classmethod
    def get_select_all_column_statement(cls, table_name):
        cols = dbSQL.get_table_column_names( table_name)
        sql = 'SELECT "'
        sql += '", "'.join( cols)
        sql += '"'
        sql += f" FROM {table_name}"
        return sql

    @staticmethod
    def fetch_table_data( tablename: str, rowlimit: int = None)-> DataFrame:
        sql = f"SELECT * FROM {tablename}"
        sql += f" LIMIT {rowlimit} " if rowlimit is not None else ""
        sql += ';'
        df = db.db_fetchall(sql)
        return df

    # @staticmethod
    # def write_to_table( df:DataFrame, tablename:str):
    #     df.to_sql(tablename, db.get_connection(), if_exists='append',index=False) 

    @staticmethod
    def copy_csv_file_to_table( filename: str, tablename: str):
        retval = None
        try:
            sql = f"COPY {tablename} from '{filename}' delimiter E'\t' CSV HEADER;"
            retval = db.pg_execute( sql)
        except Exception as ex:
            logging.error( repr(ex))
        
        return retval

    @classmethod
    def create_table_script( cls, metadata, table_name, callback):
        return dbSQL.create_table_script_with_dialect( postgresql.dialect(), metadata, table_name, callback)

    @classmethod
    def create_index_script( cls, metadata, table_name, callback):
        return dbSQL.create_index_script_with_dialect( postgresql.dialect(), metadata, table_name, callback)

