import requests, json
from bottle import run, route


@route('/')
def index():
    # url = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeId/440?format=json'
    # r = requests.get(url).json()
    # return r['Results'][0]['Model_Name']
    # return r

    year = '2009'
    make = 'honda'
    model = 'accord'
    # test call for recalls
    url = 'https://one.nhtsa.gov/webapi/api/Recalls/vehicle/modelyear/'
    url += year
    url += '/make/'
    url += make
    url += '/model/'
    url += model
    url += '?format=json'

    results = []
    r = requests.get(url).json()

    for result in r['Results']:
        results.append(result['NHTSACampaignNumber'] + '  ')

    return results

if __name__ == '__main__':
    run(debug=True, reloader=True)
