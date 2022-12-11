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
import numpy as np

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_visual_one(cur, conn):
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_URL = os.getenv("REDIRECT_URL")
    client_credentials_manager = SpotifyClientCredentials(
        CLIENT_ID, CLIENT_SECRET)
    spotify = spotipy.Spotify(
        client_credentials_manager=client_credentials_manager)

    cur.execute("SELECT spotify_artists_table.artist_top_track_id, top_song_artists.song_name, top_song_artists.artist_name \
        FROM spotify_artists_table JOIN top_song_artists ON spotify_artists_table.artist_id = top_song_artists.artist_id \
        ORDER BY spotify_artists_table.artist_followers DESC \
        LIMIT 10")
    song_list = cur.fetchall()

    artist_list = [x[2] for x in song_list]
    top_track_POP_list = []
    shazam_track_POP_list = []
    for song in song_list:
        top_track_POP_search = spotify.track(song[0])
        top_track_POP = top_track_POP_search['popularity']

        shazam_track_POP_search = spotify.search(
            'track:' + song[1] + ' artist:' + song[2], type='track')
        shazam_track_POP = shazam_track_POP_search['tracks']['items'][0]['popularity']
        top_track_POP_list.append(top_track_POP)
        shazam_track_POP_list.append(shazam_track_POP)
        print(top_track_POP)

    cur.execute("SELECT spotify_artists_table.artist_top_track_id, top_song_artists.song_name, top_song_artists.artist_name \
        FROM spotify_artists_table JOIN top_song_artists ON spotify_artists_table.artist_id = top_song_artists.artist_id \
        ORDER BY spotify_artists_table.artist_followers DESC")
    calc_list = cur.fetchall()

    with open('song_popularity_calc.txt', 'w') as f:
        for song in calc_list:
            top_track_POP_search = spotify.track(song[0])
            top_track_POP = top_track_POP_search['popularity']
            top_track_name = top_track_POP_search['name']

            shazam_track_POP_search = spotify.search(
                'artist:' + song[2] + ' track:' + song[1], type='track')
            if not shazam_track_POP_search['tracks']['items']:
                shazam_track_POP_search = spotify.search(
                    'track:' + song[1], type='track')
            shazam_track_POP = shazam_track_POP_search['tracks']['items'][0]['popularity']
            shazam_track_name = shazam_track_POP_search['tracks']['items'][0]['name']
            f.write(str(song[2]) + "'s top spotify track, " + top_track_name + ", has a popularity of " + str(top_track_POP) +
                    " and their most shazamed song, " + shazam_track_name + ", has a popularity of " + str(shazam_track_POP) + ".\n")
    



    X = 10
    width = 0.35
    ind = np.arrange(X) 

    fig, ax = plt.subplots()

    bar1 = ax.bar(ind, top_track_POP_list, width, color="yellow")
    bar2 = ax.bar(ind + width, shazam_track_POP_list, width, color="blue")

    #legend
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels = [artist_list[0], artist_list[1], artist_list[2], artist_list[3], artist_list[4], artist_list[5], artist_list[6], artist_list[7], artist_list[8], artist_list[10]]
    ax.legend((bar1[0], bar2[0]), ("Top Song", "Shazam Song"))
    ax.autoscale_view

    #set x, y axis and title
    ax.set(xlabel = "Artist", ylabel = "Popularity", title="Top Song Popularity vs Shazam Song Popularity for Top 10 Artists")
    fig.savefig("TrackPopularityGraph")
    plt.show()


    
def main():
    cur, conn = open_database('finalProjectDB.db')
    create_visual_one(cur, conn)


    #### FEEL FREE TO USE THIS SPACE TO TEST OUT YOUR FUNCTIONS

    conn.close()


if __name__ == "__main__":
    main()
   # unittest.main(verbosity = 2)
