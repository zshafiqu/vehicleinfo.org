import requests, json
from bottle import run, route


@route('/')
def index():
    url = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeId/440?format=json'
    r = requests.get(url).json()
    # return r['Results'][0]['Model_Name']
    return r

if __name__ == '__main__':
    run(debug=True, reloader=True)
