from bs4 import BeautifulSoup, SoupStrainer
import requests, json, os, mysql.connector, csv, ast, random
# Script to scrape images for each vehicle in our list
''' The goal of this script is to store the source for each image in our database '''

# username = os.environ.get('DB_USER')
# dbname = os.environ.get('DB_NAME')
# passwd = os.environ.get('DB_PASS')
# server = os.environ.get('DB_SERVER')
# port = os.environ.get('DB_PORT')

# mydb = mysql.connector.connect(host=server, port=port, user=username, password=passwd, database=dbname)
# print('databse connected')

# mysql://scott:tiger@localhost/mydatabase
# ----------------------
# def scrapeEdmunds(year, make, model):
#     # URL to scrape from
#     url = 'https://www.edmunds.com/'+make+'/'+model+'/'+year+'/review/'
#     # url = 'https://www.edmunds.com/lexus/es-300/2001/review/'
#
#     # required to emulate broswer user agent
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36',
#         'Origin': 'http://example.com',
#         'Referer': 'http://example.com/some_page'
#         }
#
#     # get html
#     source = requests.get(url, headers=headers).text
#     soup = BeautifulSoup(source, 'lxml')
#     imgSource = soup.findAll("img", {"class":"w-100"})
#
#     # Run Check
#     if len(imgSource) is 0:
#         imgSource = 'https://www.autotechemporium.com/frontend/assets/images/placeholder/inventory-full-placeholder.png'
#     else:
#         imgSource = imgSource[0]['src']
#
#     # imgSource = 'https://www.autotechemporium.com/frontend/assets/images/placeholder/inventory-full-placeholder.png'
#     # print(imgSource)
#     return imgSource
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
def getSoup(url):
    # Get soup via URL
    print('About to make request')
    i = 0

    # Continually try to make this request until its successful
    while True:
        if i is 15:
            # OR until 15 times, at which point stop wasting time and break
            page = ''
            break
        try:
            # Generate a new header [required to emulate browser behavior]
            headers = getHeader()
            # Request for the resource, timeout after 20 seconds (for hanging requests)
            page = requests.get(url, headers=headers, timeout=20).text
        except:
            # If the request fails, log it, and try again
            print('Fail on request #'+str(i)+', trying again')
            i += 1
            continue
        break # Break out of while loop here on success of the try block

    # Log that the request has been completed
    print('Finished request')
    # SoupStrainer sets it such that we only parse the response for items with this class tag
    # Helps reduce time spent doing unneccesary work
    onlyImgTags = SoupStrainer(class_="css-4g6ai3")
    # BeautifulSoup parses the page as xml for us
    soup = BeautifulSoup(page, 'lxml', parse_only=onlyImgTags)

    # return the soup'd data
    return soup
# ----------------------
def scrapeKBBImages(year, make, model, bodystyles):
    # Scrape KBB for image sources
    map = dict()

    # If there is only one body type, no need to worry about searching for multiple images
    if (len(bodystyles) == 1):
        # Build URL & get soup
        url = 'https://www.kbb.com/'+make+'/'+model+'/'+year+'/'
        soup = getSoup(url)

        # Attempt to parse for an image item from the soup'd data
        try:
            imgSource = soup.findAll("img", {"class":"css-4g6ai3"})
            map[bodystyles[0]] = imgSource[0]['src']
        # If the soup'd HTML does not contain any image tags with that class, resort to a default img value
        except:
            print("Error on scraping KBB, single body style")
            map[bodystyles[0]] = 'https://www.autotechemporium.com/frontend/assets/images/placeholder/inventory-full-placeholder.png'

    # If there are multiple body styles, we need to get an image for each style
    else:
        index = 0
        for style in bodystyles:
            # Build unique URL for each body style & then get Soup
            url = 'https://www.kbb.com/'+make+'/'+model+'/'+year+'/'+'?bodystyle='+style
            soup = getSoup(url)

            # Attempt to parse for an image item from the soup'd data
            try:
                imgSource = soup.findAll("img", {"class":"css-4g6ai3"})
                map[style] = imgSource[0]['src']

            # If the soup'd HTML does not contain any image tags with that class, resort to a default img value FOR CURRENT bodystyle
            except:
                print('Error on scraping KBB, multiple body type')
                map[bodystyles[index]] = 'https://www.autotechemporium.com/frontend/assets/images/placeholder/inventory-full-placeholder.png'

            # Increment loop counter
            index += 1

    print(map)
    return map
# ----------------------
def handleFiles(oldFilePath, newFilePath):
    # Does file reading & writing
    with open(oldFilePath) as oldFile:
        reader = csv.reader(oldFile) # create reader object from old file / path

        with open(newFilePath, 'w') as newFile:
            writer = csv.writer(newFile) # create writer object with new file / path
            writer.writerow(['year', 'make', 'model', 'body_style(s)', 'image_source(s)']) # write the headers on the first row of new file
            next(reader) # skip the first row of the old file

            # for each row in the old file
            for row in reader:
                '''
                In this schema,
                    year = row[0]
                    make = row[1]
                    model = row[2]
                    body_style = row[3] { str() literal representation of a list object }
                    imgs = scrapeKBB(year, make, model, body_style)

                '''
                # Need to update the last few vehicles without an image
                '''
                Blank imgs:
    
                12 ram c/v == https://file.kelleybluebookimages.com/kbb/base/house/2012/2012-Ram-C/V-FrontSide_RACV121_640x480.jpg?interpolation=high-quality&downsize=391:*
                13 -15 ram c/v tradesman = https://file.kelleybluebookimages.com/kbb/base/house/2012/2012-Ram-C/V-FrontSide_RACV121_640x480.jpg?interpolation=high-quality&downsize=391:*

                15 mini coupe == https://file.kbb.com/kbb/vehicleimage/housenew/480x360/2015/2015-mini-coupe-frontside_mncpe151.jpg
                19 mini convertible == https://file.kbb.com/kbb/vehicleimage/evoxseo/xl/12925/2019-mini-convertible-front-angle3_12925_089_480x360.jpg


                '''

                if (row[2] == 'Town & Country'):
                    bodylist = ast.literal_eval(row[3])
                    imgs = scrapeKBBImages(row[0], row[1], 'towncountry', bodylist)
                    writer.writerow([row[0], row[1], row[2], bodylist, imgs])
                else:
                    # Dont patch if not chrysler town and country
                    writer.writerow([row[0], row[1], row[2], row[3], row[4]])

                '''
                # Convert the make to a string list, we use this to handle case where make is two words
                makeAsList = list(row[1].split(" "))
                # Convert our bodystyles item from string list to list list so we can access len()
                bodylist = ast.literal_eval(row[3])

                # If make is of size 2, meaning it contains two words, for example Land Rover || Aston Martin
                if len(makeAsList) is 2:
                    # Convert back to a string with a dash in between the words
                    makeAsStr = makeAsList[0]+'-'+makeAsList[1]
                    # Scrape for image sources / retrieve ke/value mapping for body style : img url
                    imgs = scrapeKBBImages(row[0], makeAsStr, row[2], bodylist)
                    # Write { year , make , model, body_styles, image_sources }
                    writer.writerow([row[0], row[1], row[2], bodylist, imgs])

                # If make is of size 1, something like Ford || Honda
                else:
                    # Pass it to scrapeKBB func, referencing the first item in the list { makeAsList[0] }
                    imgs = scrapeKBBImages(row[0], makeAsList[0], row[2], bodylist)
                    # Write { year , make , model, body_styles, image_sources }
                    writer.writerow([row[0], row[1], row[2], bodylist, imgs])
                '''

    return None
# ----------------------
def readForBlanks(filename):
    with open(filename) as oldFile:
        reader = csv.reader(oldFile)
        next(reader)

        for row in reader:
            res = ast.literal_eval(row[4])
            for key in res:
                if (res[key] == 'https://www.autotechemporium.com/frontend/assets/images/placeholder/inventory-full-placeholder.png'):
                    print(row[0] + ' ' + row[1] + ' ' + row[2])

            # print(res)
            # print(row[4])
    return None
# ----------------------
''' Run script to check for any defaults '''
count = 1992
while count <= 2020:
    stryr = str(count)
    path = 'KBB_data/'+stryr+'.csv'

    print("Reading from: "+path)
    readForBlanks(path)
    print('\n')

    count += 1


# handleFiles('KBB/1992.csv', '1992.csv')
# ''' Run script for make and models from 1992 -> 2020 '''
# yearCount = 1992
#
# while (yearCount <= 2020):
#     stringYear = str(yearCount)
#     old = 'KBB_data/'+stringYear+'.csv'
#     new = stringYear+'.csv'
#     # new = stringYear+'.csv'
#
#     print(new)
#     print("<------------------------------>")
#     print('\n')
#     handleFiles(old, new)
#
#     yearCount += 1
# ----------------------
