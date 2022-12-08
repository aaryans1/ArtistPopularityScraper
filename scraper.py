from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
load_dotenv()

def getSongData(endings_list):
    baseURL = 'https://www.rollingstone.com/music/music-lists/best-songs-of-all-time-1224767/'
    for i in range(len(endings_list)): 
        url = baseURL + endings_list[i]
    #class c-gallery-vertical-album__title
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        listing_list = soup.find_all('div', class_="c-gallery-vertical-album__title")


def main():

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

    getSongData(endings_list)
   
    # Call the functions getSongData(soup) and on your soup object.
    
    

    

if __name__ == "__main__":
    main()
