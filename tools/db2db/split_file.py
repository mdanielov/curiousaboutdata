import logging
from sys import stdout, argv
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd

dotenv_path = Path.joinpath(Path(__file__).parent, '.env')
load_dotenv(dotenv_path)


def set_logging_file( log_filename):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filename=log_filename, encoding='utf-8')
    logging.getLogger().addHandler(logging.StreamHandler(stdout))
    return


def split_file(file_to_split, lines_per_chunk):
    baseName = file_to_split.stem
    with open(file_to_split, 'r') as fin:
        chunk_counter = 1
        line_counter = 0
        fout  = None
        for line in fin:
            if line_counter % lines_per_chunk == 0:
                if fout:
                    fout.close()
                output_chunk_file = Path.joinpath( file_to_split.parent, f"{file_to_split.stem}_{chunk_counter:03d}{file_to_split.suffix}")
                fout = open( output_chunk_file, "w");

                logging.info( f"Writing: {output_chunk_file.name}")
                chunk_counter += 1
            fout.write(line)
            line_counter += 1

        if fout:
            fout.close()

def chunk_file( file_path, chunk_size):
    # Create a reader object to read the file in chunks
    reader = pd.read_csv(file_path, sep='\t', chunksize=chunk_size, encoding='latin1')
    chunk_counter = 1
    # Process each chunk
    for df_chunk in reader:
        output_chunk_file = Path.joinpath( file_path.parent, f"{file_path.stem}_{chunk_counter:03d}{file_path.suffix}")
        df_chunk.to_csv( output_chunk_file, sep='\t', index=False)
        logging.info( f"Writing: {output_chunk_file.name}")
        chunk_counter += 1
    logging.info( f"Done writing {chunk_counter} files")

# Usage example
def main():
    set_logging_file("./split_file.log")
    if len(argv) > 1:
        input_file = argv[1]
    else:
        logging.info( "split_file <file_name> <chunk_size>|1000")    
        exit()

    lines_per_chunk = int(argv[2]) if len(argv) > 2 else 1000
    file_to_split = Path(input_file)
    if file_to_split.is_file():
        logging.info( f"Begin {__file__}")    
        chunk_file(file_to_split, lines_per_chunk)
        # split_file(file_to_split, lines_per_chunk)
        logging.info( "Done")
    else:
        logging.error( f"{input_file} does not exist")

if __name__ == "__main__":
    main()