# ----------------------
import os, mysql.connector, csv, json, ast
from flask import jsonify
# USAGE: to create or update our database with information from any csv file
# ----------------------
# Establish connection to our database using info stored locally on machine
username = os.environ.get('DB_USER')
dbname = os.environ.get('DB_NAME')
passwd = os.environ.get('DB_PASS')
server = os.environ.get('DB_SERVER')
port = os.environ.get('DB_PORT')
# ----------------------
def json_conversion(somestring):
    # Literal
    somestring = ast.literal_eval(somestring)
    # To json
    somestring = json.dumps(somestring)
    # return
    return somestring
# ----------------------
def file_to_database(vehicles_year, database_object):
    # Create a cursor object from the database_object
    curr = database_object.cursor()

    # Create a table name and define the file name & path (route)
    fileroute = file_pathify(vehicles_year)
    tablename = str(vehicles_year)+'_vehicles'

    # Before doing anything, check to see if the table exists & drop it if so
    curr.execute("DROP TABLE IF EXISTS "+tableName)

    # Create the table otherwise, scheme follows:
    # --------------------------------------------------------------------
    # ID | Year | Make | Model | Body-Styles | Trim-Data | Images-Sources
    # --------------------------------------------------------------------
    curr.execute(
        "CREATE TABLE "+tableName+" (id INT AUTO_INCREMENT PRIMARY KEY, year INT, make TEXT, model TEXT, body_styles TEXT, trim_data JSON, image_sources JSON)"
        )

    # Traverse the file to do the operations on it
    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:

            sql = "INSERT INTO "+tableName+" (year, make, model, body_styles, trim_data, image_sources) VALUES (%s, %s, %s, %s, %s, %s)"

            # json_conversion ->
            trim_data = json_conversion(row[4])
            image_sources = json_conversion(row[5])

            # Values list
            list = []
            list.append(str(row[0])) # Year
            list.append(str(row[1])) # Make
            list.append(str(row[2])) # Model
            list.append(str(row[3])) # Body_styles
            list.append(trim_data) # Trim_data
            list.append(image_sources) # Image_sources

            # Execute query
            print(row[0]+' '+row[1]+' '+row[2]+' being inserted.')
            curr.execute(sql, list)

            # Commit change
            database_object.commit()
            print(curr.rowcount, "record inserted.")

    return None
# ----------------------
def connect_to_db(host, port, user, password, database):
    # Establish connection to our database using info stored locally on machine
    db_object = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
        )

    return db_object
# ----------------------
def file_pathify(year):
    # Return file path for given year
    return 'master_data/'+str(year)+'.csv'
# ----------------------
def patch_range(min, max):
    # Connect with global variables
    mydb = connect_to_db(server, port, username, passwd, dbname)
    # Go thru range b/w HI & LOW
    counter = min
    
    while counter <= max:
        name = file_pathify(counter)
        print('BEGINNING FILE: '+name+'\n')
        # Call the function to get the file & upload it to the database
        file_to_database(counter, mydb)
        print('FINISHED FILE: '+name+'\n')

        counter += 1
# ----------------------
