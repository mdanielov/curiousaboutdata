
;with names as
(select name from sys.tables group by name having count(1) > 1)
,tb_ids as
(select ROW_NUMBER() OVER (partition by name order by object_id) [rn],* from sys.tables where name in (select name from names))
select SUM(
CASE WHEN DATALENGTH(A.name) > max_length THEN max_length ELSE DATALENGTH(A.name)
END) [bytes]
,SUM(max_length) [max_bytes]
,OBJECT_NAME(A.object_id) [table]
        from  sys.columns A
		JOIN tb_ids B ON A.object_id = B.object_id and B.rn=1
        and   is_computed = 0
GROUP BY OBJECT_NAME(A.object_id)
WITH ROLLUP