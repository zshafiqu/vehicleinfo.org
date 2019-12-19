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
    r = requests.get(url).json()

    return r

@app.route('/')
def index():
    # return '<h1> On home page </h1>'
    return render_template('landingpage.html')

@app.route('/random')
def random():
    # return '<h1> On home page </h1>'
    # return render_template('random.html')
    return getRecalls('2007', 'Honda', 'Civic')


if __name__ == '__main__':
    app.run(debug=True)
