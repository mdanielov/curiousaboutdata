
select distinct
[Type]=CASE b.type
when 'U' THEN 'Table'
when 'P' THEN 'Stored Procedure'
when 'F' THEN 'Function'
when 'FN' THEN 'Function'
when 'TF' THEN 'Table Function'	
when 'V' THEN 'View'
ELSE 'Tree' End,
object_name(a.id) [Object]
,a.name [Column Name]
,c.Name [DataType]
,a.prec
,a.colorder
--,a.scale
,isnullable
--,a.cdefault
--,COLUMNPROPERTY(a.id,a.name,'IsIdentity') [Identity]
,COLUMNPROPERTY(a.id,a.name,'GeneratedAlwaysType') [GeneratedAlwaysType]
--,a.* 
from syscolumns a JOIN sysobjects b ON a.id=b.id 
JOIN systypes c ON a.xtype=c.xtype

where 
1=1
--AND a.name='rdpaycode' 
and a.name like '%parent%'
--AND b.name='InventoryTag'
and b.type='U' 
AND c.name NOT IN ('sysname')
--and c.name not in ('int','uniqueidentifier','numeric','smallint','bigint','datetime','bit')
and b.type<>'S'
order by object, a.colorder


