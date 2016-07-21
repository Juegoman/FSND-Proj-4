-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (
  id SERIAL PRIMARY KEY,
  name text
);
CREATE TABLE matches (
  id SERIAL PRIMARY KEY,
  winner int references players(id) NOT NULL,
  loser int references players(id) NOT NULL
);
CREATE VIEW wincounter AS
  SELECT players.id,
         COUNT (matches.winner) AS wins
  FROM   players
         LEFT JOIN matches
                ON players.id = matches.winner
  GROUP  BY players.id;
CREATE VIEW losscounter AS
  SELECT players.id,
         COUNT (matches.loser) AS losses
  FROM   players
         LEFT JOIN matches
                ON players.id = matches.loser
  GROUP  BY players.id;
CREATE VIEW playerstandings AS
  SELECT players.id,
         players.name,
         wincounter.wins,
         (losscounter.losses + wincounter.wins) AS matches
  FROM   players, wincounter, losscounter
  WHERE  wincounter.id = players.id and losscounter.id = players.id
