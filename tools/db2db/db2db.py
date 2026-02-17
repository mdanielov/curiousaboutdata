# Read .env file

# Controls the direction of dataflow (in/out)

# Call the servicer to either export the data to file or import from file, using the configuration data structure

# create logging
import os
from sys import stdout
#from dotenv import load_dotenv
from pathlib import Path
import db_schema_service as dss
import logging
from functools import wraps
import time
from configparser import ConfigParser



def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        msg = f"Function {func.__name__}{args}"
        msg += kwargs if len(kwargs) > 0 else ''
        msg += f" Took {total_time:.4f} seconds"
        logging.info(msg)
        return result
    return timeit_wrapper



#dotenv_path = Path.joinpath(Path(__file__).parent, '.env')
#print(dotenv_path)
#load_dotenv(dotenv_path)
#read settings

config = ConfigParser()
config.read('./settings.ini')



def set_logging_file( log_filename):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filename=log_filename, encoding='utf-8')
    logging.getLogger().addHandler(logging.StreamHandler(stdout))
    return

@timeit
def main():
    #set_logging_file(os.getenv("LOG_FILE"))
    get_settings = config["settings"]
    log_file = get_settings["LOG_FILE"]
    set_logging_file(get_settings["LOG_FILE"])
    logging.info("Begin")
    #dss.run(os.getenv('ACTION'))
    action= get_settings["ACTION"]
    dss.run(get_settings["ACTION"])
    logging.info("End")

if __name__ == "__main__":
    main()