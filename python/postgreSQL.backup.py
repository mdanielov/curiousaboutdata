import configparser
import os
import subprocess
import re
import psycopg2
from subprocess import PIPE,Popen
import pgpasslib


config = configparser.ConfigParser()
config.read('C:\Git\curiosaboutdata\scripts\python\settings.ini')
host = config.get('postgresql', 'host')
database = config.get('postgresql', 'database')
user = config.get('postgresql', 'user')
password = config.get('postgresql', 'password')
root_dir = config.get('postgresql', 'backup_dir')
mysqldump_dir = config.get('postgresql', 'mysqldump_dir')
get_routines = int(config.get('postgresql', 'get_routines'))
get_schema = int(config.get('postgresql', 'get_schema'))
get_data = int(config.get('postgresql', 'get_data'))
pg_dump='"' +mysqldump_dir + "pg_dump.exe"+'"'
limit_data=1


conn = psycopg2.connect(host=host,database=database,user=user,password=password)
cur = conn.cursor()
os.environ['PGPASSWORD'] = password 

# sqldump_base = mysqldump+" -h {} -P {} -u {} --password={} --compact --default-character-set=utf8 --no-create-info --set-gtid-purged=OFF --hex-blob --column-statistics=0 --no-create-db --skip-opt ".format(host, mysql_port, user, password)
pg_dump_base = pg_dump+ " -U {} ".format(user)

qry_db_list = "SELECT datname FROM pg_database;"
except_dbs = ["postgres", "template1", "template0", "sys"]


def main():
    db_list = []
    db_list = run_qury(qry_db_list)
    for d in db_list:
        db_name = d[0]
        print(db_name)
        if not os.path.exists(root_dir):
            os.mkdir(root_dir)
        if db_name not in except_dbs and db_name == database:
                work_on_db(db_name)

def run_qury(qry_text):
    cur.execute(qry_text)
    return cur.fetchall()

def work_on_db(dbname):
    print("working on {} database".format(dbname))
    print("****************************")
    print("")
    db_dir = os.path.join(root_dir, dbname)
    if not os.path.exists(db_dir):
        os.mkdir(db_dir)
    if get_data == 1 or get_schema == 1:
        work_on_tables(dbname, db_dir)
        # work_on_triggers(dbname, db_dir)
    # if get_routines == 1:
        work_on_routines(dbname, db_dir)

def work_on_tables(db, db_dir):
    tbl_list = []
    qry_tbl_list = "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';"
    tbl_list = run_qury(qry_tbl_list)
    if get_schema == 1:
        print("working on schema")
        print("****************************")
        dir_check(os.path.join(db_dir, "schema"))
        for tbl in tbl_list:
            print("working on schema for {} table".format(tbl[0]))
            write_table_schema(db, tbl[0], db_dir)
        print("****************************")
        print("finished working on schema")
        print("")
    # if get_data == 1:
    #     dir_check(os.path.join(db_dir, "data"))
    #     print("working on data")
    #     print("****************************")
    #     for tbl in tbl_list:
    #         print("working on data for {} table".format(tbl[0]))
    #         write_table_data(db, tbl[0], db_dir)
    #     print("****************************")
    #     print("finished working on data")
    # print("")

def work_on_triggers(db, db_dir):
    tr_list = []
    print("working on triggers")
    print("****************************")
    qry_tr_list = "select trigger_name from information_schema.triggers where trigger_schema = '{}';".format(db)
    tr_list = run_qury(qry_tr_list)
    for tr in tr_list:
        print("working on trigger {}".format(tr[0]))
        write_trigger(db,tr[0],db_dir)

def dir_check(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

def write_file(file_path, file_text):
    f = open(file_path, "w", encoding="utf-8")
    f.write(file_text)
    f.close()

def write_table_data(db, tbl, base_dir):
    file_path = os.path.join(base_dir, "data", tbl + ".sql")
    if os.path.exists(file_path):
        os.remove(file_path)
    dump_string = pg_dump_base + " {} {}".format(db, tbl)
    if limit_data == 1:
        dump_string = dump_string +  " --where="""""1 limit 10"""" "
        #print(dump_string)
    #dump_string = sqldump_base + " {} {} 2>/dev/null".format(db, tbl)    
    res = subprocess.Popen(dump_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = res.communicate()

    # save it to a string and to a file
    # print(out)
    table_data = clean_str(out.decode('unicode_escape'))
    write_file(file_path, table_data)

def clean_str(input_str):
    input_strs = input_str.splitlines()
    str_out = ""
    for i,s in enumerate(input_strs):
        if "[Warning] Using a password " in s:
            input_strs.remove(s)
    return str_out.join(input_strs)

def write_table_schema(db, tbl, base_dir):
    file_path = os.path.join(base_dir, "schema", "tables", tbl + ".sql")
    dir_check(os.path.join(base_dir, "schema", "tables"))
    if os.path.exists(file_path):
        os.remove(file_path)
    dump_string = pg_dump+" -U {}  -s -d {} -t public.{} > {}".format(user, database,tbl,file_path)
    res = subprocess.Popen(dump_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = res.communicate()
    res.wait()
    
def work_on_routines(db, db_dir):
    db_dir = os.path.join(db_dir, "schema")
    dir_check(db_dir)
    # run mysqldump to get all routines
    print("working on routines")
    print("****************************")
    dump_string = pg_dump_base + " -d {} -s > {}".format(database,db_dir+"\\"+db+".sql")
    res = subprocess.Popen(dump_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = res.communicate()

    # save it to a string
    all_routines = out.decode('utf-8')

    line_list = []
    # transform the output string in to a list of lines
    # and clean it along the way
    pttrn = re.compile(r"^\/\*\!.*$")
    for ln in all_routines.splitlines():
        if not re.match(pttrn, ln):
            ln = re.sub(r"DEFINER=.*?@.*?\s", "", ln)
            line_list.append(ln)

    # now that we have a clean routine list
    # break it into files
    my_chunk = ""
    for ln in line_list:
        if ln == "DELIMITER ;;":
            my_chunk = ln + '\n'
        else:
            if ln == "DELIMITER ;":
                my_chunk += ln
                process_chunk(my_chunk, db_dir)
            else:
                my_chunk += ln + '\n'

    print("****************************")
    print("finished working on routines")


def process_chunk(my_chunk, db_dir):
    pttrn = re.compile(r"CREATE (\w*?) `(.*?)`")

    r = re.search(pttrn, my_chunk)
    if r:
        write_routine(r.group(1).lower(), r.group(2).lower(), my_chunk, db_dir)
    else:
        print("pattern not found. ERROR!")


def write_routine(routine_type, routine_name, routine_text, base_dir):
    suffix = ""
    if routine_type == "function":
        print("working on function {}".format(routine_name))
        routine_type = "Functions"
        suffix = "func"
    else:
        if routine_type == "procedure":
            print("working on procedure {}".format(routine_name))
            routine_type = "Procedures"
            suffix = "proc"
        else:
            suffix = "unk"

    dest_dir = os.path.join(base_dir, routine_type)
    dir_check(dest_dir)
    file_path = os.path.join(dest_dir, routine_name + "." + suffix + ".sql")
    write_file(file_path, routine_text)


def work_on_triggers(db, db_dir):
    tr_list = []
    print("working on triggers")
    print("****************************")
    qry_tr_list = "select trigger_name from information_schema.triggers where trigger_schema = '{}';".format(db)
    tr_list = run_qury(qry_tr_list)
    for tr in tr_list:
        print("working on trigger {}".format(tr[0]))
        # write_trigger(db,tr[0],db_dir)

def work_on_tables(db, db_dir):
    tbl_list = []
    qry_tbl_list = "SELECT distinct table_name,table_type FROM information_schema.tables where table_schema = '{}';".format(db)
    tbl_list = run_qury(qry_tbl_list)
    if get_schema == 1:
        print("working on schema")
        print("****************************")
        dir_check(os.path.join(db_dir, "schema"))
        for tbl in tbl_list:
            print("working on schema for {} table".format(tbl[0]))
            write_table_schema(db, tbl[0], db_dir)
        print("****************************")
        print("finished working on schema")
        print("")
    if get_data == 1:
        dir_check(os.path.join(db_dir, "data"))
        print("working on data")
        print("****************************")
        for tbl in tbl_list:
            if tbl[1] == "BASE TABLE":
                print("working on data for {} table".format(tbl[0]))
                write_table_data(db, tbl[0], db_dir)
        print("****************************")
        print("finished working on data")
    print("")


main()