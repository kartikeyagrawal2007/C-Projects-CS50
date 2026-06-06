-- 12. Titles of all of movies in which both Jennifer Lawrence and Bradley Cooper starred
select title
from movies
where id in(
    select movie_id from stars
    where person_id = (
        select id
        from people where name = 'Bradley Cooper'
    )
)
AND id in (
    select movie_id
    from stars
    where person_id =(
        select id
        from people
        where name = 'Jennifer Lawrence'
    )
);
