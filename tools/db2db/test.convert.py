from sqlalchemy import (
    create_engine,
    MetaData,
    Table
)
from sqlalchemy.schema import CreateTable
from sqlalchemy.ext.compiler import compiles
# Import the specific dialect types we need to translate
from sqlalchemy.dialects import mssql, postgresql

# --- Step 1: Define the Custom Translation Rules ---

# This rule intercepts the special MSSQL TIMESTAMP (rowversion) type...
@compiles(mssql.TIMESTAMP, "postgresql")
def compile_mssql_timestamp(element, compiler, **kw):
    # ...and tells the compiler to output the text 'BYTEA' instead.
    return "BYTEA"

# This rule explicitly handles MSSQL DATETIME for clarity.
@compiles(mssql.DATETIME, "postgresql")
def compile_mssql_datetime(element, compiler, **kw):
    # It translates it to a standard timestamp without a time zone.
    return "TIMESTAMP WITHOUT TIME ZONE"


# --- Step 2: Connect to SQL Server and Reflect the Table ---

# Replace with your actual SQL Server connection string
SQL_SERVER_CONN_STR = "mssql://pentaho:pentaho@127.0.0.1:1434/YardManagement?driver=ODBC+Driver+17+for+SQL+Server"

# The name of the table you want to script
TABLE_NAME_TO_SCRIPT = "tblYardReport"
SCHEMA_NAME = "dbo"

sql_server_engine = create_engine(SQL_SERVER_CONN_STR)
metadata = MetaData()

print(f"Reflecting table '{SCHEMA_NAME}.{TABLE_NAME_TO_SCRIPT}' from SQL Server...")

try:
    reflected_table = Table(
        TABLE_NAME_TO_SCRIPT,
        metadata,
        schema=SCHEMA_NAME,
        autoload_with=sql_server_engine
    )
    print("Reflection successful.")
except Exception as e:
    print(f"Error reflecting table: {e}")
    exit()

# --- Step 3: Compile the CreateTable Statement for PostgreSQL ---
# No manual type changes are needed now. The custom rules handle it.
reflected_table.schema = "public"
create_table_statement = CreateTable(reflected_table)

# The str() call will now trigger our custom compilation rules
postgres_ddl_script = str(
    create_table_statement.compile(dialect=postgresql.dialect())
).strip()

print("\n--- Generated PostgreSQL CREATE TABLE Script ---")
print(postgres_ddl_script)