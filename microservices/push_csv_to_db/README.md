# Push CSVs to our Database
> This folder contains the code and entry points needed to push all the CSV files to our remote database.

## HOW TO UPDATE THE DATABASE :
- All you need to do is make a copy of the master_data that contains the data you'd like to push.

- Run the script, 'migrate_csv_to_database.py', and it'll prompt you to enter a range on year's you'd like to update

- For each year, the script will create a table with the following scheme: (All values are of TEXT datatype)

### --------------------------------------------------------------------
### ID | Year | Make | Model | Body-Styles | Trim-Data | Images-Sources
### --------------------------------------------------------------------

## SPECIAL NOTES :
- Database credentials are stored within OS variables in shell.
