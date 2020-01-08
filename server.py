from flask import Flask, render_template, jsonify, make_response, request
# from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy
import requests, json, os, ast, datetime
# ----------------------
# Initialize flask app, enable auto deploy from master branch for heroku
app = Flask(__name__)
app.secret_key = os.environ.get('KEY')
# ----------------------
# Configure flask app with info stored locally within environment (locally or heroku)
# To install mysqlclient, needed to run brew install mysql
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('BASE_URI')
# app.config['MYSQL_DATABASE_HOST'] = os.environ.get('DB_HOST')
# app.config['MYSQL_DATABASE_PORT'] = int(os.environ.get('DB_PORT'))
# app.config['MYSQL_DATABASE_USER'] = os.environ.get('DB_USER')
# app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('DB_PASSWORD')
# app.config['MYSQL_DATABASE_DB'] = os.environ.get('DB_DBNAME')
# ----------------------
# Bind app to db obj
db = SQLAlchemy(app)
# mysql = MySQL()
# mysql.init_app(app)
# ----------------------
''' Template filter converter for JSON formatted time '''
@app.template_filter('strftime')
def parse_date(datestring):
    timepart = datestring.split('(')[1].split(')')[0]
    milliseconds = int(timepart[:-5])
    hours = int(timepart[-5:]) / 100
    time = milliseconds / 1000
    dt = datetime.datetime.utcfromtimestamp(time + hours * 3600)
    return dt.strftime("%Y-%m-%d")
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

    try:
        # Execute query via SQLAlchemy engine
        results = db.engine.execute(query)
    except:
        # Query did not execute successfully
        return jsonify(default_response())

    # Parse row items into a list of dictionaries (JSON)
    list = parse_results(results)

    # Aggregate data into a JSON casted response map with count, message, and results
    return jsonify(compile_response(list))
# ----------------------
# Route 2, get all vehicles for a given year and make
@app.route('/api/<year>/<make>/', methods=['GET'])
def get_by_year_and_make(year, make):

    '''
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
    '''
    return ''
# ----------------------
# Route 3, get all vehicles for a given year and make
@app.route('/api/<year>/<make>/<model>/', methods=['GET'])
def get_by_year_make_and_model(year, make, model):

    '''
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

    # print(response)
    # Return JSON object
    return jsonify(response)
    '''
# ----------------------
@app.route('/')
def index():
    page = 'Home'
    return render_template('home.html', page=page)

    # return render_template('temp.html')
# ----------------------
@app.route('/report')
def report():
    page = 'Vehicle Report'
    return render_template('report.html', page=page)
    # return render_template('temp.html')
# ----------------------
@app.route('/handlerequest', methods=['POST'])
def handle_request():
    # print(request)
    page = 'Vehicle Report'
    try :
        year = request.form['year'].strip()
        make = request.form['make'].strip()
        model = request.form['model'].strip()

        data = get_by_year_make_and_model(year, make, model).get_json()
        recalls = get_recalls_from_NHTSA(year, make, model)
        complaints = get_complaints_from_NHTSA(year, make, model)

        return render_template('process_report.html', data=data, recalls=recalls, complaints=complaints, page=page)
    except Exception as e:
        print(e)
        # 404 not found
        return render_template('error.html', page=page)
# ----------------------
@app.route('/api')
def api():
    page = 'API Documentation'
    return render_template('api.html', page=page)
    # return render_template('temp.html')
# ----------------------
@app.route('/versions')
def versions():
    page = 'Version History'
    return render_template('versions.html', page=page)
    # return render_template('temp.html')
# ----------------------
@app.route('/about')
def about():
    page = 'About This Project'
    return render_template('about.html', page=page)
    # return render_template('temp.html')
# ----------------------
def run_app():
    app.run()
    return None
# ----------------------
if __name__ == '__main__':
    app.run(debug=True)
