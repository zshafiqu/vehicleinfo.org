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

mydb = mysql.connector.connect(
    host=server,
    port=port,
    user=username,
    password=passwd,
    database=dbname
    )
# print('databse connected')
if mydb.is_connected():
    print('open')
else:
    print('close')
# ----------------------
