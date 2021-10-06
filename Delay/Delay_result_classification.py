import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import re
import glob
import csv
from datetime import datetime, date, time
import pandas as pd




# Read csv file to extract the fault injection time and the PD value =========================================
f = open('Parsed Accel-Deceleration_All Vehicles_2021-08-27 10.27.11 ParsedData.csv', 'r')
readCSV = csv.reader(f)
neg_time=[]
neg_duration=[]
neg_value=[]
benign_time=[]
benign_duration=[]
benign_value=[]
severe_time=[]
severe_duration=[]
severe_value=[]
TTC = []
Time = []
value = []
ID = []
next(readCSV)
for row in readCSV:
    ID.append(float(row[1]))
    if row[5] =='collision':
       severe_time.append(float(row[2]))
       severe_duration.append(float(row[3])-float(row[2]))
       severe_value.append(float(row[4]))
       TTC.append(float(row[6]) - float(row[2]))
       # include the car number here
    else:
         decel_list = [float(row[9]), float(row[11]), float(row[13]), float(row[15])]
         decel_min = abs(min(decel_list))
         if decel_min <= 1.53:
            neg_time.append(float(row[2]))
            neg_duration.append(float(row[3])-float(row[2]))
            neg_value.append(float(row[4]))
         elif decel_min <=4.50 and decel_min > 1.53:
            benign_time.append(float(row[2]))
            benign_duration.append(float(row[3])-float(row[2]))
            benign_value.append(float(row[4]))

print('TTCmax= ', max(TTC), '    TTCmin= ', min(TTC))
print('Total= ', len(ID), 'Number of Negligible= ', len(neg_time), ' Benign= ', len(benign_time), 'Severe= ', len(severe_time))
fig = plt.figure()
ax = plt.axes(projection='3d')
#ax.scatter3D(non_time, non_value, non_duration, color='black')
ax.scatter3D(neg_time, neg_value, neg_duration, color='green')
ax.scatter3D(benign_time, benign_value, benign_duration, color='blue')
ax.scatter3D(severe_time, severe_value, severe_duration, color='red')
ax.set_xlabel('Injection Time (S)', fontsize='10')
ax.set_ylabel('PD Value (S)', fontsize='10')
ax.set_zlabel('Duration (S)', fontsize='10')
# ax.view_init(60, 35)
plt.title('Controller 2 (CACC) - Sender & Receiver - Propagation Delay')
plt.legend(['Negligible', 'Benign', 'Severe'], loc='upper left', bbox_to_anchor=(0.925, 0.5), prop={"size":10})
plt.show()


'''
short_time=[]
short_duration=[]
short_value=[]
med_time=[]
med_duration=[]
med_value=[]
long_time=[]
long_duration=[]
long_value=[]
for t in range (0, len(TTC), 1):
    if TTC[t] <= 3.0:
        short_time.append(float(severe_time[t]))
        short_value.append(float(severe_value[t]))
        short_duration.append(float(severe_duration[t]))
    elif TTC[t] > 3.0 and TTC[t] <= 10:
        med_time.append(float(severe_time[t]))
        med_value.append(float(severe_value[t]))
        med_duration.append(float(severe_duration[t]))
    elif TTC[t] > 10:
        long_time.append(float(severe_time[t]))
        long_value.append(float(severe_value[t]))
        long_duration.append(float(severe_duration[t]))
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(long_time, long_value, long_duration, color='green')
ax.scatter3D(med_time, med_value, med_duration, color='blue')
ax.scatter3D(short_time, short_value, short_duration, color='red')
ax.set_xlabel('Injection Time (S)', fontsize='10')
ax.set_ylabel('PD Value (S)', fontsize='10')
ax.set_zlabel('Duration (S)', fontsize='10')
# ax.view_init(60, 35)
plt.title('Controller 2 (CACC) - Sender & Receiver - Propagation Delay')
plt.legend([ 'Long', 'Medium', 'Short'], loc='upper left', bbox_to_anchor=(0.925, 0.5), prop={"size":10})
plt.show()
#########################################
plt.plot(neg_time, neg_value, '*g', linewidth=1)
plt.plot(benign_time, benign_value, '*b', linewidth=1)
plt.plot(severe_time, severe_value, '*r', linewidth=1)
plt.xlabel('Time (S)', fontsize='10')
plt.ylabel('PD Value (S)', fontsize='10')
#plt.zlabel('Duration (S)', fontsize='10')
plt.legend(['Negligible', 'Benign', 'Severe'], loc='center left', bbox_to_anchor=(0.925, 0.5), prop={"size":10})
# plt.grid()
plt.gcf().autofmt_xdate()
#plt.xticks([12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0])
x_ticks = np.arange(12, 17.1, 0.2)
#plt.xticks(x_ticks)
y_ticks = np.arange(0.1, 3.1, 0.2)
#plt.yticks(y_ticks)
#plt.title('Max Brake Deceleration ', fontsize='10')
plt.title('Controller 2 (CACC) - Receiver - Propagation Delay')
plt.show()
'''
