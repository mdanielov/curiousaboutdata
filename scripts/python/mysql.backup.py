import configparser
import pymysql.cursors
import os
import subprocess
import re


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),'settings.ini'))
host = config.get('mysql', 'host')
mysql_port = config.get('mysql', 'port')
user = config.get('mysql', 'user')
password = config.get('mysql', 'password')
dbname = config.get('mysql', 'db')
root_dir = config.get('mysql', 'backup_dir')
mysqldump_dir = config.get('mysql', 'mysqldump_dir')
get_routines = int(config.get('mysql', 'get_routines'))
get_schema = int(config.get('mysql', 'get_schema'))
get_data = int(config.get('mysql', 'get_data'))
mysqldump='"' +mysqldump_dir + "mysqldump.exe"+'"'
limit_data = 1

# create common strings
sqldump_base = mysqldump+" -h {} -P {} -u {} --password={} --compact --default-character-set=utf8 --no-create-info --set-gtid-purged=OFF --hex-blob --column-statistics=0 --no-create-db --skip-opt ".format(host, mysql_port, user, password)
    
connection = pymysql.connect(host=host, port=int(mysql_port), user=user, password=password, database=dbname, charset='utf8mb4')

qry_db_list = "show databases;"
except_dbs = ["information_schema", "mysql", "performance_schema", "sys"]


def main():
    db_list = []
    db_list = run_qury(qry_db_list)
    for d in db_list:
        db_name = d[0]
        print(db_name)
        if not os.path.exists(root_dir):
            os.mkdir(root_dir)
        if db_name not in except_dbs and db_name == dbname:
                work_on_db(db_name)


def work_on_db(dbname):
    print("working on {} database".format(dbname))
    print("****************************")
    print("")
    db_dir = os.path.join(root_dir, dbname)
    if not os.path.exists(db_dir):
        os.mkdir(db_dir)
    if get_data == 1 or get_schema == 1:
        work_on_tables(dbname, db_dir)
        work_on_triggers(dbname, db_dir)
    if get_routines == 1:
        work_on_routines(dbname, db_dir)


def work_on_routines(db, db_dir):
    db_dir = os.path.join(db_dir, "schema")
    dir_check(db_dir)
    # run mysqldump to get all routines
    print("working on routines")
    print("****************************")
    dump_string = sqldump_base + " --routines  --no-data {}".format(db)
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
        write_trigger(db,tr[0],db_dir)

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

def write_trigger(db, tr, base_dir):
    file_path = os.path.join(base_dir, "schema", "triggers", tr + ".sql")
    dir_check(os.path.join(base_dir, "schema", "triggers"))
    if os.path.exists(file_path):
        os.remove(file_path)
    tr_qry = "select CONCAT('DELIMITER //\n" \
              "CREATE TRIGGER "+ tr + " \n'" \
              ",ACTION_TIMING,' ',EVENT_MANIPULATION,\n" \
             "' ON  ',EVENT_OBJECT_TABLE,' FOR EACH ',ACTION_ORIENTATION,\n" \
             "'\nBEGIN\n'" \
             ",ACTION_STATEMENT," \
            "'\nEND $$" \
            "\nDELIMITER //') from information_schema.triggers where trigger_schema = '{}' AND trigger_name = '{}';".format(db, tr)
    # print(tr_qry)
    tr_txt = run_qury(tr_qry)[0][0]
    write_file(file_path, tr_txt)


def write_table_schema(db, tbl, base_dir):
    file_path = os.path.join(base_dir, "schema", "tables", tbl + ".sql")
    dir_check(os.path.join(base_dir, "schema", "tables"))
    if os.path.exists(file_path):
        os.remove(file_path)
    # dump_string = sqldump_base + "--triggers --no-data {} {}".format(db, tbl)
    # res = subprocess.Popen(dump_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # out, err = res.communicate()
    # schema_txt = out.decode('utf-8')
    qry_schema = "show create table {}.{};".format(db, tbl)
    schema_txt = run_qury(qry_schema)[0][1]
    write_file(file_path, schema_txt)


def write_table_data(db, tbl, base_dir):
    file_path = os.path.join(base_dir, "data", tbl + ".sql")
    if os.path.exists(file_path):
        os.remove(file_path)
    dump_string = sqldump_base + " {} {}".format(db, tbl)
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


def run_qury(qry_text):
    with connection.cursor() as cursor:
        cursor.execute(qry_text)
        return cursor.fetchall()

def clean_str(input_str):
    input_strs = input_str.splitlines()
    str_out = ""
    for i,s in enumerate(input_strs):
        if "[Warning] Using a password " in s:
            input_strs.remove(s)
    return str_out.join(input_strs)


def write_file(file_path, file_text):
    f = open(file_path, "w", encoding="utf-8")
    f.write(file_text)
    f.close()


def dir_check(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)


if __name__ == "__main__":
    main()
