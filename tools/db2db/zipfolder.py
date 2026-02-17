import os
from pathlib import Path
import zipfile
import logging
from sys import stdout
from dotenv import load_dotenv
from configparser import ConfigParser

config = ConfigParser()
get_settings = config.read('./settings.ini')

dotenv_path = Path.joinpath(Path(__file__).parent, '.env')
load_dotenv(dotenv_path)


def set_logging_file( log_filename):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filename=log_filename, encoding='utf-8')
    logging.getLogger().addHandler(logging.StreamHandler(stdout))
    return


def zip_files_in_folder(folder_path, filepattern=None, chunk_size=1e9):
    pattern = "*.*" if filepattern is None else f"{filepattern}*.*"
    logging.info( f"File pattern: {folder_path} {pattern}")
    file_list = sorted(Path(folder_path).glob(pattern))


    current_chunk_size = 0
    chunk_index = 1
    current_chunk_files = []
    
    for file_name in file_list:
        file_path = Path.joinpath(Path(folder_path), file_name)
        file_size = file_path.stat().st_size
        logging.info( f"{file_path}: {file_size}")

        if current_chunk_size + file_size <= chunk_size:
            current_chunk_files.append(file_path)
            current_chunk_size += file_size
        else:
            # Create a new chunk and add files to it
            create_zip_chunk(current_chunk_files, chunk_index)
            
            # Reset variables for the next chunk
            current_chunk_files = [file_path]
            current_chunk_size = file_size
            chunk_index += 1

    # Create the last chunk
    create_zip_chunk(current_chunk_files, chunk_index)


def create_zip_chunk(file_list, chunk_index):
    zipchunk_file = get_settings["ZIPFILENAME"] #os.getenv( "ZIPFILENAME", "chunk")
    zip_name = Path.joinpath(Path(get_settings["ZIPTARGETDIR"]), f"{zipchunk_file}_{chunk_index}.zip")#os.getenv("ZIPTARGETDIR")), f"{zipchunk_file}_{chunk_index}.zip")
    
    with zipfile.ZipFile(zip_name, "w") as zip_file:
        for file_path in file_list:
            file_name = Path(file_path).name
            zip_file.write(file_path, file_name)


if __name__ == "__main__":
    set_logging_file(get_settings["ZIPLOGFILE"])#os.getenv("ZIPLOGFILE"))
    logging.info("Begin")
    zip_files_in_folder(get_settings["ZIPSOURCEDIR"],get_settings["ZIPFILEPATTERN"])#os.getenv('ZIPSOURCEDIR'), os.getenv(f"ZIPFILEPATTERN"))
    logging.info("End")

