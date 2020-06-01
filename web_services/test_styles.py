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
def extract_soup_text_to_list(soup):
    items = []

    for item in soup:
        temp = item.text
        items.append(temp)

    return items
# ----------------------
def mappify_headings_and_attributes_from_list(headings, attributes):
    # We have a list of headings (the trims)
    # and list of attributes (all attributes for all trims, we need to slice this properly)
    '''
    An example of headings:
        ['Dealer Home Service', 'Base Style', 'TTS', 'RS']
        len() = 4

    An example of attributes:
        ['Combined Fuel Economy', '26 MPG', 'Seating', 'Seats 4', 'Horsepower', '228 @ 4500 RPM HP', 'Engine', '4-Cyl, Turbo, 2.0 Liter', 'Combined Fuel Economy', '25 MPG', 'Seating', 'Seats 4', 'Horsepower', '288 @ 5400 RPM HP', 'Engine', '4-Cyl, Turbo, 2.0 Liter', 'Combined Fuel Economy', '23 MPG', 'Seating', 'Seats 4', 'Horsepower', '394 hp HP', 'Engine', '5-Cyl, Turbo, 2.5 Liter']
        len() = 24
    '''

    # Use 'i' to traverse the list of headings, remember KBB added this 'Dealer Home Service' box, so be sure to skip that
    i = 1 # 'Dealer Home Service' will always be first, so just set that to 1 so we skip it
    j = 0 # Use 'j' as a loop control variable for the attributes list
    trims = dict() # This will be the wrapping dictionary for our JSON object

    # For each trim
    while i < len(headings):

        curr_trim = headings[i] # Current trim
        topmost_attribute = attributes[0] # We need to know when we've finished a trim, so we use the topmost attribute as an indicator of when we've completed one trim
        attributes_for_curr_trim = dict() # Each trim gets its own dictionary with its attributes
        new_trim_flag = True

        # Go through the list of attributes until the second to last value
        while j < len(attributes)-1:
            # Check if the current attribute is the topmost attribute, because that would indicate we just finished a trim and are on the next set of attributes
            if attributes[j] == topmost_attribute and new_trim_flag == False:
                # Set thew new_trim_flag to True indicating that we're ready to work on a new trim
                new_trim_flag = True
                break
            else:
                # Set the new_trim_flag to false cause we're currently workign on a trim
                new_trim_flag = False
                # Key, value mapping ... 'Combined Fuel Economy' : '26 MPG'
                attributes_for_curr_trim[str(attributes[j])] = str(attributes[j+1])
                 # Jump by two because we've mapped the last two values as key,value
                j += 2

        # Once the attributes have been assigned as we've broke out of the inner loop, map the trim to it's dictionary of attributes
        trims[str(curr_trim)] = attributes_for_curr_trim
        # Go to the next heading (trim)
        i += 1

    # By now, all attributes and trims should be parsed as the dictionary 'trims'
    return trims
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

a = extract_soup_text_to_list(headings)
b = extract_soup_text_to_list(attributes)

print(len(a))
print(a)

print('\n')

print(len(b))
print(b)


print('\n')

print(mappify_headings_and_attributes_from_list(a, b))
# ----------------------



# print(soup[1])
# dictionary = parse_soup_to_dictionary(soup)

# print(dictionary)
