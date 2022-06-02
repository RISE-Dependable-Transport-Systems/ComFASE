
import atexit
import logging
import os
import signal
import subprocess
import sys
import numpy
from datetime import datetime, date, time
import pandas as pd
# LISTS TO LOG ATTACK INJECTION DATA
ID_list = []             # EXPERIMENT ID
start_list = []          # ATTACK START/ACTIVATION TIME
end_list = []            # ATTACK END TIME
Step_list = []           # THE NUMBER OF EXPERIMENT WHEN TARGETING THE TIME STEPS
V_list = []              # INJECTED PD VALUES
Ex_ID = 0
Node=27  		         # NODE/VEHICLE UNDER ATTACK
Activation='true'	     # BOOLEAN FOR ATTACK ACTIVATION
Delay='true'	         # BOOLEAN FOR DELAY
Sender='true'   	     # BOOLEAN FOR TARGET SURFACE FOR SENDER
Receiver='true' 	     # BOOLEAN FOR TARGET SURFACE FOR RECEIVER
for t in numpy.arange(12.0, 17.05, 0.5):  # This loop defines the target time to inject attack
    step = 0
    pd_values = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0] # LIST OF VALUES FOR THE PD PARAMETER
    for v_pd in pd_values : #numpy.arange(0.1, 3.1, 0.1):  # v is faulty value, this loop defines the target range
        t_end= t
        while t_end < t+11.0:
            t_end+=1
            Ex_ID += 1
            step += 1
            ID_list.append(Ex_ID)
            start_list.append(t)
            end_list.append(t_end)
            Step_list.append(step)
            V_list.append(v_pd)
            #t_end = t+60   # For Transient Faults
            print('Ex_ID = ', Ex_ID,
                  '\n\n=============================================================\n================================================================================\n')
            os.system(
                './run -u Cmdenv -c SinusoidalNoGui -r 2 --*.attacker.DelayAttack=%s --*.attacker.attackStartTime=${attackStartTime=%s}s '
                '--*.attacker.attackEndTime=${attackEndTime=%s}s --*.attacker.myPDValue=${myPDValue=%s}s --*.attacker.attackNode=%s '
                '--*.attacker.attackActive=%s --*.attacker.attackOnSender=%s '
                '--*.attacker.attackOnReceiver=%s' %(Delay, t, t_end, v_pd, Node, Activation, Sender, Receiver))


# Record data in csv file===============================================================================================


df = pd.DataFrame(
    {
        'Ex ID': ID_list,
        'Start time': start_list,
        'End time': end_list,
        'Number': Step_list,
        'Value': V_list
    }
)
# Extracting the current Time ==========================================================================================
now = datetime.now()
current_time = now.strftime("%Y-%m-%d %H.%M.%S")
df.to_csv("Node_1 controller_2 attackON_senderANDreceiver-3cycles 12-17 table_{}.csv".format(current_time))

'''
print("Current Time =", now)

for t in numpy.arange (10.0, 20.0, 0.5): # this loop defines the target time to inject attack
    for v_pd in numpy.arange (0.1, 3.0, 0.1): # v is faulty value, this loop defines the target range
        for i in range(0, 6, 1): # i is the controller number
            print('i= ', i,
                  '\n\n=============================================================\n================================================================================\n')
            scenario = ['SinusoidalNoGui', 'BrakingNoGui', 'SimpleNoGui']
            controller = [0, 1, 2, 3, 4, 5] # "0:ACC", "1:ACC", "2:CACC", "3:PLOEG", "4:CONSENSUS", "5:FLATBED"  
            parameters = ["--*.**.nic.phy80211p.attackTime = ${attackTime = 20}s", "-- *.**.nic.phy80211p.myPropagationDelay = ${myPropagationDelay = 2}s"]
            #parameters[0] = "-- *.**.nic.phy80211p.attackTime = ${attackTime = 20}s"
            #parameters[1] = "-- *.**.nic.phy80211p.myPropagationDelay = ${myPropagationDelay = 2}s"
            #os.system('./run -u Cmdenv -c %s -r %s %s' %(scenario[0], str(controller[2]), parameters[0]))
            os.system('./run -u Cmdenv -c {} -r {} {}' .format(scenario[0], str(controller[2]), parameters[0]))
            #os.system('./run -u Cmdenv -c SinusoidalNoGui -r %s' % i)


'''
