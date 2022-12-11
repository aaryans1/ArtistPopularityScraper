import requests
import json
import sqlite3
import os
import matplotlib
import matplotlib.pyplot as plt

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_visual_one(cur, conn):
    


    cur.execute("SELECT artist_popularity FROM spotify_artists_table")
    x_axis = []


    def main():
        cur, conn = open_database('finalProjectDB.db')
        create_visual_one(cur, conn)


    #### FEEL FREE TO USE THIS SPACE TO TEST OUT YOUR FUNCTIONS

    conn.close()


if __name__ == "__main__":
    main()
   # unittest.main(verbosity = 2)