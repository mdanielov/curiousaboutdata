
--add the extension
CREATE EXTENSION postgres_fdw;

--create server
CREATE SERVER related_db_dw
        FOREIGN DATA WRAPPER postgres_fdw
        OPTIONS (host 'localhost', dbname 'other_database', port '5432');

--even if you're on the same server, need to create a mapping
CREATE USER MAPPING FOR current_user
        SERVER related_db_dw
        OPTIONS (user 'postgres', password 'mypwd');
		
--in the target DB create a schema that will hold all foreign tables
create schema related;

--create all tables
IMPORT FOREIGN SCHEMA public FROM SERVER related_db_dw INTO related;