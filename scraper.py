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


                # INSERT OR IGNORE INTO Employees(employee_id, first_name, last_name, job_id, hire_date, salary) VALUES (?,?,?,?,?,?)', (emp_id, first_name,last_name,job_id, hire_date,salary))
                cur.execute("INSERT INTO top_song_artists(song_id, song_name, artist_name) VALUES(?,?,?)", (i, temp_title, temp_artist))
            
        else:
            for i in range(0, 25):
                cur.execute("SELECT COUNT(*) FROM top_song_artists")
                table_size = cur.fetchone()[0]
                temp_title = song_list[table_size].text
                temp_artist = artist_list[table_size].text
                temp_artist = temp_artist.split(',')[0]
                temp_artist = temp_artist.split('&')[0]

                # INSERT OR IGNORE INTO Employees(employee_id, first_name, last_name, job_id, hire_date, salary) VALUES (?,?,?,?,?,?)', (emp_id, first_name,last_name,job_id, hire_date,salary))
                cur.execute("INSERT INTO top_song_artists(song_id, song_name, artist_name) VALUES(?,?,?)",
                            (table_size + 1, temp_title, temp_artist))
            
            
        conn.commit()

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def getSpotifySongData(cur,conn):
    spotify = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials())

    cur.execute("SELECT DISTINCT artist_name FROM top_song_artists")
    spotify_artists = cur.fetchall()



    for artist in spotify_artists:

        results = spotify.search(q='artist:' + artist[0], type='artist')
        print(results)
        spotify_id = ['items'][0]['id']
        followers = ['items'][0]['followers']
        popularity = ['items'][0]['popularity']

def main():
    cur, conn = open_database('finalProjectDB.db')
    #### YOUR CODE HERE####

    getSongData(cur, conn)
    getSpotifySongData(cur,conn)
   
    # Call the functions getSongData(soup) and on your soup object.
    
    conn.close()

    

if __name__ == "__main__":
    main()
