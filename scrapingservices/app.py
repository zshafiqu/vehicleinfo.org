from bs4 import BeautifulSoup
from urllib import urlopen
import requests, json, os, mysql.connector, csv
# Script to scrape images for each vehicle in our list
''' The goal of this script is to store the source for each image in our database '''

username = os.environ.get('DB_USER')
dbname = os.environ.get('DB_NAME')
passwd = os.environ.get('DB_PASS')
server = os.environ.get('DB_SERVER')
port = os.environ.get('DB_PORT')

# mydb = mysql.connector.connect(host=server, port=port, user=username, password=passwd, database=dbname)
# print('databse connected')

# mysql://scott:tiger@localhost/mydatabase
# ----------------------
def scrapeEdmunds(year, make, model):
    # URL to scrape from
    url = 'https://www.edmunds.com/'+make+'/'+model+'/'+year+'/review/'
    # url = 'https://www.edmunds.com/lexus/es-300/2001/review/'

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

    # Run Check
    if len(imgSource) is 0:
        imgSource = 'https://www.autotechemporium.com/frontend/assets/images/placeholder/inventory-full-placeholder.png'
    else:
        imgSource = imgSource[0]['src']

    # imgSource = 'https://www.autotechemporium.com/frontend/assets/images/placeholder/inventory-full-placeholder.png'
    # print(imgSource)
    return imgSource
# ----------------------

# calls below should open every file and print the first 5 items
yearCount = 1992

while (yearCount <= 2020):

    # dupYr = year
    strYear = str(yearCount)
    # print('CREATE TABLE '+strYear)
    filepath = 'car_data/'+strYear+'.csv'
    newFile = 'new_'+strYear+'.csv'
    print(filepath)


    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        # counter = 0;

        # next(csv_reader) #skip header

        with open(newFile, 'w') as new_file:
            csv_write = csv.writer(new_file, delimiter='\t')

            for line in csv_reader:
                csv_write.writerow(line[0])
                csv_write.writerow(line[0])



            # url = scrapeEdmunds(year, make, model)

            # print(year + ' ' + make + ' ' + model + ' ')
            # counter += 1
            # if counter is 5:
            #     break



    yearCount += 1
# ----------------------
