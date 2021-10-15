CREATE TABLE athlete_information(
    id INTEGER,
    name_id integer,
    sex text,
    age text,
    height text,
    weight text,
    country_id integer,
    games_id integer,
    event_id integer,
    medal text
);

CREATE TABLE athlete_names(
    id INTEGER,
    full_name text
);

CREATE TABLE games(
    id INTEGER,
    game_name text,
    season text,
    year text,
    city text
);

CREATE TABLE countries(
    id INTEGER,
    country_name text,
    NOC_region text
);

CREATE TABLE events(
    id INTEGER,
    event_name text,
    sport text
);

