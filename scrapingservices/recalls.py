import requests, json, csv
# try global list
# bunches = []
# ----------------------
def getRecalls(year, make, model):
    if "&" in model:
        model.replace('&', '')

    url = 'https://one.nhtsa.gov/webapi/api/Recalls/vehicle/modelyear/'+year+'/make/'+make+'/model/'+model+'?format=json'
    items = requests.get(url).json()
    empty = []

    if items['Count'] is 0:
        return empty
    else:
        return items['Results']
# ----------------------
def row_operations(row, writer_object):
    print('Beginning row operations for '+row[0]+' '+row[1]+' '+row[2])
    # We need to retrieve the list of recalls
    recalls = getRecalls(row[0], row[1], row[2])

    # print recalls
    print(recalls)

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
                # p = multiprocessing.Process(target=row_operations, args=(row,))
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
old = createOldPath(1992)
new = createNewPath(1992)
handleFilesForRecalls(old, new)
# for recall in bunches:
    # print (recall)
# print(len(bunches))
