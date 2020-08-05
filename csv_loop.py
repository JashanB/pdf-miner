# Loop through base_path
# csv path - C:\automate\attachment_list\incoming
# pdf path C:\automate\attachment\archive\BULOVA\2020\07
# Loop through csvs - grab filename, look in pdf directory for file to process 
# need to access vendor name
# ----- Build loops -------
# csv_path = C:\automate\attachment_list\incoming
# for vendor in csv_path
# for csv in vendor
# loop through csv - rows and columns - use hard coded index values 
# set path to access example
import csv
import os
with open('./test_csv_1.csv', 'r') as file:
  reader = csv.reader(file)
  for row in reader: 
    print("-----ROW-----")
    print(row)
    for index, column in enumerate(row):
      print("----Column----")
      print(f'column index: {index}' + column + "\n" + "test")

# csv_directory = './csvs'
# for csv in os.listdir(csv_directory):
#   print(csv)