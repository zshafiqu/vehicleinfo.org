'''
    June 1, 2020

    I realized that doing an 'add_new_styles' and then 'add_new_images' sequentially
    would mean that we're making two separate HTTP requests for the same information.

    So instead, we'll isolate the get_soup_from_url into its own file that returns
    multiple soup objects in a single request

'''
# ----------------------
from bs4 import BeautifulSoup, SoupStrainer
import requests, json, os, csv, ast, random
from .generate_header import get_header
# ----------------------
# This function makes an HTTP request to KBB to gather the page's HTML and convert it to a BeautifulSoup object
def get_soup_from_url(url):
    # Entered get_soup_from_url method, create an iterator to keep track
    # of request attempt count
    print('Preparing to make request for data')
    iteration = 0
    soup_dictionary = dict()

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
    # SoupStrainer sets it such that we only parse the response for items with this class tag
    # Helps reduce time spent doing unneccesary work
    # BeautifulSoup parses the page as xml for us
    only_image_tags = SoupStrainer(class_="css-4g6ai3")
    image_soup = BeautifulSoup(page, 'lxml', parse_only=only_image_tags)
    soup_dictionary['Images'] = image_soup

    # Filter for proprietary classes that contain our data
    only_boxes = SoupStrainer("div", class_="css-130z0y1-StyledBox-default emf8dez0")
    trims_soup = BeautifulSoup(page, 'lxml', parse_only=only_boxes)
    soup_dictionary['Trims'] = trims_soup

    # Return the filtered soup object dictionary
    return soup_dictionary
# ----------------------
