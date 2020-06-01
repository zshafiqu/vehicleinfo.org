'''
    May 30, 2020

    PREFACE:
        - Script to scrape the styles for newly added vehicles
        - This would be run following 'add_new_models.py', where new models would be added from the external source
        - At this point, those new models are missing their 'trim_data' and 'image_sources' columns because they haven't
        been scraped for. That is where this script comes in

    GENERAL FLOW:
        - This script starts by converting a given year's CSV file into a list of rows on memory within the program
        - This list of rows is then passed to a parallel processing module called concurrent.futures
        - This parallel processing module creates multiple threads, and processes one row at a time
        - Once all the rows are processed, they are returned in a 'result' list
        - This result list is passed to a writer function, that sorts the rows in ascending order and writes them to new CSVs
        - The writer also checks to see if its an old row or new row, and writes an empty string for the 'image_data' column on new rows, because
        that data is scraped for after this

    HOW IS EACH ROW PROCESSED?
        - For each row, it attempts to exctract row[4], which would be the 'trim_data' column
        - If that extraction is successful, that tells the program that this isn't a new vehicle, so just return that row as is

        - If the extraction fails, great, we know this is a new make and model for us that we need to get data from
        - Then for each vehicle model, we make a request to KBB to get the HTML we need using BeautifulSoup and SoupStrainer
        - Note, some vehicles have multiple body styles, so we query models by each bodystyle to get EVERY trim

        - The HTML is returned, and converted to two lists, the headings which are the trims, and the attributes which are things like MPG, seating, HP, etc
        - These two lists are then passed to another method that matches the trims and attributes together, which are then returned as a dictionary
        - Once we have the dictionary with new data, we create a new row and append this dictionary to that row
        - That row is then considered updated, and passed back to the parallel processing part of the program where its stored
        in a large result list and written to output

    ADDING A NEW YEAR?
        - If adding a whole new year to the data set (a year that doesn't already exist) :
        - Create an empty CSV with that year in the old master directory
        - The script will do its comparison, and none of the lines will be the same, so it'll just merge EVERYTHING into the new one.
        - OR you could just manually add the new year's CSV file to the 'add_new_styles'

    METHOD SIGNATURES:
        - get_soup_from_url(url):
        - convert_soup_to_text_list(soup):
        - mappify_headings_and_attributes_from_list(headings, attributes):
        - parse_soup_to_dictionary(soup):
        - scrape_styles_data(year, make, model, bodystyles):
        - get_source_filepath(year):
        - get_destination_filepath(year):
        - create_updated_csv_directory():
        - row_dispatcher(row):
        - convert_csv_rows_to_list(year):
        - write_output(list, year):
        - dispatcher_for_row_from_list(row):
        - update(year):
'''
# ----------------------
from bs4 import BeautifulSoup, SoupStrainer
import requests, json, os, csv, ast, random
from generate_header import get_header
import concurrent.futures
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
