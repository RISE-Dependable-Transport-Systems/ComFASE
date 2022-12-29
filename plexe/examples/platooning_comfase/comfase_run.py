##############################################################################################
# **************      ComFASE: Campaign configuration and execution             **************
##############################################################################################
import os
import subprocess
import sys
import numpy
from datetime import datetime, date, time
import pandas as pd
import xml.etree.ElementTree as ET

##############################################################################################
# ****************       Function for Attack Injection Run and Output Log         ************
##############################################################################################
def ComFASE_experiment_run(scenario, controller, attackModelName, attackInitiationTime, endTime,
                                                 attackValue, attackOnSender, attackOnReceiver):
    if attackModelName == "Delay":
        os.system(
            './run -u Cmdenv -c %s -r %s '
            '--*.comfase.delayAttack=%s '
            '--*.comfase.attackStartTime=%ss '
            '--*.comfase.attackEndTime=%ss '
            '--*.comfase.injectedPDValue=%ss '
            '--*.comfase.attackOnSender=%s '
            '--*.comfase.attackOnReceiver=%s'
            % (scenario, controller, "true", attackInitiationTime, endTime, attackValue, attackOnSender, attackOnReceiver))
    elif attackModelName == "DoS":
        os.system(
            './run -u Cmdenv -c %s -r %s '
            '--*.comfase.DoSAttack=%s '
            '--*.comfase.attackStartTime=%ss '
            '--*.comfase.injectedPDforDoS=%ss '
            '--*.comfase.attackOnSender=%s '
            '--*.comfase.attackOnReceiver=%s'
            % (scenario, controller, "true", attackInitiationTime, attackValue, attackOnSender, attackOnReceiver))
    elif attackModelName == "Destructive_interference":
        os.system(
            './run -u Cmdenv -c %s -r %s '
            '--*.comfase.destructiveInterferenceAttack=%s '
            '--*.comfase.attackStartTime=%ss '
            '--*.comfase.attackEndTime=%ss '
            '--*.comfase.injectedDestructiveness=%smW '
            '--*.comfase.attackOnSender=%s '
            '--*.comfase.attackOnReceiver=%s'
            % (scenario, controller, "true", attackInitiationTime, endTime, attackValue, attackOnSender, attackOnReceiver))
    if attackModelName == "Barrage_jamming":
        os.system(
            './run -u Cmdenv -c %s -r %s '
            '--*.comfase.barrageJammingAttack=%s '
            '--*.comfase.attackStartTime=%ss '
            '--*.comfase.attackEndTime=%ss '
            '--*.comfase.injectedNoiseValue=%smW '
            '--*.comfase.attackOnSender=%s '
            '--*.comfase.attackOnReceiver=%s'
            % (scenario, controller, "true", attackInitiationTime, endTime, attackValue, attackOnSender, attackOnReceiver))
    if attackModelName == "Deceptive_jamming":
        os.system(
            './run -u Cmdenv -c %s -r %s '
            '--*.comfase.deceptiveJammingAttack=%s '
            '--*.comfase.attackStartTime=%ss '
            '--*.comfase.attackEndTime=%ss '
            '--*.comfase.injectedInterferenceValue=%smW '
            '--*.comfase.attackOnSender=%s '
            '--*.comfase.attackOnReceiver=%s'
            % (scenario, controller, "true", attackInitiationTime, endTime, attackValue, attackOnSender, attackOnReceiver))


##############################################################################################
# *************                Attack Injection Campaign Config                ***************
##############################################################################################
configurationFile = ET.parse('configure_campaign.xml').getroot()
# LISTS TO LOG ATTACK INJECTION DATA
LIST_Ex_Nr = []                     # EXPERIMENT ID
LIST_Initiation_time = []            # ATTACK START/ACTIVATION TIME
LIST_End_time = []                  # ATTACK END TIME
LIST_Step_number = []               # THE NUMBER OF EXPERIMENT WHEN TARGETING THE TIME STEPS
LIST_Injected_value = []            # INJECTED PD VALUES
LIST_Run_status = []
Ex_Nr = 0                        # Number of experiment (Ex_Nr)
def config(attackModelName):
    attackModel = configurationFile.find(str(attackModelName))
    #delayAttack = str(delayAttackSetup.get("delayAttack"))
    attackInitiationStartTime = float(attackModel.get("attackInitiationStartTime"))
    attackInitiationEndTime = float(attackModel.get("attackInitiationEndTime"))
    attackInitiationTimeStep = float(attackModel.get("attackInitiationTimeStep"))
    attackStartValue = float(attackModel.get("attackStartValue"))
    attackEndValue = float(attackModel.get("attackEndValue"))
    attackValueStep = float(attackModel.get("attackValueStep"))
    attackMinDuration = float(attackModel.get("attackMinDuration"))
    attackMaxDuration = float(attackModel.get("attackMaxDuration"))
    attackDurationStep = float(attackModel.get("attackDurationStep"))
    attackOnSender = str(attackModel.get("attackOnSender"))
    attackOnReceiver = str(attackModel.get("attackOnReceiver"))
    ################# Scenario setup ##############
    scenarioType = configurationFile.find(str("Scenario_type"))
    scenario = str(scenarioType.get("Scenario"))
    controller = int(scenarioType.get("Controller"))
    Ex_Nr = 0
    if attackModelName != "DoS":
        for attackInitiationTime in numpy.arange(attackInitiationStartTime, attackInitiationEndTime, attackInitiationTimeStep):  # This loop defines the target time to inject attack
            attackInitiationTime = round(attackInitiationTime, 2)
            Step_number = 0 # Counts the step of the experiment
            for attackValue in numpy.arange(attackStartValue, attackEndValue, attackValueStep):# Injected_value is a faulty value, this loop defines the target range
                attackValue = round(attackValue, 8)
                for attackDuration in numpy.arange(attackMinDuration, attackMaxDuration, attackDurationStep):
                    endTime = attackInitiationTime + attackDuration
                    Ex_Nr += 1
                    Step_number += 1
                    LIST_Ex_Nr.append(Ex_Nr)
                    LIST_Initiation_time.append(attackInitiationTime)
                    LIST_End_time.append(endTime)
                    LIST_Step_number.append(Step_number)
                    LIST_Injected_value.append(attackValue)
                    print('\n\nEx_Number = ', Ex_Nr,
                          '\n\n============================================================='
                          '\n================================================================\n')
                    try:
                        ComFASE_experiment_run(scenario, controller, attackModelName, attackInitiationTime, endTime,
                                                     attackValue, attackOnSender, attackOnReceiver)
                        LIST_Run_status.append('Successful')
                    except Exception as err:
                        print("Something went wrong")
                        ##traci.close(False)
                        LIST_Run_status.append('Failed')
    elif attackModelName == "DoS":
        for attackInitiationTime in numpy.arange(attackInitiationStartTime, attackInitiationEndTime, attackInitiationTimeStep):  # This loop defines the target time to inject attack
            attackInitiationTime = round(attackInitiationTime, 2)
            Step_number = 0 # Counts the step of the experiment
            attackValue = round(attackStartValue, 8)
            endTime = 2000000
            Ex_Nr += 1
            Step_number += 1
            LIST_Ex_Nr.append(Ex_Nr)
            LIST_Initiation_time.append(attackInitiationTime)
            LIST_End_time.append(endTime)
            LIST_Step_number.append(Step_number)
            LIST_Injected_value.append(attackValue)
            print('\n\nEx_Number = ', Ex_Nr,
                  '\n\n============================================================='
                  '\n================================================================\n')
            try:
                ComFASE_experiment_run(scenario, controller, attackModelName, attackInitiationTime, endTime,
                                             attackValue, attackOnSender, attackOnReceiver)
                LIST_Run_status.append('Successful')
            except Exception as err:
                print("Something went wrong")
                ##traci.close(False)
                LIST_Run_status.append('Failed')

##############################################################################################
# *************        Function for Attack Injection Campaign Data Log         ***************
##############################################################################################
def ComFASE_compaign_data_log():
    # Record data in a csv file
    df = pd.DataFrame(
        {
            'Ex Number': LIST_Ex_Nr,
            'Initiation_time': LIST_Initiation_time,
            'End_time': LIST_End_time,
            'Step_number': LIST_Step_number,
            'Injected_value': LIST_Injected_value,
            'Run_status': LIST_Run_status
        }
    )
    # Current Time
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H.%M.%S")
    df.to_csv("ComFASE Attack Injection Campaign Log _{}.csv".format(current_time))
    print("Current Time =", now)
##############################################################################################
# *************                         Main Function                          ***************
##############################################################################################
if __name__ == "__main__":
  # time.sleep(8)
  # make sure params are in a good state
  configurationFile = ET.parse('configure_campaign.xml').getroot()
  attackModel = configurationFile.find('Attack_type')
  if attackModel.get("Delay") == 'true':
      attackModelName = "Delay"
      print('Delay attack: ', attackModelName)
      config(attackModelName)
  elif attackModel.get("DoS") == 'true':
      attackModelName = "DoS"
      config(attackModelName)
  elif attackModel.get("Destructive_interference") == 'true':
      attackModelName = "Destructive_interference"
      config(attackModelName)
  elif attackModel.get("Barrage_jamming") == 'true':
      attackModelName = "Barrage_jamming"
      config(attackModelName)
  elif attackModel.get("Deceptive_jamming") == 'true':
      attackModelName = "Deceptive_jamming"
      config(attackModelName)
  else:
      print('\n\n------------------- Select an attack model in xml file')
  # Log the fault injection campaign data
  ComFASE_compaign_data_log()