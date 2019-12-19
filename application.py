from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests, json
# ----------------------
# Create flask app
app = Flask(__name__)
# ----------------------
def scrapeEdmunds(year, make, model):
    # URL to scrape from
    url = 'https://www.edmunds.com/'+make+'/'+model+'/'+year+'/review/'
    # get html
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    imgSource = soup.find()
    return ''
# ----------------------
# Make an API call to the NHTSA page for recall Information
def getRecalls(year, make, model):
    # Build URL for call to JSON response
    url = 'https://one.nhtsa.gov/webapi/api/Recalls/vehicle/modelyear/'+year+'/make/'+make+'/model/'+model+'?format=json'
    # Make request
    items = requests.get(url).json()

    return items
# ----------------------
@app.route('/handleRequest', methods=['POST'])
def process():
    query = request.form['searchparameter']
    parameter = query.split()
    year = parameter[0]
    make = parameter[1]
    model = parameter[2]

    recalls = getRecalls(year, make, model)
    return render_template('dashboard.html', recalls=recalls)
# ----------------------
@app.route('/')
def index():
    return render_template('home.html')
# ----------------------
@app.route('/jsonTest')
def random():
    recalls = getRecalls('2007', 'lexus', 'es')
    return recalls
# ----------------------
if __name__ == '__main__':
    app.run(debug=True)
