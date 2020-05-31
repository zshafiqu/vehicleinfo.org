'''
    May 30, 2020
    Script to add new models to our master data CSVs

    PREFACE:
    - In our web application, we use an external source to get the makes and models of vehicles manufactured in the US
    - This data source simply contains year, make, model for us to mine information from later
    - We need to be able to seamlessly add new vehicles to our 'master_data' from the external source,
    while maintaining the information we already have. This script helps accomplish that task
    - See source here : https://github.com/abhionlyone/us-car-models-data

    EXAMPLE:
    - Lets say within our master data set, we have all the vehicles produced by Chevrolet in 2020
    - We first mined for data on these vehicles in January 2020
    - At that point, Chevrolet produced 12 vehicle models, so we ran our other scripts on these 12 models
    and gathered information for them (trims, images, etc)

    - Fast forward to June 2020, now additional information has become available and Chevrolet added two models for 2020
    - Now we need to add these two models to our data set, and then run the other scripts later on the new cars we just added
    - Right now, we just want to add these two new models to our master data set. IMPORTANT! We're not doing anything else here.

    NOTE:
    - This script is only intended to merge the newly discovered models into our master data set
    - At the point of running this service, we don't have and trim information, or image sources

    USAGE:
    - Download the new CSVs from the above URL, and place the external source CSVs into their own folder
    - Ensure that you have the 'master_data' available in the same directory

    The script will open the new CSVs, and the master CSVs, and compare each row.
    If a row (defined as year/make/model) exists in the new CSV and not in the master CSV,
    a new row will be created and then added into the master data set. The other colums such as trim_data and image_sources
    will remain empty.. To be filled in a later step

    The result is a new CSV with new models filled in amongst the old models we already have
'''
# ----------------------
import csv
# ----------------------
# Helper to get the external source filename given a year
def get_external_source_filepath(year):
    return 'external_master/'+str(year)+'.csv'
# ----------------------
# Helper to get the master source filename given a year
def get_master_source_filepath(year):
    return 'master_data/'+str(year)+'.csv'
# ----------------------
# Helper to get the target destination filepath, which will be the outer directory for now
def get_new_destination_filepath(year):
    return 'models_added/'+str(year)+'.csv'
# ----------------------
def external_data_to_list(year):
    # Get current filename
    curr_filename = get_external_source_filepath(year)

    # Open file and get a cursor to read the file
    with open(curr_filename) as file:
        next(csv.reader(file)) # Skip the header
        data_list = list(csv.reader(file))

    # Return the new list
    return data_list
# ----------------------
def master_data_to_list(year):
    # Get current filename
    curr_filename = get_master_source_filepath(year)

    # Open file and get a cursor to read the file
    with open(curr_filename) as file:
        next(csv.reader(file)) # Skip the header
        data_list = list(csv.reader(file))

    # Return the new list
    return data_list
# ----------------------
def clear_double_quotes(string):
    return str(string).replace('"',"'")
# ----------------------
def add_external_source_data_to_master_data(year):
    # Get new file path (destination)
    new_path = get_new_destination_filepath(year)

    # Open the new file
    with open(new_path, 'w') as new_file:
        # Create writer object
        writer_object = csv.writer(new_file)

        # Write the headers
        writer_object.writerow(['year', 'make', 'model', 'body_styles', 'trim_data', 'image_sources'])

        # Convert the old and new files to lists
        old_list = master_data_to_list(year)
        new_list = external_data_to_list(year)
        old_counter = 0
        new_counter = 0

        # Go through both new and old files and compare the rows to look for any additions
        while new_counter != len(new_list):

            # Get old row and new row, as well each rows models
            old_row = old_list[old_counter]
            old_model = old_row[2]
            new_row = new_list[new_counter]
            new_model = new_row[2]

            if new_model != old_model:
                # Write the new year, make, model, and bodystyle. We'll get trim_data and image_sources later
                print('Adding a new model to the data set: '+str(new_row))
                writer_object.writerow([new_row[0], new_row[1], new_row[2], clear_double_quotes(new_row[3])])
                new_counter += 1 # Move the new file's cursor until it matches the old file's cursor again

            else:
                # Write the old row's info, its not a new addition and we've already got its info
                writer_object.writerow([old_row[0], old_row[1], old_row[2], old_row[3], old_row[4], old_row[5]])
                new_counter += 1
                old_counter += 1
    return None
# ----------------------
def create_updated_csv_directory():
    import os, pathlib
    curr_path = str(pathlib.Path().absolute())
    new_path = curr_path+'/models_added'
    try:
        os.mkdir(new_path)
    except OSError:
        print('Failed to create directory '+new_path)
# ----------------------
def add_years_in_range(start_year, end_year):
    create_updated_csv_directory()

    while start_year <= end_year:
        add_external_source_data_to_master_data(start_year)
        start_year += 1
    return None
# ----------------------
if __name__ == "__main__":
    add_years_in_range(2020, 2020)
