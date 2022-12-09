from bs4 import BeautifulSoup
import requests
import sqlite3
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

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
    
    
        # url = baseURL + endings_list[i]
    #class c-gallery-vertical-album__title
        # song_list = soup.find_all('div', class_="c-gallery-vertical-album__title")
        # cur.execute("SELECT Employees.first_name, Employees.last_name \
        #         FROM Employees JOIN Jobs ON Employees.job_id = jobs.job_id WHERE Employees.salary > jobs.max_salary OR Employees.salary < jobs.min_salary")
       
        # if table_size % 2 != 0:
        #     index = 25
        # else:
        #     index = 0

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def main():
    cur, conn = open_database('finalProjectDB.db')
    #### YOUR CODE HERE####

    getSongData(cur, conn)
   
    # Call the functions getSongData(soup) and on your soup object.
    
    conn.close()

    

if __name__ == "__main__":
    main()
