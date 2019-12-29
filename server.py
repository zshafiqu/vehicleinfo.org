from flask import Flask, render_template, jsonify
from flaskext.mysql import MySQL
import requests, json, os
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
# Route 1, get all vehicles for a given year
@app.route('/api/<int:year>', methods=['GET'])
def get_all_for_year(year):
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
        list.append(str(result))

    return jsonify(list)
# ----------------------
@app.route('/api')
def random():
    # recalls = getRecalls('2003', 'chevrolet', 'corvette')
    # cur = db_object.cursor()

    # cursor = mysql.get_db().cursor()
    # cursor.execute("SELECT * FROM 1992_vehicles")
    # results = cursor.fetchall()
    # # print(results)
    # list = []
    # for result in results:
    #     # print(result)
    #     list.append(str(result))
    #
    # return jsonify(list)
    return ''
    # return 'Done'

    # cur.execute("SELECT * FROM 1992_vehicles WHERE make LIKE 'ACURA'")
    # list = []
    # for row in cur:
    #     list.append(row)
    # return list

    # recalls = get_recalls('2003', 'chevrolet', 'corvette')
    # return recalls
# ----------------------
if __name__ == '__main__':
    app.run(debug=True)
