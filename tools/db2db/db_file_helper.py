from pathlib import Path
import pandas as pd
import re
CHUNKSIZE = 50000

def get_file_name_from_table( dir_name:Path, table_name: str, extension: str = "csv", filepart: int = None) -> Path:
    filename = f"{table_name}.{extension}" if filepart is None else f"{table_name}_{filepart:03d}.{extension}"
    return Path.joinpath( Path(dir_name), filename)

def get_table_name_from_file( filepath: Path) -> str:
    if (m := re.match( r"(\w+)\.(.+)_\d{3}", filepath.stem)) is not None:
        table_name = m[2]
    elif (m := re.match( r"(.+)_\d{3}", filepath.stem)) is not None:
        table_name = m[1]
    else:
        table_name = filepath.stem
    return table_name.lower()

def df_to_file(df: pd.DataFrame, fullfilename: str) -> Path:
    chunksize = 50000
    for ii in range(0, len(df), CHUNKSIZE):
        df_chunk = df[ii:ii+CHUNKSIZE]
        df_chunk.to_csv(fullfilename, mode='a', index=False, float_format='%.2f')
     
    return Path(fullfilename)

def import_in_chunks( filename: str, table_name: str, callback, row_limit: int = 0, chunk_size: int = 1000)-> int:
    rows_read = 1
    total_rows = 0
    if row_limit > 0 and row_limit < chunk_size:
        chunk_size = row_limit
    dfHead = pd.read_csv(filename, sep='\t', header=0, nrows=0)
    bFlag = True
    while bFlag:
        # actual_chunk_size = chunk_size if row_limit == 0 else total_rows % row
        df = pd.read_csv(filename, sep='\t', header=0, skiprows=total_rows)#nrows=chunk_size, 
        df.columns = dfHead.columns
        rows_read = len(df)
        total_rows += rows_read
        callback( df, table_name)
        bFlag = False if rows_read < chunk_size or total_rows > row_limit else True
        # pd.read_csv(fullfilename, sep="\t", low_memory=False)
    return total_rows

def file_to_df_chunk(fullfilename) -> pd.DataFrame:
    df = pd.read_csv(fullfilename, chunksize=CHUNKSIZE)
    return df

def get_file_names(dir_name, pattern:str = ""):
    names = Path(dir_name).glob(f"{pattern}*.[t|c]sv")
    return names

def write_file( dir_name: str, file_name: str, contents: str):
    file = Path(dir_name).joinpath( file_name)
    with open( file, "w") as fout:
        fout.write( contents)

def read_file( file: Path) -> str:
    contents = None
    with open( file, "r") as fin:
        contents = fin.read()
    return contents

def walk_directory( dir_name:str, pattern:str, callback):
    directory_path = Path(dir_name)
    # Use the `rglob()` method to recursively iterate over all files and directories
    for file_path in directory_path.rglob(f"{pattern}*"):
        if file_path.is_file():
            callback( file_path)
