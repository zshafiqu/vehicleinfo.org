from flask import Flask, render_template, jsonify
from flaskext.mysql import MySQL
import requests, json, os, ast
'''
Server Requirements:
    - flask
    - requests
    - flask-mysql
'''
# ----------------------
# Initialize flask app
app = Flask(__name__)
# ----------------------
# Get info stored locally on machine
host_name= os.environ.get('DB_SERVER')
port = os.environ.get('DB_PORT')
username = os.environ.get('DB_USER')
passwd = os.environ.get('DB_PASS')
dbname = os.environ.get('DB_NAME')
# ----------------------
# Configure flask app with db connection
app.config['MYSQL_DATABASE_HOST'] = host_name
app.config['MYSQL_DATABASE_PORT'] = int(port)
app.config['MYSQL_DATABASE_USER'] = username
app.config['MYSQL_DATABASE_PASSWORD'] = passwd
app.config['MYSQL_DATABASE_DB'] = dbname
# ----------------------
# Bind app to db obj
mysql = MySQL()
mysql.init_app(app)
# cursor = mysql.get_db().cursor()
# ----------------------

# Make an API call to the NHTSA page for recall Information
# def get_recalls(year, make, model):
#     # Build URL for call to JSON response
#     url = 'https://one.nhtsa.gov/webapi/api/Recalls/vehicle/modelyear/'+year+'/make/'+make+'/model/'+model+'?format=json'
#     # Make request
#     items = requests.get(url).json()
#
#     return items
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
def mappify_row(row):
    # Parse row object as dictionary with key : value mapping
    map = dict()
    map['Year'] = row[1]
    map['Make'] = row[2]
    map['Model'] = row[3]
    map['Styles'] = ast.literal_eval(row[4])
    map['Trims'] = ast.literal_eval(row[5])
    map['Images'] = ast.literal_eval(row[6])

    # Return a dictionary for a result object
    return map
''' ------------- ALL API ROUTES LIVE BELOW THIS LINE ------------- '''
# Route 1, get all vehicles for a given year
@app.route('/api/<year>/', methods=['GET'])
def get_by_year(year):
    # Define table name for lookup
    tableName = str(year)+'_vehicles'
    # Prepare query
    query = "SELECT * FROM "+tableName
    # Get cursor & execute query
    cursor = mysql.get_db().cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    # Parse results
    list = []
    for result in results:
        map = mappify_row(result)
        list.append(map)

    return jsonify(list)
# ----------------------
# Route 2, get all vehicles for a given year and make
@app.route('/api/<year>/<make>/', methods=['GET'])
def get_by_year_and_make(year, make):
    # Define table name for lookup
    tableName = str(year)+'_vehicles'
    # Prepare query
    query = "SELECT * FROM "+tableName+" WHERE make LIKE '"+make+"'"
    print(query)
    # Get cursor & execute query
    cursor = mysql.get_db().cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    # Parse results
    # headers = ['year', 'make', 'model', 'styles', 'trims', 'images']
    list = []
    # print(results.count())
    for result in results:
        map = mappify_row(result)
        list.append(map)
        # list.append(ast.literal_eval(result))

    return jsonify(list)
# ----------------------
# Route 3, get all vehicles for a given year and make
@app.route('/api/<year>/<make>/<model>/', methods=['GET'])
def get_by_year_make_and_model(year, make, model):
    # Define table name for lookup
    tableName = str(year)+'_vehicles'
    # Prepare query
    query = "SELECT * FROM "+tableName+" WHERE make LIKE '"+make+"'"+" AND model LIKE '"+model+"'"
    print(query)
    # Get cursor & execute query
    cursor = mysql.get_db().cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    print(results)
    # Parse results
    list = []
    for result in results:
        map = mappify_row(result)
        list.append(map)

    return jsonify(list)
# ----------------------
if __name__ == '__main__':
    app.run(debug=True)
