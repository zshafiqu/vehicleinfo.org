# ----------------------
from bs4 import BeautifulSoup, SoupStrainer
import requests, json, os, csv, ast, random
from generate_header import get_header
# ----------------------
# This function makes an HTTP request to KBB to gather the page's HTML
def get_soup_from_url(url):
    # Entered get_soup_from_url method, create an iterator to keep track
    # of request attempt count
    print('Preparing to make request for data')
    iteration = 0

    # Contintually attempt this request until it's successful
    while True:

        # Unless we've attemped this request 15 times, at which point
        # break and stop wasting the time
        if iteration == 15:
            page = '' # Empty page
            break

        try:
            # Generate a new header, required to emulate browser
            headers = get_header()
            # print(headers)
            # Make request, timeout after 20 seconds for hanging requests
            page = requests.get(url, headers=headers, timeout=20).text

        except:
            # If the request fails, log it to stdout, then try again
            print('Request failed on iteration #'+str(iteration)+', trying again!')
            iteration += 1
            continue

        # If we've exectued the above successfully, break out of while loop
        break

    print('Request completed!')

    # Filter for proprietary classes that contain our data
    only_boxes = SoupStrainer("div", class_="css-130z0y1-StyledBox-default emf8dez0")
    soup = BeautifulSoup(page, 'lxml', parse_only=only_boxes)

    # Return the filtered soup object
    return soup
# ----------------------
def parse_soup_to_dictionary(soup):
    '''
        NOTE:
        - Every vehicle follows the same pattern with up to 4 attributes per
        trim; { Fuel Economy, Seating, Horsepower, Engine Size }

        - To parse through the soup object properly, we need to consider the following;
            1. The length of the headings will tell us how many trims there are ( len(headings) = 3)
            2. The length of the attributes is a function of ( 8 * len(headings) )
            3. Attributes are split by a key, value mapping
            4. Thus, len(attributes) = 24

        - The implementation of parsing would be O( m*n ) for each trims
        - You create a dictionary until you've reached counter = ( heading_number * 8 )

        - See pseudocode below;
            for heading in headings:
                for attribute in attributes:
                    go until you've finished this trim's attributes

            dictionary : {
                trim : { attributes },
                trim : { attributes },
                etc.
            }
    '''
    headings = soup.findAll("h3")
    attributes = soup.findAll("p")
    outer_map = dict()

    i = 0
    j = 0

    while i < len(headings):
        z = 0
        inner_map = dict()

        while j < len(attributes):
            if z > 7:
                break
            else:
                inner_map[str(attributes[j].text)] = str(attributes[j+1].text)

            j += 2
            z += 2

        outer_map[str(headings[i].text)] = inner_map
        i += 1

    return outer_map
# ----------------------
# print()
year = '2020'
make = 'Audi'
model = 'TT'
url = 'https://www.kbb.com/'+make+'/'+model+'/'+year+'/'

soup = get_soup_from_url(url)
# soup = list(soup)
headings = soup.findAll('h3')
attributes = soup.findAll('p')

a = []
b = []

for heading in headings:
    temp = heading.text
    a.append(temp)

for attribute in attributes:
    temp = attribute.text
    b.append(temp)


print(a)

print('\n')

print(b)

# print(soup[1])
# dictionary = parse_soup_to_dictionary(soup)

# print(dictionary)
