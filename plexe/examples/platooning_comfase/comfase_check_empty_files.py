import xml.etree.ElementTree as ET
import re
import glob
import csv
from datetime import datetime, date, time
import pandas as pd
import os

file_GoldenRun = sorted(glob.glob("GoldenRun_braking/*fcd-output.xml*")) #Reads all xml file with the end name of fcd.xml and makes a list of their name
file_list = sorted(glob.glob("sumocfg/*fcd-output.xml*")) #Reads all xml file with the end name of fcd.xml and makes a list of their name
file_list_collision = sorted(glob.glob("sumocfg/*collision-output.xml*")) #Reads all xml file with the end name of fcd.xml and makes a list of their name
print("FCD Golden= ", len(file_GoldenRun))
print("FCD files= ", len(file_list))
print("COLLISION files= ", len(file_list_collision))
print("FCD files= ", file_list)


import os


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        bb = file_info.st_size
        bb /= 1024.0
        bb /= 1024.0
        return bb #convert_bytes(file_info.st_size)


# Lets check the file size of MS Paint exe
# or you can use any file path
# file_path = r"C:\Windows\System32\mspaint.exe"
# print(file_size(file_path))
Ex_Nr=0 #40000
Ex_list = []
for ii in file_list:
    Ex_Nr += 1
    if file_size(ii)< 1:
    # if Ex_Nr == 17611:
        print('EX ID= ', Ex_Nr, 'size is: ', file_size(ii))
        print('file name= ', ii)
        Ex_list.append(Ex_Nr)
# ************************************************************************************
print('\n\n ********************************************************************\n')
# Read csv file to extract the fault injection time and the lc.Assertive value =========================================
f = open('ComFASE Attack Injection Campaign Log _2022-10-27 04.46.40.csv', 'r')
readCSV = csv.reader(f)
startTime = []
endTime = []
value = []
next(readCSV)
empty_list = [23635, 42382]
row_Nr = 0
for row in readCSV:
    row_Nr += 1
    if float(row[1]) in empty_list:
        print('Ex_ID= ', row[1])
        print('start time= ', float(row[2]))
        print('end time= ', float(row[3]))
        print('value= ', float(row[5]), '\n----------------------------------------')

