-- 11. Titles of the five highest rated movies (in order) that Chadwick Boseman starred in, starting with the highest rated
SELECT title FROM movies JOIN stars ON movies.id = stars.movie_id JOIN ratings ON ratings.movie_id = stars.movie_id JOIN people ON people.id = stars.person_id WHERE name = 'Chadwick Boseman' ORDER BY rating DESC LIMIT 5;
