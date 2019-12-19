from flask import Flask, render_template, request
import requests, json
# ----------------------
# Create flask app
app = Flask(__name__)
# ----------------------
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

    return items
# ----------------------
@app.route('/handleRequest', methods=['POST'])
def process():
    query = request.form['searchparameter']
    parameter = query.split()

    recalls = getRecalls(parameter[0], parameter[1], parameter[2])
    return render_template('dashboard.html', recalls=recalls, parameter=parameter)
# ----------------------
@app.route('/')
def index():
    # return '<h1> On home page </h1>'
    # recalls = getRecalls('2014', 'BMW', '320i')
    return render_template('home.html')
# ----------------------
@app.route('/jsonTest')
def random():
    # return '<h1> On home page </h1>'
    # return render_template('random.html')
    recalls = getRecalls('2007', 'lexus', 'es')
    return recalls
# ----------------------
if __name__ == '__main__':
    app.run(debug=True)
