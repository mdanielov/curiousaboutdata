
declare @tb_name varchar(60) = 'Metrics'
,@schema_name varchar(60) ='135664'
DECLARE @TempTable AS TABLE (SchemaName VARCHAR(100), 
							 ObjectID INT, 
							 TableName VARCHAR(100), 
							 IndexID INT, 
							 IndexName VARCHAR(100), 
							 ColumnID INT, 
							 column_index_id INT, 
							 ColumnNames  VARCHAR(500), 
							 IncludeColumns  VARCHAR(500), 
							 NumberOfColumns INT, 
							 IndexType  VARCHAR(200),
							 LastColRecord INT);

WITH CTE_Indexes (SchemaName, ObjectID, TableName, IndexID, IndexName, ColumnID, column_index_id, ColumnNames, IncludeColumns, NumberOfColumns, IndexType)
AS
(
SELECT s.name
, t.object_id
, t.name
, i.index_id
, i.name
, c.column_id
, ic.index_column_id
, CASE ic.is_included_column WHEN 0 THEN CAST(c.name AS VARCHAR(5000)) ELSE '' END, 
CASE ic.is_included_column WHEN 1 THEN CAST(c.name AS VARCHAR(5000)) ELSE '' END
, 1
, i.type_desc
	FROM  sys.schemas AS s
		JOIN sys.tables AS t ON s.schema_id = t.schema_id
		JOIN sys.indexes AS i ON i.object_id = t.object_id
		JOIN sys.index_columns AS ic ON ic.index_id = i.index_id AND ic.object_id = i.object_id
		JOIN sys.columns AS c ON c.column_id = ic.column_id AND c.object_id = ic.object_id AND ic.index_column_id = 1
	where t.name = @tb_name
	and s.name = @schema_name
UNION ALL

SELECT s.name
, t.object_id
, t.name
, i.index_id
, i.name
, c.column_id
, ic.index_column_id
, CASE ic.is_included_column WHEN 0 THEN CAST(cte.ColumnNames + ', ' + c.name AS VARCHAR(5000))  ELSE cte.ColumnNames END
, CASE  WHEN ic.is_included_column = 1 AND cte.IncludeColumns != '' THEN CAST(cte.IncludeColumns + ', ' + c.name AS VARCHAR(5000))
		WHEN ic.is_included_column =1 AND cte.IncludeColumns = '' THEN CAST(c.name AS VARCHAR(5000)) 
			ELSE '' END
, cte.NumberOfColumns + 1
, i.type_desc
	FROM  sys.schemas AS s
		JOIN sys.tables AS t ON s.schema_id = t.schema_id
		JOIN sys.indexes AS i ON i.object_id = t.object_id
		JOIN sys.index_columns AS ic ON ic.index_id = i.index_id AND ic.object_id = i.object_id
		JOIN sys.columns AS c ON c.column_id = ic.column_id AND c.object_id = ic.object_id 
		JOIN CTE_Indexes cte ON cte.Column_index_ID + 1 = ic.index_column_id  AND cte.IndexID = i.index_id AND cte.ObjectID = ic.object_id
	where t.name = @tb_name
	and s.name = @schema_name
)
INSERT INTO  @TempTable 
SELECT *, RANK() OVER (PARTITION BY ObjectID, IndexID ORDER BY NumberOfColumns DESC) AS LastRecord FROM CTE_Indexes AS cte;

SELECT SchemaName, TableName, IndexName, ColumnNames, IncludeColumns, IndexType FROM @TempTable
WHERE LastColRecord = 1
ORDER BY objectid, TableName, indexid, IndexName