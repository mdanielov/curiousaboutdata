declare @table nvarchar(128)

set @table = 'TransactionsByCountry'


select DATALENGTH(A.name) [bytes]
,A.[name]
,A.[column_id]
,B.name [sys_type_name]
,A.max_length
,A.precision
,A.is_nullable
,A.is_identity
        from  sys.columns A
		JOIN sys.types B ON A.system_type_id = B.system_type_id
        where object_id = (select top 1 object_id from sys.objects where name = @table)
        and   is_computed = 0