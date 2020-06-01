# ----------------------
import requests, json, os, csv, ast, random
from get_soup import get_soup_from_url
from style_utilities import parse_soup_to_styles_dictionary
from image_utilities import parse_soup_for_img_src
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
def scrape_KBB_for_styles_and_images(year, make, model, bodystyles):
    # Cleanse model input
    model = model.replace('&', '')
    model = model.replace('/', '')
    # Since we'll be parsing two pieces of info with one request, we use this as the result dictionary
    styles_and_images = dict()
    styles = dict()
    images = dict()
    default_url = 'https://www.autotechemporium.com/frontend/assets/images/placeholder/inventory-full-placeholder.png'

    # ---------------------------------------------------------------------------------------------
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

    # ---------------------------------------------------------------------------------------------
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
    # ---------------------------------------------------------------------------------------------
    styles_and_images['Styles'] = styles
    styles_and_images['Images'] = images

    # Return a dictionary that contains both style and image data for this make and model
    return styles_and_images
# ----------------------
year = '2020'
make = 'Honda'
model = 'Civic'
bodystyles = ['Hatchback', 'Sedan']
bodystyle = ['Hatchback']

print(scrape_KBB_for_styles_and_images(year, make, model, bodystyles)['Images'])
