from bs4 import BeautifulSoup, SoupStrainer
import requests, json, os, mysql.connector, csv, ast, random
import images
# ----------------------
def getSoup(url):
    # Entered getSoup method
    print('About to make request for data')
    i = 0

    # Continually try to make this request until its successful
    while True:
        if i is 15:
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
            i += 1
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

    i = 0
    while i < len(attributes)


    for attribute in attributes:
        print(attribute)
        print('\n')

    # All style headings within h3 tags with class = 'css-lg2ecn-StyledHeading3-defaultStyles-h3 e1jv8h5t2'

    # <p class="css-35ezg3" is the key, ex) -> Fuel Economy
    # <p> that follows is the value

    return None
# ----------------------
# all info boxes are <div> tags with class = css-130z0y1-StyledBox-default emf8dez0
url = 'https://www.kbb.com/acura/integra/1992/?bodystyle=sedan'
getSoup(url)
