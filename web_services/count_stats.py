import csv
# ----------------------
''' Script to count things like - unique vehicles, makes, models, etc '''
# Global counter
count = 0
makes = set()
# ----------------------
def file_pathify(year):
    # Return file path for given year
    return 'master_data/'+str(year)+'.csv'
# ----------------------
def read_file(filename):

    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)
        # id = 0

        for row in reader:
            count += 1 # increase count of unique vehicles
            makes.add(str(row[1])) # add makes to set (unique values only)
# ----------------------
min = 1992
max = 2020

while min <= max:
    name = file_pathify(min)
    read_file(name)
    min += 1

# ----------------------
# at the end of the script, print num of vehicles & num of unique makes
print('Total number of cars is: ')
print(count)
print('Total number of unique manufacters')
print(len(makes))
