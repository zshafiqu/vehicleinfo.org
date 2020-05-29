# This file's purpose is to host all the utilities our server will use to complete its operations
# Abstracting this because as the application gets more complex,
# we get more and more spaghetti code, so this should help with organization
# ----------------------
from flask_wtf import FlaskForm
from wtforms import SelectField
import requests, json, ast, datetime
# ----------------------
def parse_date_util(datestring):
    # Use this method to convert JSON formatted time
    # Parse through time and assign values
    timepart = datestring.split('(')[1].split(')')[0]
    milliseconds = int(timepart[:-5])
    hours = int(timepart[-5:]) / 100
    time = milliseconds / 1000

    # Format according to datetime
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
        # Default response for when we have no data to return
        response['Message'] = 'No results found for this request'

    response['Results'] = list

    return response
# ----------------------
def default_response():
    # Default response for when we have an error
    response = dict()
    response['Count'] = 0
    response['Message'] = 'No results found for this request'
    response['Results'] = []

    return response
# ----------------------
# FlaskForm inherited from flask_wtf
class Form(FlaskForm):
    # SelectField inherited from wtforms
    # Utilizing list comprehension to hardcode the year range
    year = SelectField('year', choices=[(iter+1992, iter+1992) for iter in range(29)])
    make = SelectField('make', choices=[])
    model = SelectField('model', choices=[])
# ----------------------
# Use this for dynamic select field to get value & label for HTML
def parse_value_label(results):
    list = []

    for row in results:
        make_object = dict()
        make_object['value'] = row[0]
        make_object['label'] = row[0]
        list.append(make_object)

    return list
# ----------------------
# Use this helper function to hit the NHTSA API to decode the vin for us in a JSON consumable format
def decode_vin_vpic(vin):
    # Build a URL to hit the vPIC API from the NHTSA
    vin = str(vin).strip() # Cast to string and strip of whitespace as precaution
    url = 'https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/'+vin+'?format=json'
    # Make request
    items = requests.get(url).json()
    return items
# ----------------------
# Use this method to verify the response we got contains actual data and not errors
def validate_vpic_response(data):
    # Check data column within JSON response
    if data['Results'][1]['Value'] != "0":
        return False
    return True
# ----------------------
def validate_vin_length(vin):
    if len(vin) != 17:
        return False
    return True
# ----------------------
