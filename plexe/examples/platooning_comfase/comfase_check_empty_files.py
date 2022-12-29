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
'''
#==================================================================================#
#                               Parse Golden Run                                   #
#==================================================================================#
DecelListG_0 = []
DecelListG_1 = []
DecelListG_2 = []
DecelListG_3 = []
for file in file_GoldenRun:
    # ========================================== Reads the XML file ================
    root = ET.parse(file).getroot()
    for X in root.findall('timestep'):#Inside xml file goes to(timestep-> vehicle)then whatever I want I pick from there
        timee = float(X.get("time"))
#        if timee>=11.00:
        for B in X.findall('vehicle'):
            id = B.get("id")
            if id == "vtypeauto.0":
                value = B.get('acceleration')
                DecelListG_0.append(float(value))
            elif id == "vtypeauto.1":
                value = B.get('acceleration')
                DecelListG_1.append(float(value))
            elif id == "vtypeauto.2":
                value = B.get('acceleration')
                DecelListG_2.append(float(value))
            elif id == "vtypeauto.3":
                value = B.get('acceleration')
                DecelListG_3.append(float(value))
#==================================================================================#
#                               Parse Faulty Run                                   #
#==================================================================================#
# Lists to record vehicles deceleration separately =====================================================================
Accel_0_max = []
Decel_0_min = []
Accel_1_max = []
Decel_1_min = []
Accel_2_max = []
Decel_2_min = []
Accel_3_max = []
Decel_3_min = []

ImpactStatus = []
ID_list = [] # Experiment ID list
k = 0  # Experiment ID
for file in file_list:
    k += 1  # counts the Experiment ID
    ID_list.append(k)
    print("Experiment_ID = ", k, "***************\n\n")
    # ========================================== Reads the XML file ====================================================
    root = ET.parse(file).getroot()
    DecelList_0 = []
    DecelList_1 = []
    DecelList_2 = []
    DecelList_3 = []


    for X in root.findall('timestep'):#Inside xml file goes to(timestep-> vehicle)then whatever I want I pick from there
        timee = float(X.get("time"))
#        if timee>=11.00:
        for B in X.findall('vehicle'):
            id = B.get("id")
            if id == "vtypeauto.0":
                value = B.get('acceleration')
                DecelList_0.append(float(value))
            elif id == "vtypeauto.1":
                value = B.get('acceleration')
                DecelList_1.append(float(value))
            elif id == "vtypeauto.2":
                value = B.get('acceleration')
                DecelList_2.append(float(value))
            elif id == "vtypeauto.3":
                value = B.get('acceleration')
                DecelList_3.append(float(value))

    Accel_0_max.append(max(DecelList_0))
    Decel_0_min.append(min(DecelList_0))
    Accel_1_max.append(max(DecelList_1))
    Decel_1_min.append(min(DecelList_1))
    Accel_2_max.append(max(DecelList_2))
    Decel_2_min.append(min(DecelList_2))
    Accel_3_max.append(max(DecelList_3))
    Decel_3_min.append(min(DecelList_3))
    if DecelList_0==DecelListG_0 and DecelList_1==DecelListG_1 and DecelList_2==DecelListG_2 and DecelList_3==DecelListG_3:
        ImpactStatus.append('Non-effective')
    else:
        ImpactStatus.append('Effective')

print("Accel Max 1 = ", Accel_1_max)
print("Decel Min 1 = ", Decel_1_min)
# *********************************************************************************
collision_state = []
collider_list = []
collision_time = []
kk = 0  # Experiment ID
for file in file_list_collision:
    collision_l = []
    collider_l = []
    collision_t = []
    kk += 1  # counts the Experiment ID
    print("Experiment_ID = ", kk, "***************\n\n")
    # ========================================== Reads the XML file ====================================================
    root_collision = ET.parse(file).getroot()


    for X in root_collision.findall('collision'):
        state = X.get("type")
        c_time = X.get("time")
        collider = X.get("collider")
        collision_l.append(state)
        collision_t.append(c_time)
        collider_l.append(collider)   
        #print('collision_l= ', collision_l )
        #print('collider_l= ', collider_l)
        break
    if len(collision_l) == 0:
        collision_state.append("No")
        collision_time.append("No")
        collider_list.append("No") 
    else:
        collision_state.append(collision_l[0])
        collision_time.append(collision_t[0])
        collider_list.append(collider_l[0])

print("Collision state = ", collision_l)
print("Collision time = ", collision_t)
# ************************************************************************************

# Read csv file to extract the fault injection time and the lc.Assertive value =========================================
f = open('ComFASE Attack Injection Campaign Log _2022-03-02 02.54.05.csv', 'r')
readCSV = csv.reader(f)
startTime = []
endTime = []
value = []
next(readCSV)
for row in readCSV:
    startTime.append(float(row[2]))
    endTime.append(float(row[3]))
    value.append(float(row[5]))

# ================================================Save in CSV file =====================================================
df_7 = pd.DataFrame(
        {
            'Ex ID'     : ID_list,
            'Start_time': startTime,
            'End_time': endTime,
            'PD_value'  : value,
            'Impact_status': ImpactStatus,
            'Collision_state': collision_state,
            'Collision time': collision_time,
            'collider'  : collider_list,
            'Accel_0_max': Accel_0_max,
            'Dcel_0_min': Decel_0_min,
            'Accel_1_max': Accel_1_max,
            'Dcel_1_min': Decel_1_min,
            'Accel_2_max': Accel_2_max,
            'Dcel_2_min': Decel_2_min,
            'Accel_3_max': Accel_3_max,
            'Dcel_3_min': Decel_3_min
                }
        )

now = datetime.now() # Current time extraction =========================================================================
current_time = now.strftime("%Y-%m-%d %H.%M.%S")
df_7.to_csv("Parsed Accel-Deceleration_All Vehicles_{} ParsedData.csv".format(current_time))

'''
