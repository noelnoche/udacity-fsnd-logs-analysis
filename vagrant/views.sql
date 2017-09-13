create or replace view top_articles as 
    select articles.title, count(log.path) as views from articles, log 
    where log.status = '200 OK' and log.path != '/' and log.path like concat('%', articles.slug) 
    group by articles.title order by views desc limit 3;

create or replace view top_authors as 
    select authors.name, subsq.views from authors, 
        (select articles.author, count(log.path) as views from articles, log 
        where log.status = '200 OK' and log.path != '/' and log.path like concat('%', articles.slug) 
        group by articles.author order by views desc) as subsq where authors.id = subsq.author;

create or replace view total_view as 
    select to_char(time, 'YYYY-MM-DD') as date, count(log.status) as total_requests from log 
    group by date order by date desc;
           
create or replace view failed_view as 
    select to_char(time, 'YYYY-MM-DD') as date, count(log.status) 
    as failed_requests from log where log.status = '404 NOT FOUND' 
    group by date order by date desc;

create or replace view error_reporter as 
    select f.date as date, 
    round((f.failed_requests/t.total_requests::float * 100)::numeric, 2) as percent_error 
    from (select * from failed_view) as f, (select * from total_view) as t 
    where f.date = t.date and f.failed_requests/t.total_requests::float * 100.00 > 1;
