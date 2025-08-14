DO $$
DECLARE
    -- Declare a variable to hold the table name
    table_record RECORD;
BEGIN
    -- Loop through the results of a query that finds all foreign tables in the 'related' schema
    FOR table_record IN
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'related' AND table_type = 'FOREIGN'
    LOOP
        -- Execute the DROP FOREIGN TABLE command for each table found
        EXECUTE 'DROP FOREIGN TABLE related.' || quote_ident(table_record.table_name) || ';';
    END LOOP;
END;
$$ LANGUAGE plpgsql;

IMPORT FOREIGN SCHEMA public FROM SERVER related_db_dw INTO related;