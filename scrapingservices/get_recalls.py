import requests, json, csv, multiprocessing
import get_images
# try global list
# bunches = []
def sanitizeModelInput(model):
    ''' this will suffice for now, on next pass generate list of keywords and search string for keywords '''
    model = model.replace('&', '')
    model = model.replace('/', '')

    temp = list(model.split(" "))
    if len(temp) > 1 and temp[0].isdigit() is False:
        model = temp[0]

    return model
# ----------------------
def getRecalls(year, make, model):
    # print(model)

    model = sanitizeModelInput(model)
    print(model)
    # model = model.replace('  ', ' ')
    # print(model)

    url = 'https://one.nhtsa.gov/webapi/api/Recalls/vehicle/modelyear/'+year+'/make/'+make+'/model/'+model+'?format=json'
    # print(url)
    header = get_images.getHeader()
    response = requests.get(url, headers=header)
    empty = []
    print('STATUS CODE:' + str(response.status_code))
    if response.status_code is 200:
        response = response.json()
        if response['Count'] is 0:
            return empty
        else:
            return response['Results']
    else:
        return empty
# ----------------------
def row_operations(row, writer_object):
    print('Beginning row operations for '+row[0]+' '+row[1]+' '+row[2])
    # We need to retrieve the list of recalls
    recalls = getRecalls(row[0], row[1], row[2])

    # bunches.append(recalls)
    # print recalls
    # print(recalls)

    # Write what we already have + newly retrieved recalls item
    writer_object.writerow([row[0], row[1], row[2], row[3], row[4], recalls])

    print('Finished row operations for '+row[0]+' '+row[1]+' '+row[2])
    return None
# ----------------------
def handleFilesForRecalls(oldFilePath, newFilePath):
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
    return 'KBB_data/'+str(year)+'.csv'
# ----------------------
def createNewPath(year):
    return str(year)+'.csv'
# ----------------------
count = 1992
while count <= 2020:
    old = createOldPath(count)
    new = createNewPath(count)
    print('Currently working on: ' +new)
    handleFilesForRecalls(old, new)
    print('Finished: '+new)

    count += 1
