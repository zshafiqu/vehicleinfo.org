# Main server file
# ----------------------
# Package imports defined by requirements
from flask import render_template, jsonify, request
import json
# ----------------------
# Local imports that we created
from configurations import create_server_instance
from api_utilities import *
# ----------------------
# Create server instance and grab values
server = create_server_instance()
app = server.app # Flask app object
cache = server.cache # Flask cache object
db = server.db # Database object
cache_timeout = server.cache_timeout # Cache timeout value for server
# ----------------------
# Template filter converter for JSON formatted time
@app.template_filter('strftime')
def parse_date(datestring):
    return parse_date_util(datestring)
# ----------------------
''' ALL API ROUTES LIVE BELOW THIS COMMENT '''
# ----------------------
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
# Helper route for form selector, no need to cache this
@app.route('/models/<make>/<year>')
def get_all_models_for_year(make, year):
    tableName = get_table_name(year)
    raw_query = "SELECT MODEL FROM "+tableName+" WHERE make LIKE '"+make+"'"
    results = db.engine.execute(raw_query)
    model_list = parse_value_label(results)

    return jsonify({'models' : model_list})
# ----------------------
# Helper route for form selector, no need to cache this
@app.route('/makes/<year>')
def get_distinct_makes_for_year(year):
    tableName = get_table_name(int(year))
    raw_query = "SELECT DISTINCT MAKE FROM "+tableName
    results = db.engine.execute(raw_query)
    make_list = parse_value_label(results)

    return jsonify({'makes' : make_list})
# ----------------------
''' ALL VIEW ROUTES LIVE BELOW THIS COMMENT '''
# ----------------------
@app.route('/')
@cache.cached(timeout=cache_timeout)
def index():
    return render_template('home.html')
# ----------------------
@app.route('/api')
@cache.cached(timeout=cache_timeout)
def api():
    return render_template('api.html')
# ----------------------
@app.route('/changelog')
@cache.cached(timeout=cache_timeout)
def changelog():
    return render_template('changelog.html')
# ----------------------
@app.route('/about')
@cache.cached(timeout=cache_timeout)
def about():
    return render_template('about.html')
# ----------------------
# The cached decorator has optional argument called 'unless'
# This argument accepts a callable that returns True or False
# If unless returns True then it will bypass the caching mechanism entirely
def only_cache_GET(*args, **kwargs):
    # Basically, bypasses the caching mechanism for 'POST' requests
    # If this isn't bypassed, if someone requests a report, and then presses on 'get a report'
    # The report they just submitted a request for gets cached on the server [which we don't want]
    if request.method == 'GET':
        return False
    return True
# ----------------------
@app.route('/report', methods=['GET', 'POST'])
@cache.cached(timeout=cache_timeout, unless=only_cache_GET) # Cache on server for 5 minutes, and then pass unless parameter
def report():
    # Initialize some default value for when the page is loaded
    makes = get_distinct_makes_for_year(1992)
    form = Form()

    try:
        # Because jsonify() converts a python object to a Flask response, you need to use '.json' to make references
        # list comprehension to create tuples with (value, label) given by resulting lists from function calls
        form.make.choices = [(make['value'], make['label'])
                             for make in get_distinct_makes_for_year(1992).json['makes']]
        form.model.choices = [(model['value'], model['label'])
                              for model in get_all_models_for_year(form.make.choices[0][0], 1992).json['models']]
    except Exception as e:
        return not_found(e)

    # If POST request, that means client hit 'submit' and is requesting a report
    if request.method == "POST":
        year = form.year.data
        make = form.make.data
        model = form.model.data
        print(year)
        print(make)
        print(model)

        include_recalls = form.recalls.data
        include_complaints = form.complaints.data
        print(include_recalls)
        print(include_complaints)

        # ---------
        if include_recalls and include_complaints:
            # do something
            try:
                data = get_by_year_make_and_model(year, make, model).get_json()
                recalls = get_recalls_from_NHTSA(year, make, model)
                complaints = get_complaints_from_NHTSA(year, make, model)

                try:
                    return render_template('view_report.html',
                                    data=data,
                                    recalls=recalls,
                                    complaints=complaints)
                except Exception as e:
                    return not_found(e)
            # Pass to error handler
            except Exception as e:
                return not_found(e)
        # ---------
        elif include_recalls and not include_complaints:
            try:
                data = get_by_year_make_and_model(year, make, model).get_json()
                recalls = get_recalls_from_NHTSA(year, make, model)
                complaints = None

                try:
                    return render_template('view_report.html',
                                    data=data,
                                    recalls=recalls,
                                    complaints=complaints)
                except Exception as e:
                    return not_found(e)
            # Pass to error handler
            except Exception as e:
                return not_found(e)
        # ---------
        elif include_complaints and not include_recalls:
            try:
                data = get_by_year_make_and_model(year, make, model).get_json()
                recalls = None
                complaints = get_complaints_from_NHTSA(year, make, model)

                try:
                    return render_template('view_report.html',
                                    data=data,
                                    recalls=recalls,
                                    complaints=complaints)
                except Exception as e:
                    return not_found(e)
            # Pass to error handler
            except Exception as e:
                return not_found(e)
        # ---------
        else:
            try:
                data = get_by_year_make_and_model(year, make, model).get_json()
                recalls = None
                complaints = None

                try:
                    return render_template('view_report.html',
                                    data=data,
                                    recalls=recalls,
                                    complaints=complaints)
                except Exception as e:
                    return not_found(e)
            # Pass to error handler
            except Exception as e:
                return not_found(e)



        # stuff = request.form.getlist('optionsbox')
        # print(stuff)

        # try:
        #     data = get_by_year_make_and_model(year, make, model).get_json()
        #     recalls = get_recalls_from_NHTSA(year, make, model)
        #     complaints = get_complaints_from_NHTSA(year, make, model)
        #
        #     try:
        #         return render_template('view_report.html',
        #                         data=data,
        #                         recalls=recalls,
        #                         complaints=complaints)
        #     except Exception as e:
        #         return not_found(e)
        # # Pass to error handler
        # except Exception as e:
        #     return not_found(e)

    # For initial /GET requests
    return render_template('report.html', form=form)
# ----------------------
@app.route('/decoder', methods=['GET', 'POST'])
@cache.cached(timeout=cache_timeout, unless=only_cache_GET) # Cache on server for 5 minutes, and then pass unless parameter
def decoder():
    # When client hits submit
    if request.method == "POST":
        try:
            vin = request.form['VIN'].strip()
            # If the vin isn't 17 in length, no need to hit the vPIC API
            if validate_vin_length(vin) is not True:
                return not_found(get_decode_error(0))

            # Make an API call now
            response = decode_vin_vpic(vin)
            # No guarantee the VIN was valid, so check
            if validate_vpic_response(response) is not True:
                return not_found(get_decode_error(1))

            # If all is good, finally attempt to render Template
            return render_template('view_decoded.html', response=response)

        # If for whatever reason this fails, return an error
        except Exception as e:
            return not_found(e)
    # For all other request methods, i.e. 'GET', return the form page
    return render_template('decoder.html')
# ----------------------
# This route handles error
# Do not cache the error handler otherwise it'll stay within certain routes even after an error has been rendered
# By default, e is None unless an error description was passed to the function
@app.errorhandler(Exception)
def not_found(e=None):
    # Convert the error message to a string type if its not None, that way whatever the error message is,
    # it'll guarantee to be output
    # Then pass it to the error message if neccesary
    if e is not None:
        e = str(e)
    return render_template('error.html', e=e)
# ----------------------
if __name__ == '__main__':
    # from waitress import serve
    # serve(app)
    app.run(debug=True)
# ----------------------
