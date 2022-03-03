
GO
DECLARE 
@INPUT VARCHAR(50),
@INDEX1 INT,
@INDEX2 INT,
@obj	int,
@spidid	int

--set @spidid=73

/* paste here the value from waitresource */

--SET @INPUT=Replace(RTRIM((select waitresource from master..sysprocesses with (nolock) where spid=@spidid)),'PAG: ','')
SET @INPUT='10:1:22698'
IF @input is null or @input='' goto exit_here

/* get the position of the first colon */
SET  @INDEX1=CHARINDEX(':',@INPUT)
--select @input
/* get the position of the second colon */
SET @INDEX2=@INDEX1+CHARINDEX(':',right(@INPUT,LEN(@INPUT)-@INDEX1))

/* create a temp table to hold dbcc page results */
create table #my_tb
(
parentObject varchar(200),
object varchar(200),
field varchar(200),
value varchar(200)
)

/* convert the page address format from colon delimited to comma delimited */
DECLARE @STR VARCHAR (2000)
SET @STR='dbcc PAGe ('+LEFT(@INPUT,@INDEX1-1)+','+
SUBSTRING(@INPUT,@INDEX1+1,@INDEX2-@INDEX1-1)+','+
RIGHT(@INPUT,LEN(@INPUT)-@INDEX2)+',0) with tableresults'

/* store the output of dbcc page into the temp table */
insert into #my_tb exec(@STR)

/* query sysobjects to find out what object this page belongs to */
set @obj=(select value from #my_tb where field ='Metadata: ObjectId')

declare 
@statement nvarchar(500),
@params1 Nvarchar(200),
@params2 Nvarchar(200),
@name_db sysname,
@name_obj sysname,
@pg_num varchar(20)

set @pg_num=RIGHT(@INPUT,LEN(@INPUT)-@INDEX2)

set @name_db=db_name(LEFT(@INPUT,@INDEX1-1))
set @name_obj=object_name(@obj)

IF exists (select 1 from sysobjects where id=@obj)
	BEGIN
set @statement='use ' + @name_db +' select @obj as [ObjectID],@pg_num as [Page],@db_name as [Database], 
@obj_name as [Object_Name], Type as [Object_Type] from '+
rtrim(@name_db)+'..sysobjects where id=@obj'
set @params1='@db_name sysname, @obj_name sysname, @obj int, @pg_num varchar(20)'
set @params2='@db_name=db_name(LEFT(@INPUT,@INDEX1-1)),@obj_name=object_name(@obj),@pg_num=@pg_num'

exec sp_executesql @statement,@params1,
@db_name=@name_db,@obj_name=@name_obj,@obj=@obj,@pg_num=@pg_num
	END

--select @obj as [ObjectID],@name_db as [Database], @name_obj as [Object_Name]
/* clean up */
select * from #my_tb
drop table #my_tb

exit_here: