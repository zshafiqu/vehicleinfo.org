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
            print('Fail on request #'+str(i)+', trying again')
            iter += 1
            continue
        break # Break out of while loop here on success of the try block


    print('Finished request')

    onlyBoxes = SoupStrainer("div", class_="css-130z0y1-StyledBox-default emf8dez0")
    soup = BeautifulSoup(page, 'lxml', parse_only=onlyBoxes)

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

    # print(soup.prettify())
    headings = soup.findAll("h3")
    attributes = soup.findAll("p")
    # attributes = attributes.text
    #
    # for attribute in attributes:
    #     print()

    # print(headings)
    # print('\n')
    # print(attributes)

    # i = 0
    # while i < len(attributes)

    # for heading in headings:
    #     print(heading.text)
    #     print('\n')
    #
    # for attribute in attributes:
    #     print(attribute.text)
    #     print('\n')

    outermap = dict()

    ''' 0 , 1 '''
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

    print(outermap)
    # All style headings within h3 tags with class = 'css-lg2ecn-StyledHeading3-defaultStyles-h3 e1jv8h5t2'

    # <p class="css-35ezg3" is the key, ex) -> Fuel Economy
    # <p> that follows is the value

    return outermap
# ----------------------
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
            writer.writerow(['year', 'make', 'model', 'body_style(s)', 'image_source(s)', 'recall(s)'])
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
                ''' we have a 'reader obj', and a 'writer' obj that we instantiated inside here '''
                # p = multiprocessing.Process(target=row_operations, args=(row, writer))
                # jobs.append(p)
                # p.start()
                row_operations(row, writer)
                # # We need to retrieve the list of recalls
                # recalls = getRecalls(row[0], row[1], row[2])
                # # Write what we already have + newly retrieved recalls item
                # writer.writerow([row[0], row[1], row[2], row[3], row[4], recalls])
            # After row object completes
            # bunches contains our data

        return None
# ----------------------
def createOldPath(year):
    return 'master_data/'+str(year)+'.csv'
# ----------------------
def createNewPath(year):
    return str(year)+'.csv'
# all info boxes are <div> tags with class = css-130z0y1-StyledBox-default emf8dez0
# url = 'https://www.kbb.com/bmw/3-series/1992/'
# getSoup(url)
