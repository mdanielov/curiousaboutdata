import configparser
import codecs
import pymysql.cursors
import subprocess
import os
from os import path

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),'settings.ini'))
host = config.get('mysql', 'host')
mysql_port = config.get('mysql', 'port')
user = config.get('mysql', 'user')
password = config.get('mysql', 'password')
mysql_path = config.get('mysql', 'mysql_dir')
AllDBs = config.get('restore', 'AllDBs')
db_list = config.get("restore", "db_list").split(",")
root_dir = config.get('restore', 'restore_dir')
put_routines = int(config.get('restore', 'put_routines'))
put_schema = int(config.get('restore', 'put_schema'))
put_data = int(config.get('restore', 'put_data'))
mysql='"' +mysql_path + "\mysql.exe"+'"'

connection = pymysql.connect(host=host, port=int(mysql_port), user=user, password=password)


def main():
    # check if root dir exists
    if os.path.isdir(root_dir):
        if AllDBs == 1:
            #all DBs get list of all directories in backup directory
            dirs = tree_walker(root_dir, 'dir')
        else:
            dirs = db_list

        for d in dirs:
            # process each database backup directory
            backup_dir = os.path.join(root_dir, "d")
            if os.path.isdir(backup_dir):
                # check if db exists on target, if exists error if not create
                qry_show_db = "SHOW DATABASES LIKE `{}`".format(d)
                cursor = connection.cursor()
                cursor.execute(qry_show_db)
                if cursor.rowcount:
                    print('Cannot restore database {} already exists. Drop database in order to restore.')
                else:
                    qry_create_db = "CREATE DATABASE IF NOT EXISTS `{}`;".format(d)
                    cursor.execute(qry_create_db)
                    connection.select_db(d)
                    cursor = connection.cursor()
                    qry_fk_checks = "SET FOREIGN_KEY_CHECKS = 0;"
                    cursor.execute(qry_fk_checks)
                 
                    if put_schema == 1:  
                        # process schema
                        if os.path.isdir(os.path.join(root_dir, "schema")):
                            walk_dirs(os.path.join(root_dir, "schema"), "schema")
                        else:
                            print("{} schema backup directory does not exist", backup_dir)
                    if put_data == 1:
                        # process data
                        if os.path.isdir(os.path.join(root_dir, "data")):
                            walk_dirs(os.path.join(root_dir, "data"), "data")
                        else:
                            print("{} data backup directory does not exist", backup_dir)
            else:
                print("{} backup directory does not exist", backup_dir)
    else:
        print("Root Backup directory does not exist.")

    conn1.close()


def restore_from_dir(dir_name, dir_type="schema"):
    if os.path.isdir(dir_name):
        files = tree_walker(dir_name, 'file')
        for f in files:
            if dir_type == "schema":
                 # for the schema we execute each sql file from cursor - so as to use the same current connection with
                 # foreign key checks set to 0
                file = open(os.path.join(dir_name, f))
                sql = file.read()
                print("working on {}".format(f))
            
                cursor = conn1.cursor()

                sql_request = get_sql_from_file(os.path.join(dir_name, f), False)
                if sql_request is not False:
                    try:
                        cursor.execute(sql_request)
                    except Exception as e:
                        print(e) 

                file.close()
            elif dir_type == "data":
                # for the data the sql file is created with mysqldump and includes set foreign key checks to 0
                # we therefore just run the .sql file using mysql command line
                restore_string = mysql+" -h {} -P {} -u {} --password={} {} < {}".format(host, mysql_port, user, password, db_name, os.path.join(dir_name, f))
                res = subprocess.Popen(restore_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                out, err = res.communicate()
                if err:
                    print(err)
    

def walk_dirs(dir_name, dir_type):
    if dir_type == "schema":
        print("Restoring Schema....")
        print("Restoring Tables....")
        tbl_dir = os.path.join(dir_name, "tables")
        restore_from_dir(tbl_dir)

        print("Restoring Triggers....")
        trig_dir = os.path.join(dir_name, "triggers")
        restore_from_dir(trig_dir)

        print("Restoring Views....")
        view_dir = os.path.join(dir_name, "views")
        restore_from_dir(view_dir)

        if put_routines == 1:
            print("Restoring Functions....")
            func_dir = os.path.join(dir_name, "functions")
            restore_from_dir(func_dir)

            print("Restoring Procedures....")
            proc_dir = os.path.join(dir_name, "procedures")
            restore_from_dir(proc_dir)

    if dir_type == "data":
        print("Restoring Data....")
        restore_from_dir(dir_name, dir_type)


def tree_walker(root_dir, return_type):
    for root, dirs, files in os.walk(root_dir):
        if return_type == 'dir':
            return dirs
        else:
            return files

def get_sql_from_file(filename, split):
    """
    Get the SQL instruction from a file - :return: a list of each SQL query whithout the trailing ";"
    """
    # File did not exists
    if path.isfile(filename) is False:
        print("File load error : {}".format(filename))
        return False
    else:
        if split:
            with open(filename, "r") as sql_file:
                # Split file in list
                ret = sql_file.read().split(';')
                # drop last empty entry
                ret.pop()
                return ret
        else:
            with open(filename, "r") as sql_file:
                # Split file in list
                ret = sql_file.read()
                return ret


if __name__ == "__main__":
    main()
