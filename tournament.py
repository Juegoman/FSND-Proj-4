#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import bleach
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    query = "DELETE FROM matches"
    c.execute(query)
    query = "UPDATE players SET matches = 0"
    c.execute(query)
    query = "UPDATE players SET wins = 0"
    c.execute(query)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    query = "DELETE FROM players CASCADE"
    c.execute(query)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    query = "SELECT count(id) AS num FROM players"
    c.execute(query)
    count = int(c.fetchall()[0][0])
    conn.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Also makes sure that the name is properly escaped to prevent SQL injection
    attacks.

    Args:
      name: the player's full name (need not be unique).
    """
    safe_name = bleach.clean(name)
    conn = connect()
    c = conn.cursor()
    query = "INSERT INTO players (name) VALUES (%s)"
    c.execute(query, (str(safe_name),))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    query = "SELECT * FROM players ORDER BY wins DESC"
    c.execute(query)
    standings = c.fetchall()
    conn.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    # First, insert the match into the matches table.
    query = "INSERT INTO matches (winner, loser) VALUES (%d, %d)" % (winner,
                                                                     loser)
    c.execute(query)
    # Then, update the players to reflect that they had a match.
    query = "UPDATE players SET matches = (matches + 1) WHERE " \
            "id = %d OR id = %d" % (winner, loser)
    c.execute(query)
    # Finally, update the winner in the players table with their win.
    query = "UPDATE players SET wins = (wins + 1) WHERE id = %d" % (winner)
    c.execute(query)
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    result = []
    players = playerStandings()
    # While there are still enough players to pair.
    while len(players) > 1:
        # pop a player and add them to a pairing
        player = players.pop()
        pairing = (player[0], player[1],)
        # pop another player and complete the pairing
        player = players.pop()
        pairing = pairing + (player[0], player[1],)
        # then append the pairing to the result list
        result.append(pairing)
    return result
