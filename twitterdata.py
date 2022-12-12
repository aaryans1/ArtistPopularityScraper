from dotenv import load_dotenv
load_dotenv()
import os
import sqlite3
import tweepy

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def getTwitterUserData(cur, conn):
    BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
    auth = tweepy.OAuth2BearerHandler(BEARER_TOKEN)
    api = tweepy.API(auth)
    cur.execute("SELECT spotify_artists_table.artist_id, top_song_artists.artist_name \
        FROM spotify_artists_table JOIN top_song_artists ON spotify_artists_table.artist_id = top_song_artists.artist_id")  # change to id instead of song id
    artist_list = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM twitter_artists_table")
    table_size = cur.fetchone()[0]

    if table_size == 0:
        for i in range(0, 25):
            # id from shazam table for JOIN
            shazam_artist_id = artist_list[i][0]
            artist_name = artist_list[i][1]
            users = api.search_users(artist_name, count=2)
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
                print("You can stop running this function now!")
                break
            # id from shazam table for JOIN
            shazam_artist_id = artist_list[table_size][0]
            artist_name = artist_list[table_size][1]
            users = api.search_users(artist_name, count=2)
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

    getTwitterUserData(cur,conn)

    conn.close()


if __name__ == "__main__":
    main()
