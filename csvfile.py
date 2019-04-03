from SI507_project4 import *
import csv



outfile = open('national_parks.csv','w',encoding='utf-8')
outfile.write('Name,Type,Description,Location')
outfile.write('\n')
for list in all_list:
    row_str = '{},{},{},{}'.format(list[0],list[1],list[2].replace('\n',' ').replace(',',' '),list[3].replace(',',' '))
    outfile.write(row_str)
    outfile.write('\n')
outfile.close()
