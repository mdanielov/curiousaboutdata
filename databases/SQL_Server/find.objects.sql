
SET NOCOUNT on
DECLARE @srch sysname = 'something_to_search'
,@dbname sysname
,@cntr INT = 1
,@obj_count int
,@qry NVARCHAR(MAX)
,@qry_params NVARCHAR(MAX) = '@obj_count int OUTPUT'
DECLARE @tbl_list TABLE (
list_id INT IDENTITY
,d_name sysname
)

IF object_id ('tempdb..#obj_list') is not NULL
DROP TABLE #obj_list

create table #obj_list (
database_name sysname,
obj_name sysname)

INSERT @tbl_list(d_name)
SELECT name FROM sys.databases WHERE name NOT IN('master', 'tempdb', 'model', 'msdb') 
WHILE EXISTS (SELECT 1 FROM @tbl_list)
BEGIN
SET @obj_count = 0
SET @dbname= (SELECT d_name FROM @tbl_list WHERE list_id = @cntr)
SET @qry='set @obj_count=(select count(1) from ['+@dbname+'].sys.objects where UPPER(name) like ''%'+@srch+'%'' )'
EXECUTE sp_executesql @qry,@qry_params,@obj_count=@obj_count OUT

if @obj_count > 0

BEGIN
PRINT @dbname+' contains target object'
INSERT #obj_list
exec('select '''+@dbname+''' [db_name],name from ['+@dbname+'].sys.objects where UPPER(name) like ''%'+@srch+'%''')
END
DELETE @tbl_list WHERE list_id = @cntr
SET @cntr +=1
END

select * from #obj_list