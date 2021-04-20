import configparser
import codecs
import pymysql.cursors
import subprocess
import os


config = configparser.ConfigParser()
config.read('restore.setting.ini')
host = config.get('mysql', 'host')
mysql_port = config.get('mysql', 'port')
user = config.get('mysql', 'user')
password = config.get('mysql', 'password')
db_name = config.get('mysql', 'db')
root_dir = config.get('mysql', 'restore_dir')
put_routines = int(config.get('mysql', 'put_routines'))
put_schema = int(config.get('mysql', 'put_schema'))
put_data = int(config.get('mysql', 'put_data'))
mysql_dir = config.get('mysql', 'mysql_dir')
mysql='"' +mysql_dir + "mysql.exe"+'"'

conn1 = pymysql.connect(host=host, port=int(mysql_port), user=user, password=password, database="mysql")


def main():
    # check if db exists on target, if not create
    qry_create_db = "CREATE DATABASE IF NOT EXISTS {};".format(db_name)
    cur1 = conn1.cursor()
    cur1.execute(qry_create_db)
    for r in cur1.fetchall():
        print(r)
        print("")
        conn1.commit()
    conn1.close()

    conn2 = pymysql.connect(host=host, port=int(mysql_port), user=user, password=password, database=db_name)
    cur = conn2.cursor()

    # check if root dir exists
    if os.path.isdir(root_dir):
        # process schema
        if put_schema == 1:
            if os.path.isdir(os.path.join(root_dir, "schema")):
                walk_dirs(os.path.join(root_dir, "schema"), cur, "schema")
        if put_data == 1:
            # process data
            if os.path.isdir(os.path.join(root_dir, "data")):
                walk_dirs(os.path.join(root_dir, "data"), cur, "data")

    conn2.close()


def restore_from_dir(dir_name, cur):
    if os.path.isdir(dir_name):
        files = tree_walker(dir_name, 'file')
        for f in files:
            print("working on {}".format(f))
            fl = codecs.open(os.path.join(dir_name, f), 'r', 'UTF-8')
            qry_str = fl.read()
            fl.close()
            restore_string = mysql+" -h {} -P {} -u {} --password={} {} < {}".format(host, mysql_port, user, password, db_name, os.path.join(dir_name, f))

            res = subprocess.Popen(restore_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out, err = res.communicate()
            if err:
                print(err)

def walk_dirs(dir_name, cur, dir_type):
    if dir_type == "schema":
        tbl_dir = os.path.join(dir_name, "tables")
        restore_from_dir(tbl_dir, cur)

        func_dir = os.path.join(dir_name, "Functions")
        restore_from_dir(func_dir, cur)

        proc_dir = os.path.join(dir_name, "Procedures")
        restore_from_dir(proc_dir, cur)

    if dir_type == "data":
        restore_from_dir(dir_name, cur)


def tree_walker(root_dir, return_type):
    for root, dirs, files in os.walk(root_dir):
        if return_type == 'dir':
            return dirs
        else:
            return files


def parse_sql(data):
    stmts = []
    DELIMITER = ';'
    stmt = ''

    for lineno, line in enumerate(data):
        if not line.strip():
            continue

        if line.startswith('--'):
            continue

        if 'DELIMITER' in line:
            DELIMITER = line.split()[1]
            continue

        if (DELIMITER not in line):
            stmt += line.replace(DELIMITER, ';')
            continue

        if stmt:
            stmt += line
            stmts.append(stmt.strip())
            stmt = ''
        else:
            stmts.append(line.strip())
    return stmts


if __name__ == "__main__":
    main()
