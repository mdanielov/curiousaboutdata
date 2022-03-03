

create table #tb1
(PgeFID int
,PagePID int
,IAMFID int
,IAMPID int
,objectID int
,indexID int
,PartitionNumber int
,PartitionID bigint
,iam_chain_type varchar(12)
,PageType int
,indexLevel int
,nextPageFID int
,nextPagePID int
,PrevPageFID int
,PrevPagePID int
)
DECLARE @STR VARCHAR (2000)
SET @STR='dbcc IND (0,''my_table'',1)'
insert into #tb1 
exec(@STR)

select * from #tb1 