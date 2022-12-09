from bs4 import BeautifulSoup
import requests
import sqlite3
import os

def getSongData(endings_list, cur,conn):
    cur.execute("SELECT COUNT(*) FROM top_song_artists")
    table_size = cur.fetchone()[0]
    baseURL = 'https://www.billboard.com/charts/hot-100/'
    if table_size == 0:
        url = 'https://www.shazam.com/charts/top-200/world'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        song_id = 100
        song_list = soup.find_all(
            'div', class_ = "titleArtistContainer")
        temp1 = song_list[0]
        song_list = temp1.find_all('div')
        for i in range(0, 25):
            temp_title_artist = song_list[i].split(',')
            temp_title = temp_title_artist[1]
            temp_artist = temp_title_artist[0]
            print(temp_title_artist)
            # INSERT OR IGNORE INTO Employees(employee_id, first_name, last_name, job_id, hire_date, salary) VALUES (?,?,?,?,?,?)', (emp_id, first_name,last_name,job_id, hire_date,salary))
            cur.execute("INSERT OR IGNORE INTO top_song_artist(song_id, song_name, artist_name, page_num) VALUES(?,?,?,?)", (song_id, temp_title, temp_artist, 0))
    else:
        cur.execute(
                "SELECT page_num FROM top_song_artists WHERE song_id = (SELECT MIN(song_id) FROM top_song_artists)")
        if table_size % 2 != 0:
            page_num = cur.fetchone()[0]
            url = baseURL + endings_list[page_num]
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            song_list = soup.find_all(
                'div', class_="c-gallery-vertical-album__title")

            for i in range(25, len(song_list)):
                temp_title_artist = song_list[i].split(',')
                temp_title = temp_title_artist[1]
                temp_artist = temp_title_artist[0]

                print(temp_title_artist)
            
        else:
            page_num = cur.fetchone()[0] + 1
            url = baseURL + endings_list[page_num]
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            song_list = soup.find_all(
                'div', class_="c-gallery-vertical-album__title")
                
            for i in range(0, 25 ):
                    temp_title_artist = song_list[i].split(',')
                    temp_title = temp_title_artist[1]
                    temp_artist = temp_title_artist[0]
            
        
    
    
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
    endings_list = ['neil-young-powderfinger-1224887/', 
    'david-bowie-station-to-station-3-1224938/', 
    'john-prine-angel-from-montgomery-1224988/', 
    'the-b-52s-rock-lobster-2-1225038/', 
    'jimi-hendrix-purple-haze-2-1225088/', 
    'david-bowie-changes-2-1225138/', 
    'green-day-basket-case-1225188/', 
    'bob-dylan-blowin-in-the-wind-3-1225238/', 
    'daddy-yankee-feat-glory-gasolina-1225288/']

    getSongData(endings_list, cur, conn)
   
    # Call the functions getSongData(soup) and on your soup object.
    
    

    

if __name__ == "__main__":
    main()
