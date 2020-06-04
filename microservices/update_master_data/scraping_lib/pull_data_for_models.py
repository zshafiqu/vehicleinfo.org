'''
    June 3, 2020

    PREFACE:
        - Script to scrape the styles and images for newly added vehicles
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
        - For each row, it attempts to exctract row[4] and row[5], which would be the 'trim_data' & 'image_data' olumn
        - If that extraction is successful, that tells the program that this isn't a new vehicle, so just return that row as is

        - If the extraction fails, great, we know this is a new make and model for us that we need to get data from
        - Then for each vehicle model, we make a request to KBB to get the HTML we need using BeautifulSoup and SoupStrainer
        - Note, some vehicles have multiple body styles, so we query models by each bodystyle to get EVERY trim

        - The HTML is returned as a BeautifulSoup object that has been strained only for images and style data. This data is parsed into
        a dictionary and returned here. (See scraping_utilities.py for details)
        - The dictionary is then sliced for the image and trim info, which is then formed into a row object
        - The row object gets passed back to be written to the CSV

    METHOD SIGNATURES:
        - get_source_filepath(year)
        - get_destination_filepath(year)
        - create_data_pulled_csv_directory()
        - convert_csv_rows_to_list(year)
        - write_output(list, year)
        - handle_empty_row(row)
        - row_dispatcher(row)
        - extract_data_from_soup_dict(soup_dictionary)
        - scrape_KBB_for_styles_and_images(year, make, model, bodystyles)
        - entry_point_for_pull_data_by_year(year)
'''
# ----------------------
import os, csv, ast, pathlib
from .get_soup import get_soup_from_url
from .scraping_utilities import parse_soup_to_styles_dictionary, parse_soup_for_img_src
import concurrent.futures
# ----------------------
# Gets filepath for source CSVs
def get_source_filepath(year):
    return 'models_added/'+str(year)+'.csv'
# ----------------------
# Gets filepath for destination output CSVs
def get_destination_filepath(year):
    return 'data_pulled/'+str(year)+'.csv'
# ----------------------
# Creates directory for new output files
def create_data_pulled_csv_directory():
    curr_path = str(pathlib.Path().absolute())
    new_path = curr_path+'/data_pulled'
    try:
        os.mkdir(new_path)
    except OSError:
        print('Failed to create directory '+new_path)
# ----------------------
# Start by converting the given CSV to a list that we can store on memory
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
# Once all the parallel tasks are completed and we have a 'result' list, write that list to CSV
def write_output(list, year):
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
def handle_empty_row(row):
        year = row[0]
        # Convert the make to a string list, we use this to handle the case where make is two words
        make_as_list = list(row[1].split(" "))
        model = row[2]
        # Convert our bodystyles item from a string literal list to an actual list so we can access length
        bodystyles_as_list = ast.literal_eval(row[3])

        if len(make_as_list) == 2:
            # Convert back to string with a dash in between the words
            make_as_string = make_as_list[0]+'-'+make_as_list[1]
            data = scrape_KBB_for_styles_and_images(year, make_as_string, model, bodystyles_as_list)

        # If make is of size 1, something like 'Ford' || 'Honda'
        else:
            data = scrape_KBB_for_styles_and_images(year, make_as_list[0], model, bodystyles_as_list)

        # Return results
        return data # data is a dictionary with both style and img information
# ----------------------
def row_dispatcher(row):
        # Dispatcher for multithreaded implementation
        # Handles one row at a time
        # After adding styles, a row[5] technically exists
        # So instead of using a try/except block, we need to check that row[5] isnt empty

        if row[4] != '' and row[5] != '':
            new_row = row
        else:
            # print('In new data!')
            # If row[4] and row[5] is blank, that means no style and information
            # print('No style and image information for:'+str(row))
            data = handle_empty_row(row)

            # Create a temporary row with the newly scraped image data
            trim_data = data['Styles']
            image_data = data['Images']

            temp = [row[0], row[1], row[2], row[3], trim_data, image_data]
            print(temp)
            new_row = temp

        return new_row
# ----------------------
# Soup operations, this takes a dictionary with soup values, and attempts to extract style and img information from it
def extract_data_from_soup_dict(soup_dictionary):
    # First pass it to the styles utility, will get us a JSON dictionary of the styles
    styles_soup = soup_dictionary['Trims']
    styles_dictionary = parse_soup_to_styles_dictionary(styles_soup)

    image_soup = soup_dictionary['Images']
    image_url = parse_soup_for_img_src(image_soup)

    results = dict()
    results['style_result'] = styles_dictionary
    results['img_result'] = image_url

    return results
# ----------------------
def scrape_KBB_for_styles_and_images(year, make, model, bodystyles):
    # Cleanse model input
    model = model.replace('&', '')
    model = model.replace('/', '')
    # Since we'll be parsing two pieces of info with one request, we use this as the result dictionary
    styles_and_images = dict()
    styles = dict()
    images = dict()
    default_url = 'https://www.autotechemporium.com/frontend/assets/images/placeholder/inventory-full-placeholder.png'

    # If len(bodystyles) is 1, only need to make one request
    if len(bodystyles) == 1:
        # Sometimes KBB will detect the bot and refuse to respond with the requested webpage, which causes us to default to uknown image
        # To make the script a little better, we'll try 3 time to – request for webpage and parse responses
        # If after three times it doesn't work, then just return blank values
        url = 'https://www.kbb.com/'+make+'/'+model+'/'+year+'/'
        # print(url)
        count = 0

        while True:

            if count == 3:
                styles[bodystyles[0]] = dict()
                images[bodystyles[0]] = default_url
                break

            try:
                soup_dictionary = get_soup_from_url(url)
                items = extract_data_from_soup_dict(soup_dictionary)

                # Assign results
                styles[bodystyles[0]] = items['style_result']
                images[bodystyles[0]] = items['img_result']

            except Exception as e:
                print('\n')
                print('Error when requesting and parsing response from KBB, trying again!')
                print(url)
                print(e)
                print('\n')
                count += 1
                continue

            # If we've executed the above successfully, break out of while loop
            break

    # In all other instances where there is more than 1 bodystyle, make requests for each one
    else:
        index = 0

        for style in bodystyles:
            url = 'https://www.kbb.com/'+make+'/'+model+'/'+year+'/'+'?bodystyle='+style
            count = 0
            # print(url)

            while True:

                if count == 3:
                    styles[bodystyles[index]] = dict()
                    images[bodystyles[index]] = default_url
                    break

                try:
                    soup_dictionary = get_soup_from_url(url)
                    items = extract_data_from_soup_dict(soup_dictionary)

                    # Assign results
                    styles[bodystyles[index]] = items['style_result']
                    images[bodystyles[index]] = items['img_result']

                except Exception as e:
                    print('Error when requesting and parsing response from KBB, trying again!')
                    print(url)
                    print(e)
                    count += 1
                    continue

                # If we've executed the above successfully, break out of while loop
                break

            # Use the bodystyle as the key for the trims dictionary
            # styles[bodystyles[index]] = items['style_result']
            # images[bodystyles[index]] = items['img_result']
            index += 1

    styles_and_images['Styles'] = styles
    styles_and_images['Images'] = images

    # Return a dictionary that contains both style and image data for this make and model
    return styles_and_images
# ----------------------
def entry_point_for_pull_data_by_year(year):
    # Grabs the given year's rows from its respective CSV file, and converts it to a list
    rows = convert_csv_rows_to_list(year)
    # Get a results list going for us to add to as our threads complete
    results = []

    # Use thread pool to execute multiple requests concurrently, also max_workers can be set depending on system env
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        # For each row in rows, pass it as its own single thread to the dispatcher_for_row_from_list() method
        # Begin load operations, each dict entry looks like {<Future at 'address' state=pending>: row}
        row_futures = { executor.submit(row_dispatcher, row): row for row in rows }

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
