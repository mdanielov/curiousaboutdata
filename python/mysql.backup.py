import configparser
import pymysql.cursors
import os
import subprocess
import re


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),'settings.ini'))
host = config.get('backup', 'host')
mysql_port = config.get('backup', 'port')
user = config.get('backup', 'user')
password = config.get('backup', 'password')
root_dir = config.get('backup', 'backup_dir')
get_routines = int(config.get('backup', 'get_routines'))
get_schema = int(config.get('backup', 'get_schema'))
get_data = int(config.get('backup', 'get_data'))
AllDBs = int(config.get('backup', 'AllDBs'))
limit_data = int(config.get('backup', 'limit_data'))
db_list = config.get("backup", "db_list").split(",")
mysql_dir = config.get('mysql', 'mysql_dir')
mysqldump='"' +mysql_dir + "\mysqldump.exe"+'"'


# create common strings
# currently just used for data dump
sqldump_base = mysqldump+" -h {} -P {} -u {} --password={} --skip-triggers --skip-add-drop-table --skip-add-locks --skip-set-charset --default-character-set=utf8 --no-create-info --set-gtid-purged=OFF --hex-blob --column-statistics=0 --no-create-db --skip-opt ".format(host, mysql_port, user, password)
    
connection = pymysql.connect(host=host, port=int(mysql_port), user=user, password=password, charset='utf8mb4')

except_dbs = ["information_schema", "mysql", "performance_schema", "sys"]

def main():
    if AllDBs == 1:
         #for AllDbs backup path should not exist at all
        if os.path.exists(root_dir):
            print("Backup directory already exists. Please remove before running script.")
            exit(1)
        db_all_list = []
        db_all_list = run_qury("show databases;")
        for d in db_all_list:
            db_name = d['Database']
            if not os.path.exists(root_dir):
                os.mkdir(root_dir)
            if db_name not in except_dbs:
                work_on_db(db_name)
    else:
        if not os.path.exists(root_dir):
            os.mkdir(root_dir)
        for db_name in db_list:
            #for specific databases - check each backup/db_name individually if it exists
            if os.path.exists(os.path.join(root_dir, db_name)):
                print("Backup directory for {} already exists. Please remove before running script.", db_name)
            else:
                work_on_db(db_name)

def work_on_db(dbname):
    print("working on {} database".format(dbname))
    print("****************************")
    print("") 
    connection.select_db(dbname)

    db_dir = os.path.join(root_dir, dbname)
    if not os.path.exists(db_dir):
        os.mkdir(db_dir)
    if get_data == 1 or get_schema == 1:
        work_on_tables(dbname, db_dir)
        work_on_triggers(dbname, db_dir)
    if get_routines == 1:
        work_on_routines(dbname, db_dir)


def work_on_routines(db, db_dir):
    os.path.join(db_dir, "schema")
    dir_check(db_dir)
    # get all procedures
    print("working on procedures")
    print("****************************")
     
    routine_list = []
    qry_routine_list = "SHOW PROCEDURE STATUS WHERE Db = '{}';".format(db)
    routine_list = run_qury(qry_routine_list)
  
    for routine in routine_list:
        print("working on schema for {} procedure".format(routine['Name']))
        write_procedure_schema(db, routine['Name'], db_dir)

    print("****************************")
    print("finished working on procedures")

    # get all functinos
    print("working on functions")
    print("****************************")
     
    function_list = []
    qry_function_list = "SHOW FUNCTION STATUS WHERE Db = '{}';".format(db)
    function_list = run_qury(qry_function_list)
  
    for function in function_list:
        print("working on schema for {} function".format(function['Name']))
        write_function_schema(db, function['Name'], db_dir)

    print("****************************")
    print("finished working on procedures")

def work_on_triggers(db, db_dir):
    tr_list = []
    print("working on triggers")
    print("****************************")
    qry_tr_list = "select trigger_name from information_schema.triggers where trigger_schema = '{}';".format(db)
    tr_list = run_qury(qry_tr_list)
    for tr in tr_list:
        print("working on trigger {}".format(tr['TRIGGER_NAME']))
        write_trigger(db,tr['TRIGGER_NAME'],db_dir)

def work_on_tables(db, db_dir):
    tbl_list = []
    qry_tbl_list = "SELECT distinct TABLE_NAME,TABLE_TYPE FROM information_schema.tables where table_schema = '{}';".format(db)
    tbl_list = run_qury(qry_tbl_list)
    if get_schema == 1:
        print("working on schema")
        print("****************************")
        dir_check(os.path.join(db_dir, "schema"))
        for tbl in tbl_list:
            if tbl['TABLE_TYPE'] == "BASE TABLE":
               print("working on schema for {} table".format(tbl['TABLE_NAME']))
               write_table_schema(db, tbl['TABLE_NAME'], db_dir)
            elif tbl['TABLE_TYPE'] == "VIEW":
               print("working on schema for {} view".format(tbl['TABLE_NAME']))
               write_view_schema(db, tbl['TABLE_NAME'], db_dir)
        print("****************************")
        print("finished working on schema")
        print("")
    if get_data == 1:
        dir_check(os.path.join(db_dir, "data"))
        print("working on data")
        print("****************************")
        for tbl in tbl_list:
            if tbl['TABLE_TYPE'] == "BASE TABLE":
                print("working on data for {} table".format(tbl['TABLE_NAME']))
                write_table_data(db, tbl['TABLE_NAME'], db_dir)
        print("****************************")
        print("finished working on data")
    print("")

def write_trigger(db, tr, base_dir):
    file_path = os.path.join(base_dir, "schema", "triggers", tr + ".sql")
    dir_check(os.path.join(base_dir, "schema", "triggers"))
    if os.path.exists(file_path):
        os.remove(file_path)
    qry_schema = "show create trigger `{}`.`{}`;".format(db, tr)
  
    schema_txt = run_qury(qry_schema)[0]['SQL Original Statement']
  # remove definer for the create statement
    txtA = schema_txt.partition("TRIGGER")
    txt_modified = "CREATE TRIGGER " + txtA[2]

    write_file(file_path, txt_modified)


def write_table_schema(db, tbl, base_dir):
    pttrn_incr = re.compile(r"\sAUTO_INCREMENT=\d+\s")
    file_path = os.path.join(base_dir, "schema", "tables", tbl + ".sql")
    dir_check(os.path.join(base_dir, "schema", "tables"))
    if os.path.exists(file_path):
        os.remove(file_path)
    qry_schema = "show create table {}.{};".format(db, tbl)
    # schema_txt = run_qury(qry_schema)[0][1]
    schema_txt = run_qury(qry_schema)[0]["Create Table"]
    schema_txt = re.sub(pttrn_incr," ",schema_txt)
    schema_txt = re.sub(r'utf8mb3', 'utf8', schema_txt)
    write_file(file_path, schema_txt)

def write_view_schema(db, view, base_dir):
    file_path = os.path.join(base_dir, "schema", "views", view + ".sql")
    dir_check(os.path.join(base_dir, "schema", "views"))
    if os.path.exists(file_path):
        os.remove(file_path)
    qry_schema = "show create view `{}`.`{}`;".format(db, view)

    schema_txt = run_qury(qry_schema)[0]['Create View']
  # remove definer for the create statement
    txtA = schema_txt.split("DEFINER")
    txt_modified = txtA[0] + txtA[2]

    write_file(file_path, txt_modified)

def write_procedure_schema(db, procedure, base_dir):
    file_path = os.path.join(base_dir, "schema", "procedures", procedure + ".proc.sql")
    dir_check(os.path.join(base_dir, "schema", "procedures"))
    if os.path.exists(file_path):
        os.remove(file_path)
    qry_schema = "show create procedure `{}`.`{}`;".format(db, procedure)

    schema_txt = run_qury(qry_schema)[0]['Create Procedure']

  # remove definer for the create statement
    txtA = schema_txt.partition("PROCEDURE")
    txt_modified = "CREATE PROCEDURE " + txtA[2]

    write_file(file_path, txt_modified)

def write_function_schema(db, function, base_dir):
    file_path = os.path.join(base_dir, "schema", "functions", function + ".func.sql")
    dir_check(os.path.join(base_dir, "schema", "functions"))
    if os.path.exists(file_path):
        os.remove(file_path)
    qry_schema = "show create function `{}`.`{}`;".format(db, function)
    print(qry_schema)

    schema_txt = run_qury(qry_schema)[0]['Create Function']

  # remove definer for the create statement
    txtA = schema_txt.partition("FUNCTION")
    txt_modified = "CREATE FUNCTION "+ txtA[2]

    write_file(file_path, txt_modified)

def write_table_data(db, tbl, base_dir):
    file_path = os.path.join(base_dir, "data", tbl + ".sql")
    if os.path.exists(file_path):
        os.remove(file_path)
    dump_string = sqldump_base + " {} {}".format(db, tbl)
    if limit_data == 1:
        dump_string = dump_string +  " --where="""""1 limit 10"""" "
 
    res = subprocess.Popen(dump_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = res.communicate()

    # save it to a string and to a file
    # print(out)
    table_data = clean_str(out.decode("unicode-escape"))
    write_file(file_path, table_data)


def run_qury(qry_text):
    with connection.cursor() as cursor:
        cursor.execute(qry_text)
        columns = cursor.description 
        result = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
        return result

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
