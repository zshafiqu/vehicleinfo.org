from flask import Flask, render_template, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
import requests, json, os, ast, datetime
# ----------------------
# Activate virtual env with - source env/bin/activate
# Initialize flask app, enable auto deploy from master branch for heroku
app = Flask(__name__)
app.secret_key = os.environ.get('KEY')
# ----------------------
# Configure flask app with info stored locally within environment (locally or heroku)
# To install mysqlclient, needed to run brew install mysql
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('BASE_URI')
# ----------------------
# Bind app to db obj
db = SQLAlchemy(app)
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
    if len(list) > 0:
        response['Message'] = 'Results returned successfully'
    else:
        response['Message'] = 'No results found for this request'
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
    # Define table name for lookup and prepare query
    tableName = str(year)+'_vehicles'
    query = "SELECT * FROM "+tableName+" WHERE make LIKE '"+make+"'"

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
# Route 3, get all vehicles for a given year and make
@app.route('/api/<year>/<make>/<model>/', methods=['GET'])
def get_by_year_make_and_model(year, make, model):
    # Define table name for lookup and prepare query
    tableName = str(year)+'_vehicles'
    query = "SELECT * FROM "+tableName+" WHERE make LIKE '"+make+"'"+" AND model LIKE '"+model+"'"

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
@app.route('/')
def index():
    return render_template('home.html')
# ----------------------
@app.route('/report')
def report():
    return render_template('report.html')
# ----------------------
@app.route('/view_report', methods=['POST'])
def handle_request():
    try:
        year = request.form['year'].strip()
        make = request.form['make'].strip()
        model = request.form['model'].strip()

        data = get_by_year_make_and_model(year, make, model).get_json()
        recalls = get_recalls_from_NHTSA(year, make, model)
        complaints = get_complaints_from_NHTSA(year, make, model)

        return render_template('view_report.html', data=data, recalls=recalls, complaints=complaints)
    except:
        return render_template('error.html')
# ----------------------
@app.route('/api')
def api():
    return render_template('api.html')
# ----------------------
@app.route('/changelog')
def changelog():
    return render_template('changelog.html')
# ----------------------
@app.route('/about')
def about():
    return render_template('about.html')
# ----------------------
if __name__ == '__main__':
    app.run()
