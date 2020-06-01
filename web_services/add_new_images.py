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
'''
# ----------------------
from bs4 import BeautifulSoup, SoupStrainer
import requests, json, os, csv, ast, random
from generate_header import get_header
import concurrent.futures
# ----------------------
# This function makes an HTTP request to KBB to gather the page's HTML and convert it to a BeautifulSoup object
def get_soup_from_url(url):
    # Entered get_soup_from_url method, create an iterator to keep track
    # of request attempt count
    ''' print('Preparing to make request for data') '''
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
            ''' print('Request failed on iteration #'+str(iteration)+', trying again!') '''
            iteration += 1
            continue

        # If we've exectued the above successfully, break out of while loop
        break

    ''' print('Request completed!') '''

    # Filter for proprietary classes that contain our data
    # SoupStrainer sets it such that we only parse the response for items with this class tag
    # Helps reduce time spent doing unneccesary work
    only_image_tags = SoupStrainer(class_="css-4g6ai3")
    # BeautifulSoup parses the page as xml for us
    soup = BeautifulSoup(page, 'lxml', parse_only=only_image_tags)

    # Return the filtered soup object
    return soup
# ----------------------
# For each bodystyle, we want to have an image
# We store these as a dictionary where it is { bodystyle : url }
def scrape_KBB_for_images(year, make, model, bodystyles):
    # Scrape KBB for image sources
    map = dict()

    # If there is only one body type, no need to worry about searching for multiple images
    if (len(bodystyles) == 1):
        # Build URL & get soup
        url = 'https://www.kbb.com/'+make+'/'+model+'/'+year+'/'
        soup = get_soup_from_url(url)

        # Attempt to parse for an image item from the soup'd data
        try:
            imgSource = soup.findAll("img", {"class":"css-4g6ai3"})
            map[bodystyles[0]] = imgSource[0]['src']
        # If the soup'd HTML does not contain any image tags with that class, resort to a default img value
        except:
            print("Error on scraping KBB, single body style")
            map[bodystyles[0]] = 'https://www.autotechemporium.com/frontend/assets/images/placeholder/inventory-full-placeholder.png'

    # If there are multiple body styles, we need to get an image for each style
    else:
        index = 0
        for style in bodystyles:
            # Build unique URL for each body style & then get Soup
            url = 'https://www.kbb.com/'+make+'/'+model+'/'+year+'/'+'?bodystyle='+style
            soup = get_soup_from_url(url)

            # Attempt to parse for an image item from the soup'd data
            try:
                imgSource = soup.findAll("img", {"class":"css-4g6ai3"})
                map[style] = imgSource[0]['src']

            # If the soup'd HTML does not contain any image tags with that class, resort to a default img value FOR CURRENT bodystyle
            except:
                print('Error on scraping KBB, multiple body type')
                map[bodystyles[index]] = 'https://www.autotechemporium.com/frontend/assets/images/placeholder/inventory-full-placeholder.png'

            # Increment loop counter
            index += 1

    return map
# ----------------------
data = scrape_KBB_for_images('2020', 'Honda', 'Civic', ['Hatchback'])
print(data)
