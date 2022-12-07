from bs4 import BeautifulSoup
import requests



def main():
    # Task 1: Create a BeautifulSoup object and name it soup. Refer to discussion slides or lecture slides to complete this

    #### YOUR CODE HERE####
    url = 'https://en.wikipedia.org/wiki/University_of_Michigan'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # Call the functions getLink(soup) and getAdmissionsInfo2019(soup) on your soup object.
    


if __name__ == "__main__":
    main()
