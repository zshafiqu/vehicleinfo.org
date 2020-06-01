'''
    May 31, 2020

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

    METHOD SIGNATURES:
        - get_soup_from_url(url):
        - parse_soup_for_img_src(soup):
        - scrape_KBB_for_images(year, make, model, bodystyles):
        - row_dispatcher(row):
        - get_source_filepath(year):
        - get_destination_filepath(year):
        - create_images_csv_directory():
        - convert_csv_rows_to_list(year):
        - dispatcher_for_row_from_list(row):
        - write_output(list, year):
        - add_images(year):
'''
# ----------------------
from bs4 import BeautifulSoup, SoupStrainer
import requests, json, os, csv, ast, random
from generate_header import get_header
import concurrent.futures
# ----------------------
def parse_soup_for_img_src(soup):
    image_source = soup.findAll("img", {"class":"css-4g6ai3"})
    return image_source[0]['src']
# ----------------------
# Scrape KBB for image sources given a YEAR / MAKE / MODEL / BODYSTYLES
def scrape_KBB_for_images(year, make, model, bodystyles):
    # We want an image for each bodystyle, and store them as a dictionary where it is { bodystyle : url }
    map = dict()
    # In the event we can't get an image url, we need something to default to
    default_url = 'https://www.autotechemporium.com/frontend/assets/images/placeholder/inventory-full-placeholder.png'

    # If there is only one body type, no need to worry about searching for multiple images
    if (len(bodystyles) == 1):
        try:
            # Build URL & get soup
            # Attempt to parse for an image item from the soup'd data
            url = 'https://www.kbb.com/'+make+'/'+model+'/'+year+'/'
            soup = get_soup_from_url(url)
            map[bodystyles[0]] = parse_soup_for_img_src(soup)

        except:
            # If the soup'd HTML does not contain any image tags with that class, resort to a default img value
            # print("Error on scraping KBB, single body style")
            map[bodystyles[0]] = default_url

    # If there are multiple body styles, we need to get an image for each style
    else:
        # Need to keep track of an index so we know where to place a default
        index = 0
        for style in bodystyles:
            try:
                # Build unique URL for each body style & then get Soup
                # Attempt to parse for an image item from the soup'd data
                url = 'https://www.kbb.com/'+make+'/'+model+'/'+year+'/'+'?bodystyle='+style
                soup = get_soup_from_url(url)
                map[style] = parse_soup_for_img_src(soup)

            except:
                # If the soup'd HTML does not contain any image tags with that class, resort to a default img value FOR CURRENT bodystyle
                # print('Error on scraping KBB, multiple body type')
                map[bodystyles[index]] = default_url

            # Increment loop counter
            index += 1

    return map
# ----------------------
