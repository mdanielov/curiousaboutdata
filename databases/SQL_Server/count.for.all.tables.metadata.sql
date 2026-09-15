use KiMeTzion
SELECT 
    QUOTENAME(s.name) + '.' + QUOTENAME(t.name) AS TableName,
    SUM(p.rows) AS cnt
FROM sys.tables t
JOIN sys.schemas s ON t.schema_id = s.schema_id
JOIN sys.indexes i ON t.object_id = i.object_id
JOIN sys.partitions p ON i.object_id = p.object_id AND i.index_id = p.index_id
WHERE t.is_ms_shipped = 0
  AND i.type IN (0,1) -- 0 = Heap, 1 = Clustered Index (prevents double-counting non-clustered indexes)
GROUP BY s.name, t.name
ORDER BY cnt DESC; -- Optional: sorts from largest table to smallest