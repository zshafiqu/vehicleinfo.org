import requests, json, csv
# ----------------------
def getRecalls(year, make, model):
    url = 'https://one.nhtsa.gov/webapi/api/Recalls/vehicle/modelyear/'+year+'/make/'+make+'/model/'+model+'?format=json'
    items = requests.get(url).json()

    # for item in items['Results']:
    #     print(item)
    # print( str(items['Results']) )
    # print(items)
    return str(items['Results'])

# ----------------------
# def handleFilesForRecalls(oldFile, newFile):
#
#
#
# # ----------------------
# getRecalls('2002', 'acura','mdx')
