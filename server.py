from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_wtf import FlaskForm
from wtforms import SelectField
from sqlalchemy.pool import QueuePool
from flask_minify import minify
from flask_caching import Cache
import requests, json, os, ast, datetime
# ----------------------
# import config
# from config import create_app
# app = create_app()
# Activate virtual env with - source env/bin/activate
# Initialize flask app, enable auto deploy from master branch for heroku
# app = Flask(__name__)
# # Setup simple cache instance configuration & Initialize it to app instance
# cache = Cache(config={'CACHE_TYPE': 'simple'})
# cache.init_app(app)
# # From flask_minify, wrap app around minify module to minify the HTML/CSS/JS responses
# minify(app=app, html=True, js=True, cssless=True)
# # Designate application URL routing to occur with or without a trailing slash
# # By default, all of the routes defined below exist without a trailing slash
# app.url_map.strict_slashes = False
# # Use Talisman to force any http:// prefixed requests to redirect to https://
# # Edit the CSP in order to serve CSS styles and JavaScript files
# Talisman(app, content_security_policy=None)
# app.secret_key = os.environ.get('KEY')
# # ----------------------
# # Configure flask app with info stored locally within environment (locally or heroku)
# # To install mysqlclient, needed to run brew install mysql
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('BASE_URI')
# # ----------------------
# cache = Cache(config={'CACHE_TYPE': 'simple'})
# cache.init_app(app)
# Bind app to db obj
# db = SQLAlchemy(app)
# # ----------------------
# # Was running into a timeouterror for mySQL on Heroku's clearDB instance.
# # Referencing stackoverflow, "the only work around I could find for this by
# # talking to the ClearDB people is to add in the pessimistic ping when creating the engine."
# # Not ideal since its pings DB everytime before you do a query, but avoids 500 Internal Server Error
# db = SQLAlchemy(engine_options={"pool_size": 10, "poolclass":QueuePool, "pool_pre_ping":True})
from config import create_server_instance

server = create_server_instance()
app = server.app
cache = server.cache
db = server.db
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
def get_table_name(year):
    return str(year)+'_vehicles'
# ----------------------
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
@app.route('/api/<year>', methods=['GET'])
def get_by_year(year):
    # Define table name for lookup and prepare query
    tableName = get_table_name(year)
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
@app.route('/api/<year>/<make>', methods=['GET'])
def get_by_year_and_make(year, make):
    # Define table name for lookup and prepare query
    tableName = get_table_name(year)
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
@app.route('/api/<year>/<make>/<model>', methods=['GET'])
def get_by_year_make_and_model(year, make, model):
    # Define table name for lookup and prepare query
    tableName = get_table_name(year)
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
@cache.cached(timeout=300)
def index():
    return render_template('home.html')
# ----------------------
# FlaskForm inherited from flask_wtf
class Form(FlaskForm):
    # SelectField inherited from wtforms
    # Utilizing list comprehension to hardcode the year range
    year = SelectField('year', choices=[(iter+1992, iter+1992) for iter in range(29)])
    make = SelectField('make', choices=[])
    model = SelectField('model', choices=[])
# ----------------------
# The cached decorator has optional argument called 'unless'
# This argument accepts a callable that returns True or False
# If unless returns True then it will bypass the caching mechanism entirely
def only_cache_get(*args, **kwargs):
    # Basically, bypasses the caching mechanism for 'POST' requests
    # If this isn't bypassed, if someone requests a report, and then presses on 'get a report'
    # The report they just submitted a request for gets cached on the server
    if request.method == 'GET':
        return False
    return True
# ----------------------
@app.route('/report', methods=['GET', 'POST'])
@cache.cached(timeout=300, unless=only_cache_get) # Cache on server for 5 minutes, and then pass unless parameter
def report():
    # Initialize some default value for when the page is loaded
    makes = get_distinct_makes_for_year(1992)
    form = Form()

    try:
        # Because jsonify() converts a python object to a Flask response, you need to use '.json' to make references
        # list comprehension to create tuples with (value, label) given by resulting lists from function calls
        form.make.choices = [(make['value'], make['label']) for make in get_distinct_makes_for_year(1992).json['makes']]
        form.model.choices = [(model['value'], model['label']) for model in get_all_models_for_year(form.make.choices[0][0], 1992).json['models']]
    except:
        return render_template('error.html')

    # If POST request, that means client hit 'submit' and is requesting a report
    if request.method == "POST":
        year = form.year.data
        make = form.make.data
        model = form.model.data

        try:
            data = get_by_year_make_and_model(year, make, model).get_json()
            recalls = get_recalls_from_NHTSA(year, make, model)
            complaints = get_complaints_from_NHTSA(year, make, model)

            return render_template('view_report.html',
                                   data=data,
                                   recalls=recalls,
                                   complaints=complaints)
        # Pass to error handler
        except Exception as e:
            return not_found(e)


    # For initial /GET requests
    return render_template('report.html', form=form)
# ----------------------
# Helper route for form selector, no need to cache this
@app.route('/models/<make>/<year>')
def get_all_models_for_year(make, year):
    tableName = get_table_name(year)
    raw_query = "SELECT MODEL FROM "+tableName+" WHERE make LIKE '"+make+"'"
    results = db.engine.execute(raw_query)

    model_list = []

    for row in results:
        model_object = dict()
        model_object['value'] = row[0]
        model_object['label'] = row[0]
        model_list.append(model_object)

    return jsonify({'models' : model_list})
# ----------------------
# Helper route for form selector, no need to cache this
@app.route('/makes/<year>')
def get_distinct_makes_for_year(year):
    tableName = get_table_name(int(year))
    raw_query = "SELECT DISTINCT MAKE FROM "+tableName
    results = db.engine.execute(raw_query)

    make_list = []

    for row in results:
        make_object = dict()
        make_object['value'] = row[0]
        make_object['label'] = row[0]
        make_list.append(make_object)

    return jsonify({'makes' : make_list})
# ----------------------
@app.route('/api')
@cache.cached(timeout=300) # Cache on server for 5 minutes
def api():
    return render_template('api.html')
# ----------------------
@app.route('/changelog')
@cache.cached(timeout=300) # Cache on server for 5 minutes
def changelog():
    return render_template('changelog.html')
# ----------------------
@app.route('/about')
@cache.cached(timeout=300) # Cache on server for 5 minutes
def about():
    return render_template('about.html')
# ----------------------
# This route handles error
@app.errorhandler(Exception)
@cache.cached(timeout=300) # Cache on server for 5 minutes
def not_found(e):
    return render_template('error.html')
# ----------------------
if __name__ == '__main__':
    # from waitress import serve
    # serve(app)
    app.run(debug=True)
