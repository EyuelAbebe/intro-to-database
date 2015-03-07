-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Table for player names
CREATE TABLE players ( id SERIAL NOT NULL UNIQUE  PRIMARY KEY,
                       full_name VARCHAR(90) );

-- Table for all matches.
CREATE TABLE matches ( id SERIAL NOT NULL UNIQUE PRIMARY KEY,
                       winner integer references players (id),
                       loser integer references players (id) );
