select [type], [type_desc],count(1) [cnt]
from sys.objects
where [type] not in ('S','IT')
group by [type], [type_desc]
order by 3 desc
