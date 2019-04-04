from SI507_project4 import *
import csv

csvfile = open('national_parks.csv','w',newline='',encoding='utf-8')
header = ('Name','Type','Description','Location')
row_writer = csv.writer(csvfile)
row_writer.writerow(header)

for list in all_list:
    row_writer.writerow(list)

csvfile.close()
