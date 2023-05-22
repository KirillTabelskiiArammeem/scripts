select date_created::date as date, extract(hour from date_created) as hour, count(*)
from queue_job qj
where id > 95937396 and date_created >= '2023-05-01'
group by date_created::date, extract(hour from date_created)
order by date, hour