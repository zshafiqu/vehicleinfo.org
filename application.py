from flask import Flask, render_template
import requests, json

# Create flask app
app = Flask(__name__)

# Make an API call to the NHTSA page for recall Information
def getRecalls(year, make, model):
    # Build URL for call
    url = 'https://one.nhtsa.gov/webapi/api/Recalls/vehicle/modelyear/'
    url += year
    url += '/make/'
    url += make
    url += '/model/'
    url += model
    url += '?format=json'

    # Make request
    items = requests.get(url).json()
    results = []

    # Trim
    for item in items['Results']:
        print(item)
        print('\n')
        results.append(item)

    return items

@app.route('/')
def index():
    # return '<h1> On home page </h1>'
    recalls = getRecalls('2007', 'Honda', 'Civic')
    return render_template('dashboard.html')

@app.route('/random')
def random():
    # return '<h1> On home page </h1>'
    # return render_template('random.html')
    recalls = getRecalls('2007', 'Honda', 'Civic')
    return recalls

if __name__ == '__main__':
    app.run(debug=True)
