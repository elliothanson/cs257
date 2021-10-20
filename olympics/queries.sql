SELECT DISTINCT countries.NOC_region FROM countries
ORDER BY countries.NOC_region ASC;

SELECT DISTINCT athlete_names.full_name FROM athlete_names, athlete_information, countries
WHERE athlete_names.id = athlete_information.name_id AND
athlete_information.country_id = countries.id AND
countries.country_name LIKE 'Kenya';

SELECT athlete_information.medal, games.year, games.season, events.sport, events.event_name 
FROM athlete_information, athlete_names, games, events
WHERE athlete_information.name_id = athlete_names.id AND
athlete_information.games_id = games.id AND 
athlete_information.event_id = events.id AND
athlete_information.medal NOT LIKE 'NA' AND
athlete_names.full_name LIKE 'Gregory Efthimios (Greg) Louganis'
ORDER BY games.year;


SELECT countries.NOC_region, COUNT(athlete_information.id)
FROM countries, athlete_information
WHERE athlete_information.medal LIKE 'Gold' AND
athlete_information.country_id = countries.id
GROUP BY countries.NOC_region
ORDER BY COUNT(athlete_information.id) DESC;