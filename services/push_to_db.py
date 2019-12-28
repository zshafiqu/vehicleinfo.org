import os, mysql.connector, csv
# USAGE: to create or update our database with information from any csv file
# ----------------------
# Establish connection to our database using info stored locally on machine
username = os.environ.get('DB_USER')
dbname = os.environ.get('DB_NAME')
passwd = os.environ.get('DB_PASS')
server = os.environ.get('DB_SERVER')
port = os.environ.get('DB_PORT')
# ----------------------
# print(username)
# print(dbname)
# print(passwd)
# print(server)
# print(port)

# mydb = mysql.connector.connect(
#     host=server,
#     port=port,
#     user=username,
#     password=passwd,
#     database=dbname
#     )
# # print('databse connected')
# # if mydb.is_connected():
# #     print('open')
# # else:
# #     print('close')
# mycursor = mydb.cursor()

# print(mycursor.execute('SELECT * FROM `Test_Table`;'))
# ----------------------
def go_thru_file(filename):
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

            print(year+' '+make+' '+model+' '+bodystyles+' '+trim_data+' '+image_sources+'\n')

    return None
# ----------------------
def file_pathify(year):
    return 'master_data/'+str(year)+'.csv'
# ----------------------
def print_range(min, max):
    counter = min
    while counter <= max:
        name = file_pathify(counter)
        print('BEGINNING FILE: '+name+'\n')
        go_thru_file(name)
        print('FINISHED FILE: '+name+'\n')

        counter += 1
# ----------------------
print_range(1992, 1992)
