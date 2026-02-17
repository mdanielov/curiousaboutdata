import os
from pathlib import Path
from db_repository import dbSQL
import db_repository_factory as drf
from db_layer import get_connection_dict
import db_file_helper as dfh
import pandas as pd
import logging
from functools import wraps
import time
from db2db_progress import DB2DBProgress
from configparser import ConfigParser

config = ConfigParser()
config.read('./settings.ini')
get_settings = config["settings"]

myProgress = DB2DBProgress(get_settings["PROGRESS_FILE"]) #os.getenv("PROGRESS_FILE", "progress.json")

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        msg = f"Function {func.__name__}" # {args}"
        msg += kwargs if len(kwargs) > 0 else ''
        msg += f" Took {total_time:.4f} seconds"
        logging.info(msg)
        return result
    return timeit_wrapper

def run(action):
    action_func = {
        "export_data" : export_data
        , "import_data": import_data
        , "export_schema": export_schema
        , 'import_schema': import_schema
    }.get(action)
    logging.info( action)
    if action_func is not None:
        action_func()

def log_db_information():
    connection_dict = get_connection_dict()
    logging.info( f"DB Dialect {connection_dict.get('dbtype')} -> DB: {connection_dict.get('dbname')}")

def export_setup():
    # config['settings']['CONNECTION_STRING'] = get_settings["SOURCE_CONNECTION_STRING"]#os.getenv("SOURCE_CONNECTION_STRING")
    # with open('./settings.ini', 'w') as configfile:
    #     config.write(configfile)
    return drf.get_repository()

def import_setup():
    # config['settings']['CONNECTION_STRING'] = get_settings["TARGET_CONNECTION_STRING"]#os.getenv("TARGET_CONNECTION_STRING")
    # with open('./settings.ini', 'w') as configfile:
    #     config.write(configfile)
    return drf.get_repository()

def export_data(pattern:str = None):
    dr = export_setup()
    pattern =get_settings["TABLE_NAME"] #os.getenv('TABLE_NAME')
    retvals = [ "No tables"]
    tables =  dr.get_table_names(pattern)
    if tables is not None:
        for table_name in tables:
            if myProgress.has_seen_export_table( table_name):
                logging.info( f"Table {table_name} has been processed.")
            else:
                logging.info( f"Table {table_name} exporting...")
                export_table( dr, table_name)
    myProgress.store()
    logging.info( "\n".join(retvals))
            
@timeit
def export_table( dr: dbSQL, table_name: str):
    dr.fetch_and_write_in_chunks( table_name, export_table_chunks_callback, int(get_settings["ROW_LIMIT"]), int(get_settings["CHUNKSIZE"]))#int(os.getenv("ROW_LIMIT", "0")), int(os.getenv("CHUNKSIZE", "1000")))

def export_table_chunks_callback( table_name: str, df_chunk: pd.DataFrame, file_counter: int, chunk_size: int):
    target_dir = Path(get_settings["TARGETDIR"])
    filepath = dfh.get_file_name_from_table(target_dir, table_name, "tsv", file_counter)
    rows = df_chunk.shape[0]
    df_chunk.to_csv(filepath, sep='\t', index=False, chunksize=chunk_size)
    myProgress.mark_export( table_name, filepath.as_posix())
    logging.info( f"{table_name} -> {filepath.name} {rows} rows")
     
def import_data():
    dr = import_setup()
    print("progress file {}".format(myProgress.file_name))
    pattern = get_settings["FILE_NAME"]#os.getenv('FILE_NAME', '')
    retvals = [ "No files"]
    source_dir = get_settings["SOURCEDIR"]#os.getenv("SOURCEDIR"))
    print("source directory {}".format(source_dir))
    if not Path(source_dir).is_dir:
        logging.error( f"{source_dir} is not a directory")
        return retvals
    logging.info( f"Reading {source_dir}")
    files = dfh.get_file_names(source_dir,pattern)
    row_limit = get_row_limit()   
    total_rows_processed = 0
    if files is not None:
        for file in files:
            table_name = dfh.get_table_name_from_file(file)
            if not myProgress.has_seen_import_table( table_name):
                total_rows_processed = 0
            if should_process_import_file( table_name, os.path.basename(file), row_limit, total_rows_processed):
                rows_processed = import_file_to_table(dr, file, table_name, row_limit)
                total_rows_processed += rows_processed if rows_processed > 0 else 0
                logging.info( f"{file.name}->{table_name}: total rows {total_rows_processed}")
    logging.info( "Done Import")
    myProgress.store()
    return retvals

@timeit
def import_file_to_table(dr: dbSQL, file:Path, table_name: str, row_limit: int = 0):
    try:
        # row_count_before = dr.get_row_count(table_name)
        rows_read = dfh.import_in_chunks( file.as_posix(), table_name, dbSQL.insert_into_table, row_limit, 1000)
        msg = f"{file.name} => {table_name}: # of rows: {rows_read}"
        myProgress.mark_import( table_name, file.name)
        logging.info( msg)
        return rows_read
    except Exception as ex:
        logging.error(repr(ex))
        return -1
    
def get_row_limit():
    try:
        row_limit = int(get_settings["ROW_LIMIT"])#os.getenv("ROW_LIMIT", 0))
    except:
        row_limit = 0
    return row_limit

def should_process_export( table_name, file_name:str, row_limit:int, total_rows_processed:int) -> bool:
    if myProgress.has_seen_file('export', table_name, file_name):
        logging.info( f"File {file_name} has been processed.")
        return False
    if row_limit == 0 or total_rows_processed <= row_limit:
        return True
    return False

def should_process_import_file( table_name, file_name:str, row_limit:int, total_rows_processed:int) -> bool:
    if myProgress.has_seen_file('import', table_name, file_name):
        logging.info( f"File {file_name} has been processed.")
        return False
    if row_limit == 0 and myProgress.has_seen_import_file(table_name,file_name):
        logging.info( f"Table {table_name} has been processed.")
        return False
    if row_limit == 0 or total_rows_processed <= row_limit:
        return True
    return False

def export_schema():
    dr = export_setup()
    log_db_information()
    pattern = get_settings["TABLE_NAME"]#os.getenv('TABLE_NAME')
    retvals = [ "No tables"]
    metadata = dr.get_meta_data()
    tables =  dr.get_table_names(pattern)
    if tables is not None:
        for table_name in tables:
            dr.create_table_script( metadata, table_name, write_table_schema_script)
            dr.create_index_script( metadata, table_name, write_index_schema_script)

def write_table_schema_script( table_name, sql):
    try:
        target_dir = Path(get_settings["TARGETDIR"])#os.getenv("TARGETDIR"))
        dfh.write_file( target_dir, f"{table_name}.sql", sql)
        logging.info(f"{table_name} ->  {target_dir}/{table_name}.sql")
    except Exception as ex:
        logging.error( repr(ex))

def write_index_schema_script( index_name, sql):
    try:
        target_dir = Path(get_settings["TARGETDIR"]).joinpath("index")#os.getenv("TARGETDIR")).joinpath("index")
        if not target_dir.exists():
            target_dir.mkdir()
        dfh.write_file( target_dir, f"{index_name}.sql", sql)
        logging.info(f"{index_name} ->  {target_dir}/{index_name}.sql")
    except Exception as ex:
        logging.error( repr(ex))

def import_schema():
    dr = import_setup()
    pattern = get_settings["FILE_NAME"]#os.getenv('FILE_NAME')
    retvals = ["No files"]
    source_dir = get_settings["SCHEMA_SOURCEDIR"]#os.getenv("SCHEMA_SOURCEDIR")
    dfh.walk_directory( source_dir, pattern, execute_script)

def execute_script( file: Path) -> bool:
    retval = False
    dr = drf.get_repository()
    dr.get_connection()
    try:
        logging.info( f"{file.name} - ready to execute")
        dr.read_and_run(file.as_posix())
        logging.info(f"{file.name} - executed")
        retval = True
    except Exception as ex:
        logging.error(repr(ex))
    return retval
