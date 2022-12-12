#import requests
import json
import sqlite3
import os
import matplotlib.pyplot as plt
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import numpy as np

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_visual_one(cur, conn, spotify):
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
        

    
    



    X = 10
    width = .35
    ind = np.arange(X) 

    fig, ax = plt.subplots()
    plt.figure(figsize=(20, 3))
    bar1 = ax.bar(ind, top_track_POP_list, width, color="palegreen")
    bar2 = ax.bar(ind + width, shazam_track_POP_list, width, color="steelblue")

    #legend
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels((artist_list[0], artist_list[1], artist_list[2], artist_list[3], artist_list[4], artist_list[5], artist_list[6], artist_list[7], artist_list[8], artist_list[9]))
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    ax.legend((bar1[0], bar2[0]), ("Top Spotify Song", "Top Shazam Song"))


    #set x, y axis and title
    ax.set(xlabel = "Artist", ylabel = "Popularity (%)", title="Top Spotify Song Popularity vs Top Shazam Song Popularity for Top 10 Artists")
    fig.savefig("TrackPopularityGraph.png")
    plt.show()

def create_visual_two(cur,conn):
    cur.execute("SELECT spotify_artists_table.artist_followers, twitter_artists_table.artist_followers, spotify_artists_table.artist_name \
        FROM spotify_artists_table JOIN twitter_artists_table ON spotify_artists_table.artist_id = twitter_artists_table.artist_id \
        ORDER BY twitter_artists_table.artist_followers DESC LIMIT 15")
    pop_list = cur.fetchall()
    


    spotify_followers_list = []
    for s, _, _ in pop_list:
        spotify_followers_list.append(s)
     
    twitter_followers_list = []
    for _, i, _ in pop_list:
        twitter_followers_list.append(i)

    names = []
    for _, _, name in pop_list:
        names.append(name)
    

    
    twitter_POP_list = []
    # top_artist_followers = 113655496
    for i in twitter_followers_list:
        x = int((i / (pop_list[0][1])) * 100)
        twitter_POP_list.append(x)


    cur.execute("SELECT MAX(artist_followers) FROM spotify_artists_table")
    max_followers = cur.fetchone()[0]
    spotify_POP_list = []
    for i in spotify_followers_list:
        x = int((i / (max_followers)) * 100)
        spotify_POP_list.append(x)
        

    X = 15
    width = .35
    ind = np.arange(X) 

    fig, ax = plt.subplots()
    plt.figure(figsize=(20, 3))
    bar1 = ax.bar(ind, spotify_POP_list, width, color="darkmagenta")
    bar2 = ax.bar(ind + width, twitter_POP_list, width, color="palegreen")

    #legend
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels((names[0], names[1], names[2], names[3], names[4], names[5], names[6], names[7], names[8], names[9], names[10],names[11],names[12],names[13],names[14]))
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    ax.legend((bar1[0], bar2[0]), ("Spotify Popularity Index", "Twitter Popularity Index"))


    #set x, y axis and title
    ax.set(xlabel = "Artist", ylabel = "Popularity (%)", title="Top 15 Shazamed Artist's Popularity on Spotify vs Twitter")
    fig.savefig("ArtistPopularityGraph.png")
    plt.show()

def create_visual_three(cur,conn):
    cur.execute("SELECT spotify_artists_table.artist_followers, twitter_artists_table.artist_followers, spotify_artists_table.artist_name \
        FROM spotify_artists_table JOIN twitter_artists_table ON spotify_artists_table.artist_id = twitter_artists_table.artist_id \
        ORDER BY twitter_artists_table.artist_followers DESC LIMIT 15")
    
    list_of_artist_data = cur.fetchall()
    spotify_followers = []
    twitter_followers = []
    artist_names = []

    for s,t,n in list_of_artist_data:
        spotify_followers.append(s)
        twitter_followers.append(t)
        artist_names.append(n)
    
    X = 15
    width = .35
    ind = np.arange(X) 

    fig, ax = plt.subplots()
    plt.figure(figsize=(20, 3))
    bar1 = ax.bar(ind, spotify_followers, width, color="darkturquoise")
    bar2 = ax.bar(ind + width, twitter_followers, width, color="lightcoral")

    #legend
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels((artist_names[0], artist_names[1], artist_names[2], artist_names[3], artist_names[4], artist_names[5], artist_names[6], artist_names[7], artist_names[8], artist_names[9], artist_names[10],artist_names[11],artist_names[12],artist_names[13],artist_names[14]))
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    ax.legend((bar1[0], bar2[0]), ("Spotify Followers", "Twitter Followers"))


    #set x, y axis and title
    ax.set(xlabel = "Artist", ylabel = "Followers (Millions)", title="Spotify Followers vs Twitter Followers for Top 15 Artists")
    fig.savefig("FollowersGraph.png")
    plt.show()



def create_song_popularity_calc(cur,conn,spotify):
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

def create_artist_popularity_calc(cur,conn):
    cur.execute("SELECT spotify_artists_table.artist_followers, twitter_artists_table.artist_followers, spotify_artists_table.artist_name \
        FROM spotify_artists_table JOIN twitter_artists_table ON spotify_artists_table.artist_id = twitter_artists_table.artist_id \
        ORDER BY twitter_artists_table.artist_followers DESC")
    pop_list_total = cur.fetchall()

    twitter_followers_list = []
    for _, i, _ in pop_list_total:
        twitter_followers_list.append(i)

    twitter_POP_list = []
    for i in twitter_followers_list:
        x = int((i / (pop_list_total[0][1])) * 100)
        twitter_POP_list.append(x)

    spotify_followers_list = []
    for s, _, _ in pop_list_total:
        spotify_followers_list.append(s)
    
    cur.execute("SELECT MAX(artist_followers) FROM spotify_artists_table")
    max_followers = cur.fetchone()[0]
    spotify_POP_list = []
    for i in spotify_followers_list:
        x = int((i / (max_followers)) * 100)
        spotify_POP_list.append(x)

    with open('artist_popularity_calc.txt', 'w') as f:
        for i in range(len(pop_list_total)):
            f.write((str(pop_list_total[i][2])) + " has a Spotify popularity index of " + str(spotify_POP_list[i]) + " and a Twitter popularity index of " + str(twitter_POP_list[i]) + ".\n")
        

    



    

    
def main():
    cur, conn = open_database('finalProjectDB.db')

     # CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_ID = 'f23a7b980c684642b807c7be4fc4d799'
    # CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    CLIENT_SECRET = 'a9aac79406ef4ab69f0ae4c0944d470a'
   
    # REDIRECT_URL = os.getenv("REDIRECT_URL")
    client_credentials_manager = SpotifyClientCredentials(
        CLIENT_ID, CLIENT_SECRET)
    spotify = spotipy.Spotify(
        client_credentials_manager=client_credentials_manager)

    create_visual_one(cur, conn,spotify)
    create_visual_two(cur,conn)
    create_visual_three(cur,conn)
    create_artist_popularity_calc(cur, conn)
    create_song_popularity_calc(cur,conn,spotify)

    #### FEEL FREE TO USE THIS SPACE TO TEST OUT YOUR FUNCTIONS

    conn.close()


if __name__ == "__main__":
    main()
   # unittest.main(verbosity = 2)
