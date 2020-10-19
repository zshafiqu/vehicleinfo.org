'''
    June 3, 2020

    PREFACE:
        - This file contains all the helper methods for scraping images and trim data from KBB.
        - The main objective of the methods here are to take in a BeautifulSoup object, and search
        through it using things like CSS classes and HTML tags.
        - The data is then organized into dictionaries and returned

    METHOD SIGNATURES:
        - convert_soup_to_text_list(soup)
        - mappify_headings_and_attributes_from_list(headings, attributes)
        - parse_soup_to_styles_dictionary(soup)
        - parse_soup_for_img_src(soup)
'''
# ----------------------
from bs4 import BeautifulSoup, SoupStrainer
# ----------------------
# This function takes a soup object, and converts it into a list based on all the inner texts from the HTML
def convert_soup_to_text_list(soup):
    items = []
    for item in soup:
        temp = item.text
        items.append(temp)
    return items
# ----------------------
# This method takes in a list of headings and attributes, and parses them into a dictionary where attributes are split by trim
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

    See pseudocode below;
        for heading in headings:
            for attribute in attributes:
                go until you've finished this trim's attributes

        dictionary : {
            trim : { attributes },
            trim : { attributes },
            etc.
        }
    '''

    # Use 'i' to traverse the list of headings, remember KBB added this 'Dealer Home Service' box, so be sure to skip that
    i = 1 # 'Dealer Home Service' will always be first, so just set that to 1 so we skip it
    j = 0 # Use 'j' as a loop control variable for the attributes list
    outer_map = dict() # This will be the wrapping dictionary for our JSON object

    # For each trim
    while i < len(headings):

        topmost_attribute = attributes[0] # We need to know when we've finished a trim, so we use the topmost attribute as an indicator of when we've completed one trim
        inner_map = dict() # Each trim gets its own dictionary with its attributes
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
                inner_map[attributes[j]] = attributes[j+1]
                 # Jump by two because we've mapped the last two values as key,value
                j += 2

        # Once the attributes have been assigned as we've broke out of the inner loop, map the trim to it's dictionary of attributes
        outer_map[headings[i]] = inner_map
        # Go to the next heading (trim)
        i += 1

    # By now, all attributes and trims should be parsed as the dictionary 'trims'
    return outer_map
# ----------------------
# Dispatcher method that takes in some soup and converts it into a dictionary
def parse_soup_to_styles_dictionary(soup):
    # Grab all the headings and attributes that we need
    headings = soup.findAll('h3')
    attributes = soup.findAll('p')

    # Convert the headings and attributes to a list
    headings_list = convert_soup_to_text_list(headings)
    attributes_list = convert_soup_to_text_list(attributes)

    # Pass to mappify function that'll handle conversion to JSON dictionary
    dictionary = mappify_headings_and_attributes_from_list(headings_list, attributes_list)

    # Return the JSON ready dict
    return dictionary
# ----------------------
# Parses an image soup object for a URL
def parse_soup_for_img_src(soup):
    image_source = soup.findAll("img", {"class":"css-n0lk2j-StyledImage e99w8gw0"})
    return image_source[0]['src']
# ----------------------
