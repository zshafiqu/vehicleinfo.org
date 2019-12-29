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

# print(username)
# print(dbname)
# print(passwd)
# print(server)
# print(port)
# ----------------------
mydb = mysql.connector.connect(
    host=server,
    port=port,
    user=username,
    password=passwd,
    database=dbname
    )

curr = mydb.cursor()

curr.execute("SELECT * FROM 1992_vehicles WHERE make LIKE 'ACURA' AND model like 'LEGEND'")

for x in curr:
    # x = json.loads(str(x))
    # x = ast.literal_eval(x)
    # x = jsonify(x)
    print(x)

'''
Create a table for cars of a specific year that looks like {
-----------------------------------------------------------------------------------------------------------------
ID (int) | Year (int) | Make (text) | Model (text) | Body-Styles (text) | Trim-Data (JSON)| Images-Sources (JSON)
-----------------------------------------------------------------------------------------------------------------

}
'''
# year = 1992
#
# filename = 'master_data/'+str(year)+'.csv'
# tableName = str(year)+'_vehicles'
#
# curr.execute("DROP TABLE IF EXISTS "+tableName)
#
# curr.execute("CREATE TABLE "+tableName+" (id INT AUTO_INCREMENT PRIMARY KEY, year INT, make TEXT, model TEXT, body_styles TEXT, trim_data JSON, image_sources JSON)")
#
# with open(filename) as file:
#     reader = csv.reader(file)
#     next(reader)
#
#     for row in reader:
#
#         # year = row[0]
#         # make = row[1]
#         # model = row[2]
#         # bodystyles = row[3]
#         # trim_data = row[4]
#         # image_sources = row[5]
#         sql = "INSERT INTO "+tableName+" (year, make, model, body_styles, trim_data, image_sources) VALUES (%s, %s, %s, %s, %s, %s)"
#
#         list = []
#         list.append(str(row[0]))
#         list.append(str(row[1]))
#         list.append(str(row[2]))
#         list.append(str(row[3]))
#
#         # Single quoted ->
#         trim_data = row[4]
#         image_sources = row[5]
#
#         # Literal
#         trim_data = ast.literal_eval(trim_data)
#         image_sources = ast.literal_eval(image_sources)
#
#         # To json
#         trim_data = json.dumps(trim_data)
#         image_sources = json.dumps(image_sources)
#
#         list.append(trim_data)
#         list.append(image_sources)
#         # list[1] = row[1]
#         # list[2] = row[2]
#         # list[3] = row[3]
#         # list[4] = json.loads(row[4])
#         # list[5] = json.loads(row[5])
#
#         curr.execute(sql, list)
#
#         mydb.commit()
#         print(row[0]+' '+row[1]+' '+row[2]+' being inserted.')
#         print(curr.rowcount, "record inserted.")
# ----------------------
# def connect_to_db(host, port, user, password, database):
#     # Establish connection to our database using info stored locally on machine
#     db_object = mysql.connector.connect(
#         host=host,
#         port=port,
#         user=user,
#         password=password,
#         database=database
#         )
#
#     return db_object
# ----------------------
def go_thru_file(filename):
    # Traverse a file
    print(filename)

    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            year = row[0]
            make = row[1]
            model = row[2]
            bodystyles = row[3]
            trim_data = row[4]
            image_sources = row[5]

            # print(year+' '+make+' '+model+' '+bodystyles+' '+trim_data+' '+image_sources+'\n')

    return None
# ----------------------
def file_pathify(year):
    # Return file path for given year
    return 'master_data/'+str(year)+'.csv'
# ----------------------
def print_range(min, max):
    # Print range b/w HI & LOW
    counter = min
    while counter <= max:
        name = file_pathify(counter)
        print('BEGINNING FILE: '+name+'\n')
        go_thru_file(name)
        print('FINISHED FILE: '+name+'\n')

        counter += 1
# ----------------------
# print_range(1992, 1992)
