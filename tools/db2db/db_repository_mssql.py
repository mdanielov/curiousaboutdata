from pandas import DataFrame
from sqlalchemy.dialects import mssql
import subprocess
from db_repository import dbSQL
import db_layer as db

class dbMSSQL(dbSQL):
    @classmethod
    def get_select_all_column_statement(cls, table_name:str, row_limit: int=0) -> str:
        cols = dbSQL.get_table_column_names( table_name)
        sql = "SELECT "
        if row_limit > 0: sql += f"TOP ({row_limit}) "
        sql += "["
        sql += '], ['.join( cols)
        sql += f"] FROM {table_name}"
        return sql


    @staticmethod
    def fetch_table_data( tablename: str, rowlimit: str = None)-> DataFrame:
        sql = "SELECT "
        sql += f" TOP {rowlimit} " if rowlimit is not None else ""
        sql += f"* FROM {tablename}"
        df = db.db_fetchall(sql)
        return df

    def fetch_table_data_in_chunks( tablename: str, offset:str = "0", rowlimit: str = "1000")-> DataFrame:
        sql = f"""
SELECT *
FROM {tablename}
ORDER BY 1
OFFSET {offset} ROWS FETCH NEXT {rowlimit} ROWS ONLY;
"""
        df = db.db_fetchall(sql)
        return df
    
    @staticmethod
    def get_bcp_cmd( direction: str, tablename: str, filename: str, rowlimit: str = None) -> list:
        dbconfig = dbSQL.get_dbconfig()
        # Define the BCP command as a list of arguments
        bcp_command = ["bcp", tablename, direction, filename, "-c", "-t", "-S", dbconfig.get('host'), "-d", dbconfig.get('dbname') ]
        if rowlimit is not None:
            bcp_command += [ "-L", rowlimit]
        if 'user' in dbconfig:
            bcp_command += ["-U", dbconfig.get('user')]
            if 'password' in dbconfig:
                bcp_command += ["-P", dbconfig.get('password')]
        else:
            bcp_command.append( "-T") # trusted connection
        return bcp_command

    @staticmethod
    def get_bcp_out_cmd(tablename: str, targetdir: str, rowlimit: str = None)->str:
        lastrow = f" -L {rowlimit}" if rowlimit is not None else ""
        stmnt = f"""
SELECT CONCAT( 'bcp [', TABLE_SCHEMA, '].[', TABLE_NAME, '] out {targetdir}\', TABLE_NAME, '.tsv -S ', @@SERVERNAME, ' -d ', DB_NAME(), ' -T -c -t {lastrow}')
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME = '{tablename}'
ORDER BY TABLE_NAME
;
"""
        return stmnt


    @staticmethod
    def bcp_in(tablename: str, filename: str, rowlimit: str = None):
        bcp_command = dbMSSQL.get_bcp_cmd( "in", tablename, filename, rowlimit)
        # Execute the BCP command
        retval = subprocess.run(bcp_command)
        num_rows = 'All' if rowlimit is None else rowlimit

        return num_rows if retval.returncode == 0 else 'Error: ' + retval.returncode
    @staticmethod
    def bcp_out(tablename: str, filename: str, rowlimit: str = None):
        bcp_command = dbMSSQL.get_bcp_cmd( "out", tablename, filename, rowlimit)
        # Execute the BCP command
        retval = subprocess.run(bcp_command)
        num_rows = 'All' if rowlimit is None else rowlimit

        return num_rows if retval.returncode == 0 else 'Error: ' + retval.returncode

    @classmethod
    def create_table_script( cls, metadata, table_name, callback):
        return dbSQL.create_table_script_with_dialect( mssql.dialect(), metadata, table_name, callback)

    @classmethod
    def create_index_script( cls, metadata, table_name, callback):
        return dbSQL.create_index_script_with_dialect( mssql.dialect(), metadata, table_name, callback)
