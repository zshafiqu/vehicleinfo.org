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
def handleFiles(oldFilePath, newFilePath):
    # Does file reading & writing
    with open(oldFilePath) as oldFile:
        reader = csv.reader(oldFile) # create reader object from old file / path

        with open(newFilePath, 'w') as newFile:
            writer = csv.writer(newFile) # create writer object with new file / path
            writer.writerow(['year', 'make', 'model', 'body_style', 'image_src']) # write the headers on the first row of new file
            next(reader) # skip the first row of the old file


            for row in reader: # for each row in the old file
                '''
                In this schema,
                    year = row[0]
                    make = row[1]
                    model = row[2]
                    body_style = row[3] { str() literal representation of a list object }

                '''
                # print(row)
                writer.writerow([row[0], row[1], row[2], row[3], 'this is a new file.com'])
                
    return None
# ----------------------
'''
# calls below should open every file and print the first 5 items
yearCount = 1992

while (yearCount <= 2020):


    # dupYr = year
    strYear = str(yearCount)
    # print('CREATE TABLE '+strYear)
    filepath = 'car_data/'+strYear+'.csv' # filepath for each year
    newFileName = 'new_'+strYear+'.csv' # new file name for each year
    print(filepath)


    with open(filepath, 'r') as oldFile: # reading from old csv
        reader = csv.reader(oldFile)
        # counter = 0;

        next(reader) #skip header

        with open(newFileName, 'w') as newFile:
            writer = csv.writer(newFile, delimiter='\t')

            for line in reader:
                writer.writerow(line[1])
                # csv_write.writerow(line[0])



            # url = scrapeEdmunds(year, make, model)

            # print(year + ' ' + make + ' ' + model + ' ')
            # counter += 1
            # if counter is 5:
            #     break



    yearCount += 1
    '''
# ----------------------
