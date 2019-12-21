from bs4 import BeautifulSoup, SoupStrainer
from urllib import urlopen
import requests, json, os, mysql.connector, csv, ast, random
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
def getHeader():
    # return a random user agent header based on generated number
    list = [
            {
             'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36',
             'Origin': 'http://example.com',
             'Referer': 'http://example.com/some_page'
             },
            {
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
             'Origin': 'http://example.com',
             'Referer': 'http://example.com/some_page'
             },
            {
             'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
             'Origin': 'http://example.com',
             'Referer': 'http://example.com/some_page'
             },
            {
             'User-Agent': 'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
             'Origin': 'http://example.com',
             'Referer': 'http://example.com/some_page'
            },
            {
             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
             'Origin': 'http://example.com',
             'Referer': 'http://example.com/some_page'
             },
            {
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
             'Origin': 'http://example.com',
             'Referer': 'http://example.com/some_page'
             },
            {
             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
             'Origin': 'http://example.com',
             'Referer': 'http://example.com/some_page'
             },
            {
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
             'Origin': 'http://example.com',
             'Referer': 'http://example.com/some_page'
             },
            {
             'User-Agent': 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
             'Origin': 'http://example.com',
             'Referer': 'http://example.com/some_page'
             },
            {
             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
             'Origin': 'http://example.com',
             'Referer': 'http://example.com/some_page'
             },
            {
             'User-Agent': 'Mozilla/5.0 (X11; U; Linux i586; en-US) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/5.0.342.1 Safari/533.2',
             'Origin': 'http://example.com',
             'Referer': 'http://example.com/some_page'
             }
        ]
    # list is of size 11
    curr = random.randrange(0, 10)
    return list[curr]
# ----------------------
def getSoup():
    # required to emulate broswer user agent
    url = 'https://www.kbb.com/honda/civic/1992/'

    # get html
    # source = requests.get(url, headers=headers).text
    headers = getHeader()

    # headers={ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0' }
    # agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    page = requests.get(url, headers=headers).text
    onlyImgTags = SoupStrainer(class_="css-4g6ai3")



    soup = BeautifulSoup(page, 'lxml', parse_only=onlyImgTags)
    print(soup)
    print('\n')
    imgSource = soup.findAll("img", {"class":"css-4g6ai3"})

    print(imgSource[0]['src'])
    # return the soup'd data
    return ''
# ----------------------
# def scrapeKBB(year, make, model, bodystyles):
#     # build KBB url
#     url = 'https://www.kbb.com/'+make+'/'+model+'/'+year+'/'
#
#     if (len(bodystyles) > 1):
#
#
#     imgSource = soup.findAll("img", {"class":"css-4g6ai3"})
#
#     # print(imgSource)
#
#     '''
#     if length of body_style > 1
#         for each body style
#             create a url
#                 make a request to that URL
#
#
#
#
#     return a list of img sources,
#
#     '''
#
#
#
#
#     return ''
# ----------------------
def handleFiles(oldFilePath, newFilePath):
    # count = 1.0
    # Does file reading & writing
    with open(oldFilePath) as oldFile:
        reader = csv.reader(oldFile) # create reader object from old file / path

        with open(newFilePath, 'w') as newFile:
            writer = csv.writer(newFile) # create writer object with new file / path
            writer.writerow(['year', 'make', 'model', 'body_style']) # write the headers on the first row of new file
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
                # src = scrapeEdmunds(row[0], row[1], row[2])
                src = []
                # print(len(row[3]))
                res = ast.literal_eval(row[3])
                # res = json.loads(row[3])
                # print(res)
                # print(len(res))
                writer.writerow([row[0], row[1], row[2], res])
                # print(src)
                # print '*' * int(count)
                # count += .22

    return None
# ----------------------
getSoup()
# handleFiles('car_data/1992.csv', 'new_1992.csv')

# yearCount = 1992
#
# while (yearCount <= 2020):
#     stringYear = str(yearCount)
#     old = 'car_data/'+stringYear+'.csv'
#     # new = 'new_'+stringYear+'.csv'
#     new = stringYear+'.csv'
#
#     print(new)
#     print("<------------------------------>")
#     print('\n')
#     handleFiles(old, new)
#
#     yearCount += 1

# ----------------------
