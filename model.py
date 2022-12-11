import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv
load_dotenv()

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def make_top_song_artists_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS top_song_artists (artist_id INTEGER PRIMARY KEY UNIQUE, song_name TEXT, artist_name TEXT)") #change to artist_id
    conn.commit()

def make_spotify_artists_table(cur,conn):
    cur.execute(
        "CREATE TABLE IF NOT EXISTS spotify_artists_table (id INTEGER PRIMARY KEY UNIQUE, artist_id INTEGER, artist_name TEXT, artist_popularity NUMBER, artist_followers NUMBER, artist_spotify_id TEXT, artist_top_track_id TEXT)")  # keep artist name and num followers for now also change artist_popularity back to number
    conn.commit()

def make_twitter_artists_table(cur,conn):
    cur.execute(
        "CREATE TABLE IF NOT EXISTS twitter_artists_table(artist_id INTEGER, artist_name TEXT, artist_followers NUMBER, artist_twitter_id NUMBER)")  # keep artist name and num followers for now
    conn.commit()

def main():
    cur, conn = open_database('finalProjectDB.db')
    make_top_song_artists_table(cur, conn)
    make_spotify_artists_table(cur,conn)
    make_twitter_artists_table(cur,conn)


    #### FEEL FREE TO USE THIS SPACE TO TEST OUT YOUR FUNCTIONS

    conn.close()


if __name__ == "__main__":
    main()
   # unittest.main(verbosity = 2)
    