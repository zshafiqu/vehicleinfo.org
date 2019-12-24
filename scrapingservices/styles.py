from bs4 import BeautifulSoup, SoupStrainer
import requests, json, os, mysql.connector, csv, ast, random
import images
# ----------------------
def getSoup(url):
    # Entered getSoup method
    print('About to make request for data')
    iter = 0

    # Continually try to make this request until its successful
    while True:
        if iter is 15:
            # OR until 15 times, at which point stop wasting time and break
            page = ''
            break
        try:
            # Generate a new header [required to emulate browser behavior]
            headers = images.getHeader()
            # Request for the resource, timeout after 20 seconds (for hanging requests)
            page = requests.get(url, headers=headers, timeout=20).text
        except:
            # If the request fails, log it, and try again
            print('Fail on request #'+str(iter)+', trying again')
            iter += 1
            continue
        break # Break out of while loop here on success of the try block


    print('Finished request')

    onlyBoxes = SoupStrainer("div", class_="css-130z0y1-StyledBox-default emf8dez0")
    soup = BeautifulSoup(page, 'lxml', parse_only=onlyBoxes)

    return soup
# ----------------------
def parseSoupToMap(soup):
    '''
    Every vehicle follows the same pattern with four attributes per trim {
        Fuel Economy,
        Seating,
        Horsepower,
        Engine
    }

    Length of headings will tell us how many trims there are

    len(headings) = 3

    Length of attributes is a function of (8 * length(headings))

    attributes are split by a key and value

    len(attributes) = 24

    o(m*n) implementation would be for each trim, create a dictionary until you've reached
    counter = headingNumber * 8

    ie {
        for heading in headings
            for attribute in attributes
                go until you've finished this trims attributes
            dict { trim : {Attributes} , trim : {attributes} }
    }


    '''
    headings = soup.findAll("h3")
    attributes = soup.findAll("p")
    outermap = dict()

    i = 0
    j = 0

    while i < len(headings):
        z = 0
        innermap = dict()
        while j < len(attributes):
            if z > 7:
                break
            else:
                innermap[str(attributes[j].text)] = str(attributes[j+1].text)
            j += 2
            z += 2
        outermap[str(headings[i].text)] = innermap
        i += 1

    # print(outermap)
    # All style headings within h3 tags with class = 'css-lg2ecn-StyledHeading3-defaultStyles-h3 e1jv8h5t2'
    # <p class="css-35ezg3" is the key, ex) -> Fuel Economy
    # <p> that follows is the value

    return outermap
# ----------------------
def scrapeTrimData(year, make, model, bodystyles):
    # Cleanse input
    # print('\n')
    print(bodystyles)
    print('\n')
    # print('\n')
    model = model.replace('&', '')
    model = model.replace('/', '')
    trims = dict()

    if len(bodystyles) is 1:
        url = 'https://www.kbb.com/'+make+'/'+model+'/'+year+'/'
        soup = getSoup(url)

        try:
            result = parseSoupToMap(soup)
        except:
            print("Error on parsing soup to map / single bodystyle / inside of scrape trim data")
            result = dict()

        trims[bodystyles[0]] = result

    else:
        index = 0
        for style in bodystyles:
            url = 'https://www.kbb.com/'+make+'/'+model+'/'+year+'/'+'?bodystyle='+style
            soup = getSoup(url)

            try:
                result = parseSoupToMap(soup)
            except:
                print("Error on parsing soup to map / multiple bodystyle / inside of scrape trim data")
                result = dict()

            trims[bodystyles[index]] = result
            # i++
            index += 1

    print('\n')
    print(trims)
    return trims
# ----------------------
def handleFilesForStyles(oldFilePath, newFilePath):
    # Does file reading & writing
    with open(oldFilePath) as oldFile:
        # create reader object from old file / path
        reader = csv.reader(oldFile)

        with open(newFilePath, 'w') as newFile:
            # create writer object with new file / path
            writer = csv.writer(newFile)
            # write the headers on the first row of new file
            writer.writerow(['year', 'make', 'model', 'body_style(s)', 'trim(s)', 'image_source(s)'])
            # skip the first row of the old file
            next(reader)

            '''
            This time, we have the following info {
                year = row[0]
                make = row[1]
                model = row[2]
                bodystyles = row[3]
                image_sources = row[4]
            }

            Goal:
                For each row, get its list of recalls as a json object
                by making a call to getRecalls(year, make, model)

            Results:
                the CSV table should look like ->
                ------------------------------------------------------------
                year | make | model | body_styles | image_sources | recalls
                ------------------------------------------------------------
            '''
            # jobs = []
            for row in reader:
                # print('\n')
                print('\n-------------------------------------------------------------')
                print('Beginning row operations for '+row[0]+' '+row[1]+' '+row[2])

                # Convert the make to a string list, we use this to handle case where make is two words
                makeAsList = list(row[1].split(" "))
                # Convert our bodystyles item from string list to list list so we can access len()
                bodylist = ast.literal_eval(row[3])

                if len(makeAsList) is 2:
                    # Convert back to a string with a dash in between the words
                    makeAsStr = makeAsList[0]+'-'+makeAsList[1]
                    trims = scrapeTrimData(row[0], makeAsStr, row[2], bodylist)
                    # Write { year , make , model, body_styles, trims,  image_sources }
                    writer.writerow([row[0], row[1], row[2], bodylist, trims, row[4]])

                # If make is of size 1, something like Ford || Honda
                else:
                    # Pass it to scrapeKBB func, referencing the first item in the list { makeAsList[0] }
                    trims = scrapeTrimData(row[0], makeAsList[0], row[2], bodylist)
                    # Write { year , make , model, body_styles, trims,  image_sources }
                    writer.writerow([row[0], row[1], row[2], bodylist, trims, row[4]])

                # print(s)
                print('\nFinished row operations for '+row[0]+' '+row[1]+' '+row[2])
                # print('-------------------------------------------------------------')
                # print('\n')

        return None
# ----------------------
def patchWithNull(oldFilePath, newFilePath):
    # Does file reading & writing
    with open(oldFilePath) as oldFile:
        # create reader object from old file / path
        reader = csv.reader(oldFile)

        with open(newFilePath, 'w') as newFile:
            # create writer object with new file / path
            writer = csv.writer(newFile)
            # write the headers on the first row of new file
            writer.writerow(['year', 'make', 'model', 'body_styles', 'trims', 'image_sources'])
            # skip the first row of the old file
            next(reader)

            '''
            This time, we have the following info {
                year = row[0]
                make = row[1]
                model = row[2]
                bodystyles = row[3]
                trim_data = row[4]
                image_sources = row[5]
            }
            '''
            # jobs = []
            for row in reader:
                # print('\n')
                # print('\n-------------------------------------------------------------')
                # print('Beginning row operations for '+row[0]+' '+row[1]+' '+row[2])

                trimStr = str(row[4])
                if "{}" in trimStr:
                    print('Error found in: '+row[0]+' '+row[1]+' '+row[2])
                    writer.writerow([row[0], row[1], row[2], row[3], 'NULL', row[5]])
                else:
                    writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5]])

                # print('\nFinished row operations for '+row[0]+' '+row[1]+' '+row[2])
                # print('-------------------------------------------------------------')
                # print('\n')

        return None
# ----------------------
def createOldPath(year):
    return 'master_data/'+str(year)+'.csv'
# ----------------------
def createNewPath(year):
    return str(year)+'.csv'
# ----------------------
# old = createOldPath('test')
# new = createNewPath('test')
# handleFilesForStyles(old, new)
count = 1992
while count <= 1992:
    old = createOldPath(count)
    new = createNewPath(count)
    print('Currently working on: ' +new)
    patchWithNull(old, new)
    print('Finished: '+new)

    count += 1
