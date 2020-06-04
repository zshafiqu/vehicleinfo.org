# Update Master Data
> This folder contains all the code and entry points needed to update the master data with new information.

## HOW TO UPDATE DATA :
- Start by downloading year, make, and model information from the external source. See https://github.com/abhionlyone/us-car-models-data.

- This download will give you a zipped folder with a bunch of CSV files separated by year. Unzip this folder and put all the CSV files into a folder titled 'external_master'. Make sure the external_master folder is in the same directory as this current one, where the script will be ran.

- Make a copy of the 'master_data' directory into this directory as well. The script will compare the 'master_data' to the 'external_master', and make additions based on that.

- Activate the virtual enviroment contained in the source code, and run update_script.py. The program will prompt you to enter a start year and an end year. This will update all the CSVs within a specific range, and return the updated CSVs. How is this useful? Let's say all CSVs for years 2009 and below haven't had any additions, there's no need to run the script redundantly on those years.

- After the script completes, it will create a new directory called 'new_master_data'

- Within 'new_master_data', there will be another folder called 'data_pulled' with all the data that was just added. All the CSVs will be in here.

- Move the data out of the 'data_pulled' directory into its parent directory, 'new_master_data'

- You can verify that everything that needed to be updated, was updated.

- Then you'll need to move all these new files in the directory called 'master_data'

- Voila, the master data has been updated. Now all you need to is run the script to merge the CSVs in 'master_data' with the database instance.

## SPECIAL NOTES :
- If you're adding a whole new year, such as 2021, you'll need to first create a new 2021.csv file within 'master_data' and make sure it contains all the correct headings. This will allow the script to do a proper 'comparison' and add the new vehicles. Once you create this new folder, you can create a copy of the whole 'master_data' directory and run the script against the 'external_master' source.

## HOW IT WORKS :
- I created a library of files called 'scraping_lib', which contains a bunch of files that do various operations on updating data. We can look at those files one by one.

  1. add_new_models.py:

    - This file's sole job is to compare the local master data against the newly added external source. The external source files are incomplete, and are missing a lot of the data that makes vehicleinfo.org. These files contain the year, make, and model data. We want to be able to merge the newly added makes and models to our existing CSVs, while maintaining order and not losing any data we already have.

    - The script starts by searching for an external source file path, as well as a master data file path. These paths are 'external_master/' and 'master_data/', respectively. It also creates a new folder called 'models_added', which will contain all of our updated CSVs.

    - It opens a file from each of the folders, for example '2020.csv', and converts them to python lists that'll be stored on memory. Let's say these lists are called old_list and new_list. new_list is the one that contains updated information.

    - Starting with two pointers, it runs down each list line by line and checks to see if the 'model' is the same.

    - If the model from the new list is not the same as the model from the old list, then we have a new model to add to the data set. Write this data to a new file, and leave the extra parameters blank (since we don't have trim or image info yet). Move the new pointer up by 1. We don't move the old pointer up because we want to make sure we don't skip any data.

    - If the model is the same, then it's not a new addition to our data set. We don't do anything other than write the row as is, since we've already compiled data. Move both the new and old pointers up by 1. We move both pointers this time because the old data has caught up to the new data.

    - After all rows have been written, return the new CSV file, with blanks for trim/image data where new additions were made.

  2. scraping_utilities.py:
    - This file contains all the helper methods for scraping images and trim data from KBB. The main objective of the methods here are to take in a BeautifulSoup object, and search through it using things like CSS classes and HTML tags. The data is then organized into dictionaries and returned.

  3. generate_header.py:
    - This file contains the get_header method that returns an HTTP header for us to use in our web requests in order to avoid bot detectors.

  4. get_soup.py:
    - This file contains the access method called get_soup_from_url(url) that makes a request to KBB, and returns a BeautifulSoup object that strained for only image and trim data using SoupStrainer.

    - Before, we were scraping for each of these data points separate, which was redundant because we would have to make two separate requests.. Was inefficient and wasted time. We speed up our scraping process by only requesting once but creating two BeautifulSoup objects.

  5. pull_data_for_models.py:
    - Script to scrape the styles and images for newly added vehicles. This would be run following 'add_new_models.py', where new models would be added from the external source. At this point, those new models are missing their 'trim_data' and 'image_sources' columns because they haven't been scraped for. That is where this script comes in.

    - This script starts by converting a given year's CSV file into a list of rows on memory within the program. This list of rows is then passed to a parallel processing module called 'concurrent.futures'. This parallel processing module creates multiple threads, and processes one row at a time.

    - Once all the rows are processed, they are returned in a 'result' list. This result list is passed to a writer function, that sorts the rows in ascending order and writes them to new CSVs. The writer also checks to see if its an old row or new row, and writes an empty string for the 'image_data' column on new rows, because that data is scraped for after this.
