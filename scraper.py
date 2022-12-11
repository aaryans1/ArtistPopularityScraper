from bs4 import BeautifulSoup
import requests
import sqlite3
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import tweepy
import re
load_dotenv()

def getSongData(cur,conn):
    
    cur.execute("SELECT COUNT(*) FROM top_song_artists")
    table_size = cur.fetchone()[0]
    url = 'https://www.shazam.com/charts/top-200/united-states'
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    song_list = soup.find_all(
        'a', {'data-shz-beacon-id': 'charts.ue-track-title'})
    artist_list = soup.find_all(
        'a', {'data-shz-beacon-id': 'charts.ue-track-artist'})
    if table_size == 200:
        pass
    else:
        if table_size == 0:
            for i in range(1, 26):
                temp_title = song_list[i-1].text
                temp_artist = artist_list[i-1].text
                temp_artist = temp_artist.split(',')[0]
                temp_artist = temp_artist.split('&')[0]
                temp_artist = temp_artist.strip()
                temp_title = temp_title.split('(')[0].strip()



                # INSERT OR IGNORE INTO Employees(employee_id, first_name, last_name, job_id, hire_date, salary) VALUES (?,?,?,?,?,?)', (emp_id, first_name,last_name,job_id, hire_date,salary))
                cur.execute("INSERT INTO top_song_artists(artist_id, song_name, artist_name) VALUES(?,?,?)", (i, temp_title, temp_artist))
            
        else:
            for i in range(0, 25):
                cur.execute("SELECT COUNT(*) FROM top_song_artists")
                table_size = cur.fetchone()[0]
                if table_size == 200:
                    break
                temp_title = song_list[table_size].text
                temp_artist = artist_list[table_size].text
                temp_artist = temp_artist.split(',')[0]
                temp_artist = temp_artist.split('&')[0]
                temp_artist = temp_artist.strip()
                temp_title = temp_title.split('(')[0].strip()

                # INSERT OR IGNORE INTO Employees(employee_id, first_name, last_name, job_id, hire_date, salary) VALUES (?,?,?,?,?,?)', (emp_id, first_name,last_name,job_id, hire_date,salary))
                cur.execute("INSERT INTO top_song_artists(artist_id, song_name, artist_name) VALUES(?,?,?)",
                            (table_size + 1, temp_title, temp_artist))
            
            
        conn.commit()

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def getSpotifySongData(cur,conn):
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_URL = os.getenv("REDIRECT_URL")
    client_credentials_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    cur.execute("SELECT DISTINCT artist_name FROM top_song_artists") #make sure to change song_id to 
    spotify_artists = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM spotify_artists_table")
    table_size = cur.fetchone()[0]
    if table_size == 200:
        pass
    else:
        if table_size == 0:
            for i in range(0, 25):
                cur.execute("SELECT artist_id FROM top_song_artists WHERE artist_name = ?", (spotify_artists[i][0],))
                shazam_artist_id = cur.fetchone()[0] # id from shazam table for JOIN
                artist_name = spotify_artists[i][0]
                results = spotify.search(q= 'artist:' + artist_name, type='artist')
                artist_id = results['artists']['items'][0]['id'] #spotify artist id from query
                top_tracks = spotify.artist_top_tracks(artist_id)
                top_track_id = top_tracks['tracks'][0]['id']
                artist_popularity = results['artists']['items'][0]['popularity']
                # print(type(str(artist_popularity)))
                artist_followers = results['artists']['items'][0]['followers']['total']
                cur.execute("INSERT INTO spotify_artists_table(id, artist_id, artist_name, artist_popularity, artist_followers, artist_spotify_id, artist_top_track_id) VALUES(?,?,?,?,?,?,?)" , (i+1, int(shazam_artist_id), str(artist_name), artist_popularity, int(artist_followers), str(artist_id), str(top_track_id)))

        else:
            for i in range(0, 25):
                cur.execute("SELECT COUNT(*) FROM spotify_artists_table")
                table_size = cur.fetchone()[0]
                if(table_size == len(spotify_artists)):
                    break
                cur.execute(
                    "SELECT artist_id FROM top_song_artists WHERE artist_name = ?", (spotify_artists[table_size][0],))
                # id from shazam table for JOIN
                shazam_artist_id = cur.fetchone()[0]
                artist_name = spotify_artists[table_size][0]
                results = spotify.search(
                    q='artist:' + artist_name, type='artist')
                # spotify artist id from query
                artist_id = results['artists']['items'][0]['id']
                top_tracks = spotify.artist_top_tracks(artist_id)
                top_track_id = top_tracks['tracks'][0]['id']
                artist_popularity = results['artists']['items'][0]['popularity']
                artist_followers = results['artists']['items'][0]['followers']['total']
                cur.execute("INSERT INTO spotify_artists_table(id, artist_id, artist_name, artist_popularity, artist_followers, artist_spotify_id, artist_top_track_id) VALUES(?,?,?,?,?,?,?)",
                            (table_size + 1, int(shazam_artist_id), str(artist_name), artist_popularity, int(artist_followers), str(artist_id), str(top_track_id)))

    conn.commit()



def getTwitterUserData(cur,conn):
    BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
    auth = tweepy.OAuth2BearerHandler(BEARER_TOKEN)
    api = tweepy.API(auth)
    # cur.execute("SELECT Pokemon.name, Types.type, Pokemon.speed, Pokemon.defense \
    #                 FROM Pokemon JOIN Types ON Pokemon.type_id = Types.id \
    #                     WHERE Pokemon.speed > ? AND Pokemon.defense > ? AND Types.type = ?", (speed, defense, type))   
    cur.execute("SELECT spotify_artists_table.artist_id, top_song_artists.artist_name \
        FROM spotify_artists_table JOIN top_song_artists ON spotify_artists_table.artist_id = top_song_artists.artist_id") # change to id instead of song id
    artist_list = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM twitter_artists_table")
    table_size = cur.fetchone()[0]

    if table_size == 0:
        for i in range(0, 25):
            # id from shazam table for JOIN
            shazam_artist_id = artist_list[i][0]
            artist_name = artist_list[i][1]
            users = api.search_users(artist_name, count = 2)
            if users:
                user = users[0]
                artist_followers = user.followers_count
                twitter_id = user.id
            else: 
                artist_followers = 0
                twitter_id = 0
            # spotify artist id from query
            cur.execute("INSERT INTO twitter_artists_table(artist_id, artist_name, artist_followers, artist_twitter_id) VALUES(?,?,?,?)",
                        (int(shazam_artist_id), str(artist_name), int(artist_followers), twitter_id))

    else:
        for i in range(0, 25):
            cur.execute("SELECT COUNT(*) FROM twitter_artists_table")
            table_size = cur.fetchone()[0]
            if(table_size == len(artist_list)):
                break
            # id from shazam table for JOIN
            shazam_artist_id = artist_list[table_size][0]
            artist_name = artist_list[table_size][1]
            users = api.search_users(artist_name, count = 2)
            if users:
                user = users[0]
                artist_followers = user.followers_count
                twitter_id = user.id
            else: 
                artist_followers = 0
                twitter_id = 0
            cur.execute("INSERT INTO twitter_artists_table(artist_id, artist_name, artist_followers, artist_twitter_id) VALUES(?,?,?,?)",
                        (int(shazam_artist_id), str(artist_name), int(artist_followers), twitter_id))

    conn.commit()
    


        

        



def main():
    cur, conn = open_database('finalProjectDB.db')
    #### YOUR CODE HERE####

    #getSongData(cur, conn)
    # getSpotifySongData(cur,conn)
    for i in range(8):
        getSongData(cur,conn)
    # for i in range(8):
    #     getSpotifySongData(cur,conn)
    # for i in range(8):
    #     getTwitterUserData(cur,conn)
    # Call the functions getSongData(soup) and on your soup object.
    
    conn.close()

    

if __name__ == "__main__":
    main()
