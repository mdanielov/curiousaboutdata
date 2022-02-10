/*
extended stored procedure parameters are as follows:

Value of error log file you want to read: 0 = current, 1 = Archive #1, 2 = Archive #2, etc...
Log file type: 1 or NULL = error log, 2 = SQL Agent log
Search string 1: String one you want to search for
Search string 2: String two you want to search for to further refine the results
Search from start time  
Search to end time
Sort order for results: N'asc' = ascending, N'desc' = descending
*/
if object_id('tempdb..#tb') is not null
drop table #tb
create table #tb (Logdate datetime, ProcessInfo sysname,Text varchar(max))

insert into #tb 
EXEC master.dbo.xp_readerrorlog 1,1,null,null,null,null,N'desc'

select top 50 * from #tb where ProcessInfo not in ('Backup')
 --and text not like 'The log shipping%' 
 and text not like '%login%' and text not like '%Error: 18456%'
 --and processInfo !='logon'
-- and text like '%XML%'
  order by 1 desc
  