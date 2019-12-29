from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import requests, json, os, mysql.connector
# ----------------------
# Initialize flask app
app = Flask(__name__)
# ----------------------
# Get info stored locally on machine
username = os.environ.get('DB_USER')
dbname = os.environ.get('DB_NAME')
passwd = os.environ.get('DB_PASS')
host = os.environ.get('DB_SERVER')
port = os.environ.get('DB_PORT')
# ----------------------
# Configure flask app with db connection
# app.config['MYSQL_HOST'] = host
# app.config['MYSQL_PORT'] = port
# app.config['MYSQL_USER'] = username
# app.config['MYSQL_PASSWORD'] = passwd
# app.config['MYSQL_DB'] = dbname

# Establish connection to our database using info stored locally on machine
# db_object = mysql.connector.connect(
#     host=host,
#     port=port,
#     user=username,
#     password=passwd,
#     database=dbname
#     )
# ----------------------
# Bind app to db obj
# mysql = MySQL()
# mysql.init_app(app)
# ----------------------

# Make an API call to the NHTSA page for recall Information
def getRecalls(year, make, model):
    # Build URL for call to JSON response
    url = 'https://one.nhtsa.gov/webapi/api/Recalls/vehicle/modelyear/'+year+'/make/'+make+'/model/'+model+'?format=json'
    # Make request
    items = requests.get(url).json()

    return items
# ----------------------
# @app.route('/handleRequest', methods=['POST'])
# def process():
#     query = request.form['searchparameter']
#     parameter = query.split()
#     year = parameter[0]
#     make = parameter[1]
#     model = parameter[2]
#
#     recalls = getRecalls(year, make, model)
#     # imagesrc = scrapeEdmunds(year, make, model)
#
#     # return render_template('dashboard.html', recalls=recalls)
#     return recalls
# ----------------------
@app.route('/')
def index():
    return render_template('home.html')
# ----------------------
# @app.route('/jsonTest')
# def random():
#     recalls = getRecalls('2007', 'lexus', 'es')
#     return recalls
# ----------------------
@app.route('/api')
def random():
    # recalls = getRecalls('2003', 'chevrolet', 'corvette')
    cur = db_object.cursor()
    cur.execute("SELECT * FROM 1992_vehicles WHERE make LIKE 'ACURA'")
    list = []
    for row in cur:
        list.append(row)
    return list
# ----------------------
if __name__ == '__main__':
    app.run(debug=True)
