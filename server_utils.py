# This file's purpose is to host all the utilities our server will use to complete its operations
# Abstracting this because as the application gets more complex,
# we get more and more spaghetti code, so this should help with organization
# ----------------------
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
