'''
    May 30, 2020
    Script to scrape the styles for newly added vehicles
    This would be run following 'add_new_models.py'
'''
# ----------------------
from bs4 import BeautifulSoup, SoupStrainer
import requests, json, os, csv, ast, random
import generate_header
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
            headers = generate_header.get_header()
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
def scrape_styles_data(year, make, model, bodystyles):
    # Cleanse model input
    model = model.replace('&', '')
    model = model.replace('/', '')
    trims = dict()

    # If there is only one body style, so the url is unique
    if len(bodystyles) == 1:

        url = 'https://www.kbb.com/'+make+'/'+model+'/'+year+'/'
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
def get_source_filepath(year):
    return 'models_added/'+str(year)+'.csv'
# ----------------------
def get_destination_filepath(year):
    return 'styles_added/'+str(year)+'.csv'
# ----------------------
def create_updated_csv_directory():
    import os, pathlib
    curr_path = str(pathlib.Path().absolute())
    new_path = curr_path+'/styles_added'
    try:
        os.mkdir(new_path)
    except OSError:
        print('Failed to create directory '+new_path)
# ----------------------
# def add_styles_for_new_vehicles(year):
#     # Get source path to read from, and destination path to write to
#     source_path = get_source_filepath(year)
#     # destination_path = get_destination_filepath(year)
#
#     #Open source file to find the vehicles that have blanks for trim_data
#     with open(source_path) as source:
#         # Get reader object, skip first row as its the header
#         reader = csv.reader(source)
#         next(reader)
#
#         for row in reader:
#             try:
#                 temp = row[4]
#             except:
#                 print(row)
#             # if row[3] is None:
#             #     print(row)
#             # print(row[3])
# ----------------------
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
def add_styles_for_new_vehicles(year):
    # Get source path to read from, and destination path to write to
    source_path = get_source_filepath(year)
    destination_path = get_destination_filepath(year)

    #Open source file to find the vehicles that have blanks for trim_data
    with open(source_path) as source:
        # Get reader object, skip first row as its the header
        reader = csv.reader(source)
        next(reader)

        with open(destination_path, 'w') as destination:
            # Create writer object
            writer = csv.writer(destination)
            # Write the headers on the first row of new file
            writer.writerow(['year', 'make', 'model', 'body_styles', 'trim_data', 'image_sources'])

            # Traverse rows in source file
            for row in reader:
                # See if there's anything in the styles column
                try:
                    temp = row[4] # If this executes successfully, just write the row as is
                    # Write – year , make , model, body_styles, trim_data,  image_sources
                    writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5]])
                except:
                    # If this fails, we just got a hit. So pass this to the soup function(s)
                    print('No style information for:'+str(row))
                    data = row_dispatcher(row)
                    # Write – year , make , model, body_styles, trim_data,  image_sources
                    writer.writerow([row[0], row[1], row[2], row[3], data])
                    print('Finished row operations for:'+str(row))
# ----------------------
create_updated_csv_directory()
add_styles_for_new_vehicles(2020)
