declare @srch1 varchar(50)
/* specify the searchstring here */
set @srch1='message_introduction'

--fn_StrReplCtrlChar_Unicode
--fn_StrReplForCCXmlGWB_Unicode
--fn_StrStripNonAlpha

select name,type,min(text) from (
     SELECT top 100 percent 
Object_Name(c1.id) name,
'type'= CASE
when objectproperty(c1.id,'IsProcedure')=1 THEN 'Procedure'
when objectproperty(c1.id,'IsTrigger')=1 THEN 'Trigger'
when objectproperty(c1.id,'IsTable')=1 THEN 'Table' 
when objectproperty(c1.id,'IsView')=1 THEN 'View' 
WHEN objectproperty(c1.id,'IsTableFunction')=1 OR objectproperty(c1.id,'IsScalarFunction')=1 OR objectproperty(c1.id,'IsInlineFunction')=1 
THEN 'Function' 
when objectproperty(c1.id,'IsDefault')=1 THEN 'Default' 
when objectproperty(c1.id,'IsRule')=1 THEN 'Rule' 
ELSE 'unknown' END,substring(c1.text,(CHARINDEX(@srch1,c1.text)-50),200) as [text]
     FROM syscomments c1
     LEFT OUTER JOIN syscomments c2 ON c1.id = c2.id AND c2.number = c1.number + 1
     WHERE 
Cast( c1.text AS varchar(4000) )+ Coalesce( Cast( c2.text AS varchar(4000) ), '' ) LIKE '%'+@srch1+'%' ) A
group by name,type

ORDER BY 1

