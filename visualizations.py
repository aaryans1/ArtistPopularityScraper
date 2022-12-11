import requests
import json
import sqlite3
import os
import matplotlib
import matplotlib.pyplot as plt
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import tweepy

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_visual_one(cur, conn):
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_URL = os.getenv("REDIRECT_URL")
    client_credentials_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    cur.execute("SELECT spotify_artists_table.artist_top_track_id, top_song_artists.song_name, top_song_artists.artist_name \
        FROM spotify_artists_table JOIN top_song_artists ON spotify_artists_table.artist_id = top_song_artists.artist_id \
        ORDER BY spotify_artists_table.artist_followers DESC \
        LIMIT 10")
    song_list = cur.fetchall()

    artist_list = [x[2] for x in song_list]
    
    for song in song_list:
        top_track_POP = spotify.track(song[0])
        shazam_track_POP = spotify.search('track:' + song[1], type='track')
        print(shazam_track_POP)

    cur.execute("SELECT spotify_artists_table.artist_top_track_id, top_song_artists.song_name, top_ \
        FROM spotify_artists_table JOIN top_song_artists ON spotify_artists_table.artist_id = top_song_artists.artist_id \
        ORDER BY spotify_artists_table.artist_followers DESC")
    calc_list = cur.fetchall()
    

    labels = #artist name 
    top_song_pop = #artist top song popularity
    shazam_song_pop = #popularity of artist's shazamed song

    plt.xlabel("Artist")
    plt.ylabel("Popularity")
    plt.title("Top Song vs Top Shazamed Song Popularity for Top 10 Artists")
    
    fig, ax = plt.subplots()
    ax.plot(labels, top_song_pop, label="Top Song")
    ax.plot(labels,shazam_song_pop, label="Top Shazam Song")
    ax.legend()
    
def main():
    cur, conn = open_database('finalProjectDB.db')
    create_visual_one(cur, conn)


    #### FEEL FREE TO USE THIS SPACE TO TEST OUT YOUR FUNCTIONS

    conn.close()


if __name__ == "__main__":
    main()
   # unittest.main(verbosity = 2)
