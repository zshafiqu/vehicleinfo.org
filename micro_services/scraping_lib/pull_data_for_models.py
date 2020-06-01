# ----------------------
import requests, json, os, csv, ast, random
from get_soup import get_soup_from_url
from scraping_utilities import parse_soup_to_styles_dictionary, parse_soup_for_img_src
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
    import os, pathlib
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
            # If row[4] and row[5] is blank, that means no style and information
            # print('No style and image information for:'+str(row))
            data = handle_empty_row(row)

            # Create a temporary row with the newly scraped image data
            trim_data = data['Trims']
            image_data = data['Images']
            temp = [row[0], row[1], row[2], row[3], trim_data, image_data]
            print(temp)
            new_row = temp

        return new_row
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
        url = 'https://www.kbb.com/'+make+'/'+model+'/'+year+'/'

        # Get dictionary of soup
        soup_dictionary = get_soup_from_url(url)

        try:
            # First pass it to the styles utility, will get us a JSON dictionary of the styles
            styles_soup = soup_dictionary['Trims']
            styles_dictionary = parse_soup_to_styles_dictionary(styles_soup)

            # Next, pass to image utility
            image_soup = soup_dictionary['Images']
            image_url = parse_soup_for_img_src(image_soup)


        except:
            print("Error on parsing soup to map / single bodystyle / inside of scrape trim data")
            # Assign blank dictionaries if it fails
            styles_dictionary = dict()
            image_url = default_url

        styles[bodystyles[0]] = styles_dictionary
        images[bodystyles[0]] = image_url

    # In all other instances where there is more than 1 bodystyle, make requests for each one
    else:
        index = 0
        for style in bodystyles:
            url = 'https://www.kbb.com/'+make+'/'+model+'/'+year+'/'+'?bodystyle='+style
            # Get dictionary of soup
            soup_dictionary = get_soup_from_url(url)

            try:
                # First pass it to the styles utility, will get us a JSON dictionary of the styles
                styles_soup = soup_dictionary['Trims']
                styles_dictionary = parse_soup_to_styles_dictionary(styles_soup)

                # Next, pass to image utility
                image_soup = soup_dictionary['Images']
                image_url = parse_soup_for_img_src(image_soup)

            except:
                print("Error on parsing soup to map / multiple bodystyle / inside of scrape trim data")
                # Assign blank dictionaries if it fails
                styles_dictionary = dict()
                image_url = default_url

            # Use the bodystyle as the key for the trims dictionary
            styles[bodystyles[index]] = styles_dictionary
            images[bodystyles[index]] = image_url
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
    with concurrent.futures.ThreadPoolExecutor(max_workers=128) as executor:
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

# year = '2020'
# make = 'Honda'
# model = 'Civic'
# bodystyles = ['Hatchback', 'Sedan']
# bodystyle = ['Hatchback']
#
# print(scrape_KBB_for_styles_and_images(year, make, model, bodystyles)['Images'])
