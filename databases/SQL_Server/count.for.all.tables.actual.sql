DECLARE @SQL NVARCHAR(MAX) = N'';

-- Build the dynamic SQL string
SELECT @SQL = @SQL + 
    N'SELECT ''' + QUOTENAME(s.name) + '.' + QUOTENAME(t.name) + ''' AS TableName, ' +
    N'COUNT(*) AS cnt ' +
    N'FROM ' + QUOTENAME(s.name) + '.' + QUOTENAME(t.name) + N' UNION ALL '
FROM sys.tables t
JOIN sys.schemas s ON t.schema_id = s.schema_id
WHERE t.is_ms_shipped = 0; -- Excludes system tables

-- Remove the trailing ' UNION ALL ' from the final string
IF LEN(@SQL) > 0
    SET @SQL = LEFT(@SQL, LEN(@SQL) - 10);
    set @sql = @sql + char(13) + ' order by [cnt] desc'

-- Execute the generated statement
EXEC sp_executesql @SQL;