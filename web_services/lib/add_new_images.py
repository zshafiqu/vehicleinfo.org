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
# This function makes an HTTP request to KBB to gather the page's HTML and convert it to a BeautifulSoup object
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
    # SoupStrainer sets it such that we only parse the response for items with this class tag
    # Helps reduce time spent doing unneccesary work
    only_image_tags = SoupStrainer(class_="css-4g6ai3")

    # BeautifulSoup parses the page as xml for us
    soup = BeautifulSoup(page, 'lxml', parse_only=only_image_tags)

    # Return the filtered soup object
    return soup
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
        image_data = scrape_KBB_for_images(year, make_as_string, model, bodystyles_as_list)

    # If make is of size 1, something like 'Ford' || 'Honda'
    else:
        image_data = scrape_KBB_for_images(year, make_as_list[0], model, bodystyles_as_list)

    # Return results
    return image_data
# ----------------------
# Gets filepath for source CSVs
def get_source_filepath(year):
    return 'styles_added/'+str(year)+'.csv'
# ----------------------
# Gets filepath for destination output CSVs
def get_destination_filepath(year):
    return 'images_added/'+str(year)+'.csv'
# ----------------------
# Creates directory for new output files
def create_images_csv_directory():
    import os, pathlib
    curr_path = str(pathlib.Path().absolute())
    new_path = curr_path+'/images_added'
    try:
        os.mkdir(new_path)
    except OSError:
        print('Failed to create directory '+new_path)
# ----------------------
def convert_csv_rows_to_list(year):
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
# This dispatcher function accepts one row at a time.
def dispatcher_for_row_from_list(row):
    # Dispatcher for multithreaded implementation
    # Handles one row at a time
    # After adding styles, a row[5] technically exists
    # So instead of using a try/except block, we need to check that row[5] isnt empty

    if row[5] != '':
        new_row = row
    else:
        # If row[5] is blank, that means no image information
        # print('No image information for:'+str(row))
        image_data = row_dispatcher(row)
        # print(image_data)
        # Create a temporary row with the newly scraped image data
        temp = [row[0], row[1], row[2], row[3], row[4], image_data]
        print(temp)
        # print('Finished row operations for:'+str(row))
        new_row = temp

    return new_row
# ----------------------
def write_output(list, year):
    # print('In write output')
    # Get source path to read from, and destination path to write to
    destination_path = get_destination_filepath(year)
    # Must sort list of output data, otherwise it'll write out of order
    list.sort()

    # Create a file descriptor to open the destination path file
    with open(destination_path, 'w') as destination:
        # Create writer object
        writer = csv.writer(destination)
        # Write the headers on the first row of new file
        writer.writerow(['year', 'make', 'model', 'body_styles', 'trim_data', 'image_sources'])

        # Traverse rows in result list
        for row in list:
            # We should have everything by now, so write row[] index 0-5
            writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5]])
# ----------------------
# Main entry point for given year
def add_images(year):
    # Grabs the given year's rows from its respective CSV file, and converts it to a list
    rows = convert_csv_rows_to_list(year)
    # Get a results list going for us to add to as our threads complete
    results = []

    # Use thread pool to execute multiple requests concurrently, also max_workers can be set depending on system env
    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
        # For each row in rows, pass it as its own single thread to the dispatcher_for_row_from_list() method
        # Begin load operations, each dict entry looks like {<Future at 'address' state=pending>: row}
        row_futures = { executor.submit(dispatcher_for_row_from_list, row): row for row in rows }

        for thread_result in concurrent.futures.as_completed(row_futures):
            # Extract updated row from thread_result
            try:
                data = thread_result.result()
                results.append(data) # Add this updated row to our results list here
            except Exception as e:
                continue

    # Once this whole multithreaded operation completes, we pass our LARGE resulting list to our write_output function
    write_output(results, year)
    return None
# ----------------------
if __name__ == '__main__':
    # print("you're in add_new_styles.py")
    # create_images_csv_directory()
    # add_images(2020)
