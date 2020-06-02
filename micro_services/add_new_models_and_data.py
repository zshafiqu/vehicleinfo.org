# ----------------------
import scraping_lib.add_new_models as ANM
import scraping_lib.pull_data_for_models as PDFM
import os, pathlib, shutil
# ----------------------
'''
    PREFACE:
        - In our web application, we use an external source to get the makes and models of vehicles manufactured in the US
        - This data source simply contains year, make, model for us to mine information from later
        - We need to be able to seamlessly add new vehicles to our 'master_data' from the external source,
        while maintaining the information we already have. This script is the entry point to accomplish that task
        - See source here : https://github.com/abhionlyone/us-car-models-data

    USAGE:
        - To do this properly, download the updated CSVs from the above link and put them in a folder called 'external_master'
        - After that, run this script, and it'll prompt you for the range you'd like to update
        - Specify your range, and the script will go through a set of sequential steps to update everything
        - All the updated files will be in a new folder called 'new_master_data'

    ADDING A NEW YEAR?
        - If adding a whole new year to the data set (a year that doesn't already exist) :
        - Create an empty CSV with that year in the old master directory
        - The script will do its comparison, and none of the lines will be the same, so it'll just merge EVERYTHING into the new one.
        - OR you could just manually add the new year's CSV file to the 'add_new_styles'
'''
# ----------------------
# Creates directory for new output files
def create_new_master_data_directory():
    curr_path = str(pathlib.Path().absolute())
    new_path = curr_path+'/new_master_data'
    try:
        os.mkdir(new_path)
    except OSError:
        print('Failed to create directory '+new_path)
# ----------------------
def move_to_new_master_data():
    curr_path = str(pathlib.Path().absolute())
    new_path = curr_path+'/new_master_data'
    old_path = curr_path+'/data_pulled'
    try:
        shutil.move(old_path, new_path)
    except OSError:
        print('Failed to copy directory from '+old_path+' to '+new_path)
# ----------------------
def remove_old_directories():
    curr_path = str(pathlib.Path().absolute())

    # Remove models_added, styles_added, and images_added ONLY after you've moved to new master
    models_path = curr_path+'/models_added'

    shutil.rmtree(models_path, ignore_errors=True)
    # shutil.rmtree(styles_path, ignore_errors=True)
    # shutil.rmtree(images_path, ignore_errors=True)

    return None
# ----------------------
def run_merge():
    start_year = int(input("Enter the start year you'd like to update: "))
    end_year = int(input("Enter the end year you'd like to update: "))

    # Create all needed directorys
    # create_new_master_data_directory()
    # Create the models added directory
    ANM.create_updated_csv_directory()
    # Create the data pulled directory
    PDFM.create_data_pulled_csv_directory()



    while start_year <= end_year:
        print('*******************************************************')
        print('Currently working on '+str(start_year))

        if start_year == 2021:
                PDFM.entry_point_for_pull_data_by_year(start_year)
        else:
            # Add the new models from external source to 'models_added'
            ANM.add_models(start_year)
            PDFM.entry_point_for_pull_data_by_year(start_year)

        print('Finished '+str(start_year))
        start_year += 1

    create_new_master_data_directory()
    move_to_new_master_data()
    remove_old_directories()
# ----------------------
if __name__ == '__main__':
    run_merge()

    # if move_to_new_master_data():
    #     remove_old_directories()
# ----------------------
