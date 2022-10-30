use DB

select * from sys. dm_db_database_page_allocations(6,object_id('table_name'),0,NULL,'DETAILED' ) where page_type_desc = 'DATA_PAGE' order by allocated_page_page_id desc