#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Returns a PostgreSQL DB connection to the tournament database.
    """

    try:
        conn = psycopg2.connect("dbname=tournament")
        return conn
    except:
        print "Unable to connect to tournament database."

def db_wrapper(func):
    """Wrapper function that connects to the PostgreSQL database, runs query from the wrapped function,
    then commit the change to the database and closes the connection.
    """

    def func_wrapper(*args):
        DB = connect()
        cur = DB.cursor()
        query = func(*args)
        if len(query) == 2:
            cur.execute(query[0], query[1])
        else:
            cur.execute(query[0])

        DB.commit()
        DB.close()

    return func_wrapper

@db_wrapper
def deleteMatches():
    """Remove all the match records from the database."""
    
    query = "DELETE FROM matches;"
    return [query]

@db_wrapper
def deletePlayers():
    """Remove all the player records from the database."""
    
    query = "DELETE FROM players;"
    return [query]


def countPlayers():
    """Returns the number of players currently registered."""

    DB = connect()
    cur = DB.cursor()
    query = " select count(id) as num FROM players;"
    cur.execute(query)
    count = cur.fetchone()
    DB.close()
    if count:
        return int(count[0])
    return 0

@db_wrapper
def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    query = " INSERT INTO players ( full_name ) values (%s);"
    return [query, (name,)]


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    DB = connect()
    cur = DB.cursor()
    playerStandings = []
    query_all_players = "select * from players;"
    query_a_players_win = "select count(winner) as win from matches where winner = %s"
    query_a_players_loss = "select count(loser) as loss from matches where loser = %s"

    cur.execute(query_all_players)
    all_players_list = cur.fetchall()

    for player in all_players_list:
        cur.execute(query_a_players_win, (int(player[0]),))
        win = cur.fetchone()
        cur.execute(query_a_players_loss, (int(player[0]),))
        loss = cur.fetchone()
        playerStandings.append((int(player[0]), player[1], int(win[0]), int(win[0]) + int(loss[0])))

    DB.close()
    return playerStandings
    
@db_wrapper
def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
 
    query = "INSERT INTO matches (winner, loser) values(%s, %s);"
    return [query, (winner, loser)]
 
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

    DB = connect()
    cur = DB.cursor()
    query = "select players.id, full_name, (select count(winner) from matches\
     where winner = players.id) as win from players, matches group by players.id order by win desc;"
    cur.execute(query)
    results = cur.fetchall()
    DB.close()
    pairings = []
    i = 0

    while i < len(results):
        pairings.append((results[i][0], results[i][1], results[i+1][0], results[i+1][1]))
        i += 2

    return pairings


