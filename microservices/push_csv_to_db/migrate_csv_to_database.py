# ----------------------
import os, csv, json, ast
import mysql.connector
# ----------------------
def get_database_object():
    # Establish connection to our database using info stored locally on machine
    host = os.environ.get('RDS_HOST')
    port = os.environ.get('RDS_PORT')
    user = os.environ.get('RDS_USER')
    password = os.environ.get('RDS_PASSWORD')
    database = os.environ.get('RDS_DBNAME')

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
    return 'master_data/'+str(year)+'.csv'
# ----------------------
def get_table_name(year):
    return str(year)+'_vehicles'
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
    # NOTE - storing the body_styles, trim_data, and image_sources as plain text because we can cast it to JSON later within our server
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
def write_csv_in_range():
    start_year = int(input("Enter the start year you'd like to write to the database: "))
    end_year = int(input("Enter the end year you'd like to to write to the database: "))

    # Needed since no guarantee the table exists
    host = os.environ.get('RDS_HOST')
    port = os.environ.get('RDS_PORT')
    user = os.environ.get('RDS_USER')
    password = os.environ.get('RDS_PASSWORD')

    # Connect to DB without specifying a database
    db_object = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        )

    # Use this local object to create the database
    initial_sql = "CREATE DATABASE IF NOT EXISTS `vehicleinfo-db`" 
    curr = db_object.cursor() # Get the cursor 
    curr.execute(initial_sql)  # Execute the initial DB creation 

    while start_year <= end_year:
        print('*******************************************************')
        print('Currently working on '+str(start_year))

        write_csv(start_year)

        print('Finished '+str(start_year))
        start_year += 1
# ----------------------
if __name__ == "__main__":
    write_csv_in_range()
# ----------------------
