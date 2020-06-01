'''
    May 30, 2020
    Script to scrape the styles for newly added vehicles
    This would be run following 'add_new_models.py'
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
    only_boxes = SoupStrainer("div", class_="css-130z0y1-StyledBox-default emf8dez0")
    soup = BeautifulSoup(page, 'lxml', parse_only=only_boxes)

    # Return the filtered soup object
    return soup
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
def parse_soup_to_dictionary(soup):
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
# Entry point for YEAR / MAKE / MODEL / BODYSTYLES
def scrape_styles_data(year, make, model, bodystyles):
    # Cleanse model input
    model = model.replace('&', '')
    model = model.replace('/', '')
    trims = dict()

    # If there is only one body style, so the url is unique
    if len(bodystyles) == 1:

        url = 'https://www.kbb.com/'+make+'/'+model+'/'+year+'/'
        # print(url)
        soup = get_soup_from_url(url)

        try:
            result = parse_soup_to_dictionary(soup)
        except:
            print("Error on parsing soup to map / single bodystyle / inside of scrape trim data")
            result = dict()

        trims[bodystyles[0]] = result

    # In all other instances where there is more than 1 bodystyle, make requests for each one
    else:
        index = 0
        for style in bodystyles:
            url = 'https://www.kbb.com/'+make+'/'+model+'/'+year+'/'+'?bodystyle='+style
            soup = get_soup_from_url(url)

            try:
                result = parse_soup_to_dictionary(soup)

            except:
                print("Error on parsing soup to map / multiple bodystyle / inside of scrape trim data")
                result = dict()

            # Use the bodystyle as the key for the trims dictionary
            trims[bodystyles[index]] = result
            index += 1

    # Return trims dictionary with data
    return trims
# ----------------------
# Gets filepath for source CSVs
def get_source_filepath(year):
    return 'models_added/'+str(year)+'.csv'
# ----------------------
# Gets filepath for destination output CSVs
def get_destination_filepath(year):
    return 'styles_added/'+str(year)+'.csv'
# ----------------------
# Creates directory for new output files
def create_updated_csv_directory():
    import os, pathlib
    curr_path = str(pathlib.Path().absolute())
    new_path = curr_path+'/styles_added'
    try:
        os.mkdir(new_path)
    except OSError:
        print('Failed to create directory '+new_path)
# ----------------------
# Row Dispatcher for each row in CSV
def row_dispatcher(row):
    year = row[0]
    model = row[2]
    # Convert the make to a string list, we use this to handle the case where make is two words
    make_as_list = list(row[1].split(" "))

    # Convert our bodystyles item from a string literal list to an actual list so we can access length
    bodystyles_as_list = ast.literal_eval(row[3])

    if len(make_as_list) == 2:
        # Convert back to string with a dash in between the words
        make_as_string = make_as_list[0]+'-'+make_as_list[1]
        styles_data = scrape_styles_data(year, make_as_string, model, bodystyles_as_list)

    # If make is of size 1, something like 'Ford' || 'Honda'
    else:
        styles_data = scrape_styles_data(year, make_as_list[0], model, bodystyles_as_list)

    # Return results
    return styles_data
# ----------------------
# # Opens source CSVs, parses them, makes call to get new data, then writes the new data
# def add_styles_for_new_vehicles(year):
#     # Get source path to read from, and destination path to write to
#     source_path = get_source_filepath(year)
#     destination_path = get_destination_filepath(year)
#     list = []
#
#     #Open source file to find the vehicles that have blanks for trim_data
#     with open(source_path) as source:
#         # Get reader object, skip first row as its the header
#         reader = csv.reader(source)
#         next(reader)
#
#         with open(destination_path, 'w') as destination:
#             # Create writer object
#             writer = csv.writer(destination)
#             # Write the headers on the first row of new file
#             writer.writerow(['year', 'make', 'model', 'body_styles', 'trim_data', 'image_sources'])
#
#             # Traverse rows in source file
#             for row in reader:
#                 # See if there's anything in the styles column
#                 try:
#                     temp = row[4] # If this executes successfully, just write the row as is
#                     # Write – year , make , model, body_styles, trim_data,  image_sources
#                     writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5]])
#                     list.append(row)
#                 except:
#                     # If this fails, we just got a hit. So pass this to the soup function(s)
#                     # print('No style information for:'+str(row))
#                     data = row_dispatcher(row)
#                     print(data)
#                     # Write – year , make , model, body_styles, trim_data,  image_sources
#                     writer.writerow([row[0], row[1], row[2], row[3], data])
#                     # print('Finished row operations for:'+str(row))
#                     list.append(row)
#
#     print(list)
# ----------------------
# ----------------------
def csv_rows_to_list(year):
    # Get source path to read from, and destination path to write to
    source_path = get_source_filepath(year)
    list = []

    #Open source file to find the vehicles that have blanks for trim_data
    with open(source_path) as source:
        # Get reader object, skip first row as its the header
        reader = csv.reader(source)
        next(reader)

        # Traverse rows in source file
        for row in reader:
            list.append(row)

    return list
# ----------------------
def write_output(list, year):
    # Get source path to read from, and destination path to write to
    destination_path = get_destination_filepath(year)
    list.sort()
    with open(destination_path, 'w') as destination:
        # Create writer object
        writer = csv.writer(destination)
        # Write the headers on the first row of new file
        writer.writerow(['year', 'make', 'model', 'body_styles', 'trim_data', 'image_sources'])

        # Traverse rows in source file
        for row in list:
            # print(row)
            try:
                writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5]])
            except:
                writer.writerow([row[0], row[1], row[2], row[3], row[4], ''])
# ----------------------
# Opens source CSVs, parses them, makes call to get new data, then writes the new data
def dispatcher_for_row_from_list(row):
    # Get source path to read from, and destination path to write to
    # results = []
    try:
        temp = row[4] # If this executes successfully, just write the row as is
        # Write – year , make , model, body_styles, trim_data,  image_sources
        # writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5]])
        # temp = [row[0], row[1], row[2], row[3], row[4], row[5]]
        # results.append(row)
        new_row = row
    except:
        # If this fails, we just got a hit. So pass this to the soup function(s)
        ''' print('No style information for:'+str(row)) '''
        data = row_dispatcher(row)
        # print(data)
        # print(data)
        # Write – year , make , model, body_styles, trim_data,  image_sources
        temp = [row[0], row[1], row[2], row[3], data]
        print(temp)
        ''' print('Finished row operations for:'+str(row)) '''
        new_row = temp
        # results.append(temp)
    return new_row
# ----------------------
def update(year):
    create_updated_csv_directory()
    rows = csv_rows_to_list(year)
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
        stuff = { executor.submit(dispatcher_for_row_from_list, row): row for row in rows }

        for thread_result in concurrent.futures.as_completed(stuff):
            try:
                data = thread_result.result()
                results.append(data)
            except Exception as e:
                continue


    write_output(results, year)
    return None
# ----------------------
# create_updated_csv_directory()
# add_styles_for_new_vehicles(2020)
# print(csv_rows_to_list(2020))
# def do_work(year):
#     rows = csv_rows_to_list(year)
# data = csv_rows_to_list(2020)
# write_output(data, 2020)
update(2020)

# ----------------------
''' NOTE : BELOW IS THE OLD METHOD FOR PARSING SOUP TO A DICTIONARY '''
# def parse_soup_to_dictionary(soup):
#     '''
#         - Every vehicle follows the same pattern with up to 4 attributes per
#         trim; { Fuel Economy, Seating, Horsepower, Engine Size }
#
#         - To parse through the soup object properly, we need to consider the following;
#             1. The length of the headings will tell us how many trims there are ( len(headings) = 3)
#             2. The length of the attributes is a function of ( 8 * len(headings) )
#             3. Attributes are split by a key, value mapping
#             4. Thus, len(attributes) = 24
#
#         - The implementation of parsing would be O( m*n ) for each trims
#         - You create a dictionary until you've reached counter = ( heading_number * 8 )
#
#         - See pseudocode below;
#             for heading in headings:
#                 for attribute in attributes:
#                     go until you've finished this trim's attributes
#
#             dictionary : {
#                 trim : { attributes },
#                 trim : { attributes },
#                 etc.
#             }
#     '''
#     headings = soup.findAll("h3")
#     attributes = soup.findAll("p")
#     outer_map = dict()
#
#     i = 0
#     j = 0
#
#     while i < len(headings):
#         z = 0
#         inner_map = dict()
#
#         while j < len(attributes):
#             if z > 7:
#                 break
#             else:
#                 inner_map[str(attributes[j].text)] = str(attributes[j+1].text)
#
#             j += 2
#             z += 2
#
#         outer_map[str(headings[i].text)] = inner_map
#         i += 1
#
#     return outer_map
# # ----------------------
