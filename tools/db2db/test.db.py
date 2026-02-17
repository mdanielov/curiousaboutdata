import sqlalchemy
from sqlalchemy.engine import URL

connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=127.0.0.1;DATABASE=personal;UID=pentaho;PWD=pentaho"

connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

engine = sqlalchemy.create_engine(connection_url)

conn = engine.raw_connection()

cursor = conn.cursor()

query = "SELECT name FROM sys.tables order by name"

result = cursor.execute(query)

for row in result:
    print(row[0])