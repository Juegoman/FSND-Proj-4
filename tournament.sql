-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players (
  id SERIAL PRIMARY KEY,
  name text,
  wins int DEFAULT 0,
  matches int DEFAULT 0
);
CREATE TABLE matches (
  id SERIAL PRIMARY KEY,
  winner int references players(id) NOT NULL,
  loser int references players(id) NOT NULL
);
