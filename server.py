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
# ----------------------
def get_recalls_from_NHTSA(year, make, model):
    # Build URL for call to NHTSA API and typecast incase year input is int
    year = str(year) # typecast incase input is int
    url = 'https://one.nhtsa.gov/webapi/api/Recalls/vehicle/modelyear/'+year+'/make/'+make+'/model/'+model+'?format=json'
    # Make request
    items = requests.get(url).json()
    return items
# ----------------------
def get_complaints_from_NHTSA(year, make, model):
    # Build URL for call to NHTSA API and typecast incase year input is int
    year = str(year)
    url = 'https://one.nhtsa.gov/webapi/api/Complaints/vehicle/modelyear/'+year+'/make/'+make+'/model/'+model+'?format=json'
    # Make request
    items = requests.get(url).json()
    return items
# ----------------------
@app.route('/')
def index():
    # Can use methods without decorator like below
    # res = get_by_year_make_and_model(2002, 'toyota', 'corolla')
    # return res
    return render_template('home.html')
    # res=get_complaints_NHTSA('1999', 'honda', 'civic')
    # return res
# ----------------------
''' ------------- HELPER FUNCTIONS FOR API ROUTES BELOW THIS LINE ------------- '''
def mappify_row(row):
    # Parse row object to return a dictionary with {key : value} mapping
    map = dict()
    map['Year'] = row[1]
    map['Make'] = row[2]
    map['Model'] = row[3]
    map['Styles'] = ast.literal_eval(row[4])
    map['Trims'] = ast.literal_eval(row[5])
    map['Images'] = ast.literal_eval(row[6])

    # Return a dictionary for a result object
    return map
# ----------------------
def parse_results(results):
    # Parse results
    list = []
    for result in results:
        map = mappify_row(result)
        list.append(map)
    return list
# ----------------------
def compile_response(list):
    response = dict()
    response['Count'] = len(list)
    response['Message'] = 'Results returned successfully'
    response['Results'] = list
    return response
# ----------------------
def default_response():
    response = dict()
    response['Count'] = 0
    response['Message'] = 'No results found for this request'
    response['Results'] = []
    return response
# ----------------------
''' ------------- ALL API ROUTES LIVE BELOW THIS LINE ------------- '''
# Route 1, get all vehicles for a given year
@app.route('/api/<year>/', methods=['GET'])
def get_by_year(year):
    # Define table name for lookup and prepare query
    tableName = str(year)+'_vehicles'
    query = "SELECT * FROM "+tableName

    # Get cursor & execute query
    cursor = mysql.get_db().cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    # Check for validity
    if len(results) == 0:
        return jsonify(response=default_response())

    # Verified, now parse all rows in results to a list
    # And aggregate data in map for count, response, results
    list = parse_results(results)
    response = compile_response(list)

    # Return JSON object
    return jsonify(response)
# ----------------------
# Route 2, get all vehicles for a given year and make
@app.route('/api/<year>/<make>/', methods=['GET'])
def get_by_year_and_make(year, make):
    # Define table name for lookup and prepare query
    tableName = str(year)+'_vehicles'
    query = "SELECT * FROM "+tableName+" WHERE make LIKE '"+make+"'"

    # Get cursor & execute query
    cursor = mysql.get_db().cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    # Check for validity
    if len(results) == 0:
        return jsonify(response=default_response())

    # Verified, now parse all rows in results to a list
    # And aggregate data in map for count, response, results
    list = parse_results(results)
    response = compile_response(list)

    # Return JSON object
    return jsonify(response)
# ----------------------
# Route 3, get all vehicles for a given year and make
@app.route('/api/<year>/<make>/<model>/', methods=['GET'])
def get_by_year_make_and_model(year, make, model):
    # Define table name for lookup and prepare query
    tableName = str(year)+'_vehicles'
    query = "SELECT * FROM "+tableName+" WHERE make LIKE '"+make+"'"+" AND model LIKE '"+model+"'"

    # Get cursor & execute query
    cursor = mysql.get_db().cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    # Check for validity
    if len(results) == 0:
        return jsonify(response=default_response())

    # Verified, now parse all rows in results to a list
    # And aggregate data in map for count, response, results
    list = parse_results(results)
    response = compile_response(list)

    # Return JSON object
    return jsonify(response)
# ----------------------
if __name__ == '__main__':
    app.run(debug=True)
