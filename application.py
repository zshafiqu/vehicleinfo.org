from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from urllib import urlopen
import requests, json
'''
requirements ->
flask, bs4, lxml
'''
# ----------------------
# Create flask app
app = Flask(__name__)
# ----------------------
def scrapeEdmunds(year, make, model):
    # URL to scrape from
    # url = 'https://www.edmunds.com/'+make+'/'+model+'/'+year+'/review/'
    url = 'https://www.edmunds.com/lexus/es-300/2001/review/'
    # required to emulate broswer user agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36',
        'Origin': 'http://example.com',
        'Referer': 'http://example.com/some_page'
        }
    # get html
    source = requests.get(url, headers=headers).text
    soup = BeautifulSoup(source, 'lxml')
    imgSource = soup.findAll("img", {"class":"w-100"})
    imgSource = imgSource[0]['src']
    print(imgSource)

    return imgSource
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
    imagesrc = scrapeEdmunds(year, make, model)
    return render_template('dashboard.html', recalls=recalls, imagesrc=imagesrc)
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
