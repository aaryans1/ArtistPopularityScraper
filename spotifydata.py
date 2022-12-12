import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
load_dotenv()
import os
import sqlite3

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def getSpotifySongData(cur, conn,spotify):

    # make sure to change song_id to
    cur.execute("SELECT DISTINCT artist_name FROM top_song_artists")
    spotify_artists = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM spotify_artists_table")
    table_size = cur.fetchone()[0]
    if table_size == 200:
        pass
    else:
        if table_size == 0:
            for i in range(0, 25):
                cur.execute(
                    "SELECT artist_id FROM top_song_artists WHERE artist_name = ?", (spotify_artists[i][0],))
                # id from shazam table for JOIN
                shazam_artist_id = cur.fetchone()[0]
                artist_name = spotify_artists[i][0]
                results = spotify.search(
                    q='artist:' + artist_name, type='artist')
                # spotify artist id from query
                artist_id = results['artists']['items'][0]['id']
                top_tracks = spotify.artist_top_tracks(artist_id)
                top_track_id = top_tracks['tracks'][0]['id']
                artist_popularity = results['artists']['items'][0]['popularity']
                # print(type(str(artist_popularity)))
                artist_followers = results['artists']['items'][0]['followers']['total']
                cur.execute("INSERT INTO spotify_artists_table(id, artist_id, artist_name, artist_popularity, artist_followers, artist_spotify_id, artist_top_track_id) VALUES(?,?,?,?,?,?,?)",
                            (i+1, int(shazam_artist_id), str(artist_name), artist_popularity, int(artist_followers), str(artist_id), str(top_track_id)))

        else:
            for i in range(0, 25):
                cur.execute("SELECT COUNT(*) FROM spotify_artists_table")
                table_size = cur.fetchone()[0]
                if(table_size == len(spotify_artists)):
                    print("You can stop running this function now!")
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


def main():
    cur, conn = open_database('finalProjectDB.db')
    #### YOUR CODE HERE####
    CLIENT_ID = 'f23a7b980c684642b807c7be4fc4d799'
    # CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    CLIENT_SECRET = 'a9aac79406ef4ab69f0ae4c0944d470a'

    # REDIRECT_URL = os.getenv("REDIRECT_URL")
    client_credentials_manager = SpotifyClientCredentials(
        CLIENT_ID, CLIENT_SECRET)
    spotify = spotipy.Spotify(
        client_credentials_manager=client_credentials_manager)

    getSpotifySongData(cur,conn,spotify)


    conn.close()


if __name__ == "__main__":
    main()
