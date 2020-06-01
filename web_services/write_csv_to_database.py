# ----------------------
import os, csv, json, ast
import mysql.connector
# ----------------------
def get_database_object():
    # Establish connection to our database using info stored locally on machine
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    database = os.environ.get('DB_DBNAME')

    db_object = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
        )

    return db_object
# ----------------------
def get_file_by_year(year):
    # Return file path for given year
    return 'new_master_data/'+str(year)+'.csv'
# ----------------------
def get_table_name(year):
    return str(year)+'_vehicles'
# ----------------------
def convert_string_to_json(string):
    temp = string
    try:
        # Evaluate as a list literal, then evaluate to JSON
        string = ast.literal_eval(string)
        string = json.dumps(string)
    except:
        # If the above fails, return the OG string we stored in 'temp'
        return temp
    # If all works out, return the string converted to JSON
    return string
# ----------------------
def write_csv(year):
    # Create a cursor object from the database_object
    db_object = get_database_object()
    curr = db_object.cursor()

    # Get path for the file we're going to write
    path = get_file_by_year(year)
    table_name = get_table_name(year)

    # Before doing anything, check to se if the table exists and drop it if so
    curr.execute("DROP TABLE IF EXISTS "+table_name)

    # Create the table otherwise, scheme follows:
    # --------------------------------------------------------------------
    # ID | Year | Make | Model | Body-Styles | Trim-Data | Images-Sources
    # --------------------------------------------------------------------

    # Executing this as a raw query
    curr.execute(
        "CREATE TABLE "+table_name+" (id INT AUTO_INCREMENT PRIMARY KEY, year INT, make TEXT, model TEXT, body_styles TEXT, trim_data TEXT, image_sources TEXT)"
        )

    # Open file and traverse it row by row, writing each row to the database
    with open(path) as file:
        reader = csv.reader(file)
        next(reader) # Skip first row
        id = 0 # NOTE - this is not the database ID, this is just to keep track of progress when writing an update

        # For each row in the CSv
        for row in reader:

            # First create a template raw query that we can fill in with the row information later
            sql = "INSERT INTO "+table_name+" (year, make, model, body_styles, trim_data, image_sources) VALUES (%s, %s, %s, %s, %s, %s)"
            #
            # trim_data = json_conversion(row[4])
            # image_sources = json_conversion(row[5])
            # # Values list
            # list = []
            # list.append(str(row[0])) # Year
            # list.append(str(row[1])) # Make
            # list.append(str(row[2])) # Model
            # list.append(str(row[3])) # Body_styles
            # list.append(trim_data) # Trim_data
            # list.append(image_sources) # Image_sources

            ordered_list = [row[0], row[1], row[2], row[3], row[4], row[5]]

            # Execute query
            print('Row ID: '+str(id)+' Vehicle: '+row[0]+' '+row[1]+' '+row[2]+' being inserted.')
            curr.execute(sql, ordered_list) # Execute the query with the %s's being filled in by 'ordered_list'

            # Commit change
            db_object.commit()
            print(curr.rowcount, "record inserted.")
            id += 1
    return None
# ----------------------
if __name__ == "__main__":
    write_csv(2020)
