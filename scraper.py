from bs4 import BeautifulSoup
import requests



def main():
    # Task 1: Create a BeautifulSoup object and name it soup. Refer to discussion slides or lecture slides to complete this

    #### YOUR CODE HERE####
    url = 'https://en.wikipedia.org/wiki/University_of_Michigan'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # Call the functions getLink(soup) and getAdmissionsInfo2019(soup) on your soup object.
    
    endings_list = ['neil-young-powderfinger-1224887/', 'david-bowie-station-to-station-3-1224938/', 'john-prine-angel-from-montgomery-1224988/', 'the-b-52s-rock-lobster-2-1225038/', 'jimi-hendrix-purple-haze-2-1225088/', 'david-bowie-changes-2-1225138/', 'green-day-basket-case-1225188/', 'bob-dylan-blowin-in-the-wind-3-1225238/', 'daddy-yankee-feat-glory-gasolina-1225288/']


    
if __name__ == "__main__":
    main()
