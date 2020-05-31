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
'''
# ----------------------
import csv
# ----------------------
# Helper to get the external source filename given a year
def get_external_source_name(year):
    return 'external_master'+str(year)+'.csv'
# ----------------------
# Prints external source files within a year range
def read_external_sources(start_year, end_year):

    # Go through full range
    while start_year <= end_year:
        # Get current file name
        curr_filename = get_external_source_name(start_year)

        # Open file and get a cursor to read the file
        with open(curr_filename) as file:
            reader = csv.reader(file)
            # Move one row to avoid headers
            next(reader)

            for row in reader:
                print(row)
    return None
# ----------------------
