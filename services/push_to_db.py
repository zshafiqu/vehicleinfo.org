import os, mysql.connector, csv
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

# curr.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
#
# curr.execute("SHOW TABLES")
#
# for x in curr:
#   print(x)
year = 1992
filename = 'master_data/'+str(year)+'.csv'

'''
Create a table for cars of a specific year that looks like {
-----------------------------------------------------------------------------------------------------------------
ID (int) | Year (int) | Make (text) | Model (text) | Body-Styles (text) | Trim-Data (JSON)| Images-Sources (JSON)
-----------------------------------------------------------------------------------------------------------------

}
'''

# curr.execute("CREATE TABLE 1992 (id INT AUTO_INCREMENT PRIMARY KEY, year INT, make TEXT, model TEXT, body-styles TEXT, trim-data TEXT, image-sources TEXT)")

# curr.execute("CREATE TABLE '"+dbname+".1992' ( `id` INT NOT NULL AUTO_INCREMENT , `year` INT NOT NULL , `make` TEXT NOT NULL , `model` TEXT NOT NULL , `body-styles` TEXT NOT NULL , `trim-data` JSON NOT NULL , `image-sources` JSON NOT NULL , PRIMARY KEY (`id`))")

# ( `id` INT NOT NULL AUTO_INCREMENT , `year` INT NOT NULL , `make` TEXT NOT NULL , `model` TEXT NOT NULL , `body-styles` TEXT NOT NULL , `trim-data` JSON NOT NULL , `image-sources` JSON NOT NULL , PRIMARY KEY (`id`))

curr.execute("SHOW TABLES")

for x in curr:
  print(x)

# # print('databse connected')
# # if mydb.is_connected():
# #     print('open')
# # else:
# #     print('close')
# mycursor = mydb.cursor()

# print(mycursor.execute('SELECT * FROM `Test_Table`;'))
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
