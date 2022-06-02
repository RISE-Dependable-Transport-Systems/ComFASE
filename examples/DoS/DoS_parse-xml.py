import xml.etree.ElementTree as ET
import re
import glob
import csv
from datetime import datetime, date, time
import pandas as pd

file_list = sorted(glob.glob("sumocfg/*fcd-output.xml*")) #Reads all xml file with the end name of fcd.xml and makes a list of their name
file_list_collision = sorted(glob.glob("sumocfg/*collision-output.xml*")) #Reads all xml file with the end name of fcd.xml and makes a list of their name
print("FCD files= ", len(file_list))
print("COLLISION files= ", len(file_list_collision))
print("FCD files= ", file_list)
# Lists to record vehicles deceleration separately =====================================================================
Accel_0_max = []
Decel_0_min = []
Accel_1_max = []
Decel_1_min = []
Accel_2_max = []
Decel_2_min = []
Accel_3_max = []
Decel_3_min = []

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

print("Accel Max 1 = ", Accel_1_max)
print("Decel Min 1 = ", Decel_1_min)
# *********************************************************************************
collision_state = []
collider_list = []
kk = 0  # Experiment ID
for file in file_list_collision:
    collision_l = []
    collider_l = []
    kk += 1  # counts the Experiment ID
    print("Experiment_ID = ", kk, "***************\n\n")
    # ========================================== Reads the XML file ====================================================
    root_collision = ET.parse(file).getroot()


    for X in root_collision.findall('collision'):
        state = X.get("type")
        collider = X.get("collider")
        collision_l.append(state)
        collider_l.append(collider)   
        #print('collision_l= ', collision_l )
        #print('collider_l= ', collider_l)
        break
    if len(collision_l) == 0:
        collision_state.append("No")    
        collider_list.append("No") 
    else:
        collision_state.append(collision_l[0])
        collider_list.append(collider_l[0])    

print("Collision state = ", collision_state)
print("Collider = ", collider_list)
# ************************************************************************************

# Read csv file to extract the fault injection time and the lc.Assertive value =========================================
f = open('Node_1 controller_2 attackON_senderANDreceiver-DoS table_2021-08-25 10.26.43.csv', 'r')
readCSV = csv.reader(f)
startTime = []
endTime = []
value = []
next(readCSV)
for row in readCSV:
    startTime.append(float(row[2]))
    #endTime.append(float(row[3]))
    value.append(float(row[4]))

# ================================================Save in CSV file =====================================================
df_7 = pd.DataFrame(
        {
            'Ex ID'     : ID_list,
            'Start_time': startTime,
            #'End_time': endTime,
            'PD_value'  : value,
            'Collision_state': collision_state,
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


