import pandas as pd
import numpy
import numpy as np
import random
import csv
import os
from matplotlib import pyplot as plt
import seaborn as sns
from pathlib import Path

def main(fileName1 = None, fileName2=None, expTypeName = "", attackInitiationStartTime = 20, attackInitiationEndTime = 22.5, attackInitiationTimeStep = 0.2, attackStartValue = 0.2, attackEndValue = 1.01, attackValueStep = 0.2):

    plt.rcParams['figure.figsize'] = 16, 7
    import warnings
    warnings.filterwarnings('ignore')
    #==================================================================================#
    #                     Read parsed data for attack campaign                         #
    #==================================================================================#
    # Data Analysis (DA): pd.read_csv('please correct the address accordingly')
    if fileName2!= None:
        DA = pd.read_csv(fileName2)
    else:
        DA = pd.read_csv('Parsed Accel-Deceleration_All Vehicles_2024-09-23 13.10.44 ParsedData.csv')
    DA.info()
    DA['AttackDuration'] = round(DA['End_time'] - DA['Start_time'] , 2)
    DA['Categories'] = DA['Collision_state']
    DA['Categories'] = 'NAN'
    DA['Affected_car'] = DA['collider']
    DA['Affected_car'] = 'NAN'
    #######################################
    # Renaming the car names from vtypeauto to Car:
    for index, col in DA.iterrows():
        if DA['collider'][index] == 'vtypeauto.0':
            DA['collider'][index] = 'Car 1'
        elif DA['collider'][index] == 'vtypeauto.1':
            DA['collider'][index] = 'Car 2'
        elif DA['collider'][index] == 'vtypeauto.2':
            DA['collider'][index] = 'Car 3'
        elif DA['collider'][index] == 'vtypeauto.3':
            DA['collider'][index] = 'Car 4'
    #==================================================================================#
    #    Result classification based on Acceleration Profile and Collisions            #
    #==================================================================================#
    Non_effective = 0
    for index, col in DA.iterrows():
        if DA['Impact_status'][index] == 'Non-effective':
            DA['Categories'][index] = 'Non_effective'
            Non_effective +=1
        elif DA['Collision_state'][index] == 'collision':
            DA['Categories'][index] = 'Severe_collision'
            # DA['Categories'][index] = 'Severe'
            DA['Affected_car'][index] = DA['collider'][index]
        else:
            decel_list = [DA['Dcel_0_min'][index], DA['Dcel_1_min'][index], DA['Dcel_2_min'][index], DA['Dcel_3_min'][index]]
            decel_min = abs(min(decel_list))
            car_list = ['Car 1', 'Car 2', 'Car 3', 'Car 4']
            car_id = decel_list.index(min(decel_list))
            DA['Affected_car'][index] = car_list[car_id]
            if decel_min <= 1.53: # was <=4.2 originally for some reason
                DA['Categories'][index] = 'Negligible'
            elif 5.0 >= decel_min > 1.53: # was >4.2 originally for some reason
                DA['Categories'][index] = 'Benign'
            elif decel_min > 5.0:
                DA['Categories'][index] = 'Severe_braking'
                # DA['Categories'][index] = 'Severe'
    #==================================================================================#
    #                                     Categorization                               #
    #==================================================================================#
    #Change the type
    DA.Injected_value  = DA.Injected_value.astype('category')
    DA.Start_time = DA.Start_time.astype('category')
    DA.Collision_state = DA.Collision_state.astype('category')
    DA.Categories = DA.Categories.astype('category')
    DA.Affected_car = DA.Affected_car.astype('category')
    #==================================================================================#
    #              Print: Classified results as Severe, benign, etc.                   #
    #==================================================================================#
    print('==========================================\n     Classified Results \n==========================================')
    print('Total:           ', DA.Categories.count())
    print('Severe_collision:', DA.Categories[(DA.Categories == "Severe_collision")].count())
    print('Severe_braking:  ', DA.Categories[(DA.Categories == "Severe_braking")].count())
    # print('Severe:          ', DA.Categories[(DA.Categories == "Severe")].count())
    print('Benign:          ', DA.Categories[(DA.Categories == "Benign")].count())
    print('Negligible:      ', DA.Categories[(DA.Categories == "Negligible")].count())
    print('Non_effective:   ', DA.Categories[(DA.Categories == "Non_effective")].count())
    print('==========================================\n==========================================')
    #==================================================================================#
    #                 Plot: Attack duration vs Experiment numbers                      #
    #==================================================================================#
    ATTList = DA.Categories.cat.categories
    List = []
    Label = []
    Colors = []

    for name in ATTList:
        List.append(DA[DA.Categories == name].AttackDuration)
        Label.append(name)
        if name == "Non_effective":
            Colors.append("green")
        elif name == "Negligible":
            Colors.append("steelblue")
        elif name == "Benign":
            Colors.append("darkorange")
        elif name == "Severe_braking":
            Colors.append("red")
        elif name == "Severe_collision":
            Colors.append("darkred")

    sns.set_style('whitegrid')
    fig, ax = plt.subplots()
    fig.set_size_inches(11.7, 8.27)  # size of A4 paper 11.7, 8.27
    sns.set_palette(palette="deep")
    # plt.hist(List, bins=30, color={"green", "blue", "red", "black"}, hatch={'*', 'x', 'o', '+'}, stacked=True, rwidth=0.7,label=Label)
    print(DA.Categories)
    plt.hist(List, bins=31, stacked=True, rwidth=2.17, color=Colors,
                label=Label)
    plt.xlabel('Attack duration [s]', fontsize=22, color='black')
    plt.xticks(fontsize=19)
    plt.ylabel('Number of experiments', fontsize=22, color='black')
    #plt.ylim([-1, 2600])
    plt.yticks(fontsize=19)
    plt.legend(fontsize=16,  ncol=5, loc='upper center', bbox_to_anchor=(0.5, 1.035))
    # plt.show()
    if fileName2 != None:
        filePathAbs = str(Path(fileName1).absolute()).split(fileName1)[0] + "ComFASE_data/" + fileName1[0:-4]
        graphFilePath = filePathAbs + '/' + expTypeName + '_AttackDuration_vs_NumberOfExp' +'.png'
        print(graphFilePath)
        plt.savefig(graphFilePath, dpi=plt.gcf().dpi, bbox_inches='tight')
    else:
        plt.show()
    #==================================================================================#
    #                     Print: cars involved in collisions                           #
    #==================================================================================#

    print('==========================================\n     Cars Involved in Collisions \n==========================================')
    print('Car1: ', DA.Affected_car[(DA.Affected_car == "Car 1") & (DA.Categories == "Severe_collision")].count())
    print('Car2: ', DA.Affected_car[(DA.Affected_car == "Car 2") & (DA.Categories == "Severe_collision")].count())
    print('Car3: ', DA.Affected_car[(DA.Affected_car == "Car 3") & (DA.Categories == "Severe_collision")].count())
    print('Car4: ', DA.Affected_car[(DA.Affected_car == "Car 4") & (DA.Categories == "Severe_collision")].count())
    print('Total: ', DA.Affected_car[(DA.Categories == "Severe_collision")].count())
    #==================================================================================#
    #               Plot: Injection Time vs Number of Experiments                      #
    #==================================================================================#
    def round_2(x):
        try:
            return round(x, 2)
        except:
            return x
    DA['Start_time'] = DA['Start_time'].apply(round_2)
    time_nonEffective = []
    time_negligible = []
    time_benign = []
    time_severe = []
    time_severeCollision = []
    numbers_nonEffective = []
    numbers_negligible = []
    numbers_benign = []
    numbers_severe = []
    numbers_severeCollision = []
    # Change the AttackStartTimeRange according to the selected traffic scenario such as "Sinusoidal", "Braking"
    for attackStartTime in numpy.arange(attackInitiationStartTime, attackInitiationEndTime, attackInitiationTimeStep):
        attackStartTime = round(attackStartTime, 2)
        time_nonEffective.append(attackStartTime)
        numbers_nonEffective.append(DA.Start_time[(DA.Categories == "Non_effective") & (DA['Start_time'] == attackStartTime)].count())
        time_negligible.append(attackStartTime)
        numbers_negligible.append(DA.Start_time[(DA.Categories == "Negligible") & (DA['Start_time'] == attackStartTime)].count())
        # Numbers of Benign
        time_benign.append(attackStartTime)
        numbers_benign.append(DA.Start_time[(DA.Categories == "Benign") & (DA['Start_time'] == attackStartTime)].count())
        # Numbers of Severe_braking
        time_severe.append(attackStartTime)
        numbers_severe.append(DA.Start_time[(DA.Categories == "Severe_braking") & (DA['Start_time'] == attackStartTime)].count())
        # Numbers of Severe_collision
        time_severeCollision.append(attackStartTime)
        numbers_severeCollision.append(DA.Start_time[(DA.Categories == "Severe_collision") & (DA['Start_time'] == attackStartTime)].count())

    fig, ax = plt.subplots()
    fig.set_size_inches(11.7, 8.27)  # size of A4 paper
    plt.plot(time_benign, numbers_benign, '*', color='darkorange', linewidth=1, linestyle='-')
    plt.plot(time_negligible, numbers_negligible, '+b', linewidth=1, linestyle='dashed')
    plt.plot(time_nonEffective, numbers_nonEffective, '*g', linewidth=1, linestyle='dashed')
    plt.plot(time_severe, numbers_severe, '^r', linewidth=1, linestyle='--')
    plt.plot(time_severeCollision, numbers_severeCollision, '^', color='darkred', linewidth=1, linestyle='--')
    plt.xlabel('Attack start time (s)', fontsize='22')
    plt.ylabel('Number of experiments', fontsize='22')
    x_ticks = np.arange(attackInitiationStartTime, attackInitiationEndTime, attackInitiationTimeStep)
    plt.xticks(x_ticks)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.gcf().autofmt_xdate()
    #plt.title('Controller 2 (CACC) - Sender & Receiver - Propagation Delay')
    plt.legend(['Benign', 'Negligible', 'Non-effective', 'Severe_braking', 'Severe_collision'],  ncol=5, loc='upper center', bbox_to_anchor=(0.5, 1.05), prop={"size":16})
    # plt.show()
    if fileName2 != None:
        filePathAbs = str(Path(fileName1).absolute()).split(fileName1)[0] + "ComFASE_data/" + fileName1[0:-4]
        graphFilePath = filePathAbs + '/' + expTypeName + '_AttackStartTime_vs_NumberOfExp' +'.png'
        print(graphFilePath)
        plt.savefig(graphFilePath, dpi=plt.gcf().dpi, bbox_inches='tight')
    else:
        plt.show()
    #==================================================================================#
    #               Plot: Injected Value vs Number of Experiments                      #
    #==================================================================================#
    Injected_value_nonEffective = []
    Injected_value_negligible = []
    Injected_value_benign = []
    Injected_value_severe = []
    Injected_value_severeCollision = []
    EXnumbers_nonEffective = []
    EXnumbers_negligible = []
    EXnumbers_benign = []
    EXnumbers_severe = []
    EXnumbers_severeCollision = []
    # Change the attackValueRange according to the selected attack model such as "NoiseValue" , "Destructiveness"
    for attackValue in numpy.arange(attackStartValue, attackEndValue, attackValueStep):
        attackValue = round(attackValue, 8)
        Injected_value_nonEffective.append(attackValue)
        EXnumbers_nonEffective.append(DA.Start_time[(DA.Categories == "Non_effective") & (DA['Injected_value'] == attackValue)].count())
        Injected_value_negligible.append(attackValue)
        EXnumbers_negligible.append(DA.Start_time[(DA.Categories == "Negligible") & (DA['Injected_value'] == attackValue)].count())
        # Numbers of Benign
        Injected_value_benign.append(attackValue)
        EXnumbers_benign.append(DA.Start_time[(DA.Categories == "Benign") & (DA['Injected_value'] == attackValue)].count())
        # Numbers of Severe_braking
        Injected_value_severe.append(attackValue)
        EXnumbers_severe.append(DA.Start_time[(DA.Categories == "Severe_braking") & (DA['Injected_value'] == attackValue)].count())
        # Numbers of Severe_collision
        Injected_value_severeCollision.append(attackValue)
        EXnumbers_severeCollision.append(DA.Start_time[(DA.Categories == "Severe_collision") & (DA['Injected_value'] == attackValue)].count())

    fig, ax = plt.subplots()
    fig.set_size_inches(11.7, 8.27)  # size of A4 paper
    plt.plot(Injected_value_benign, EXnumbers_benign, '*', color='darkorange', linewidth=1, linestyle='-')
    plt.plot(Injected_value_negligible, EXnumbers_negligible, '+b', linewidth=1, linestyle='dashed')
    plt.plot(Injected_value_nonEffective, EXnumbers_nonEffective, '*g', linewidth=1, linestyle='dashed')
    plt.plot(Injected_value_severe, EXnumbers_severe, '^r', linewidth=1, linestyle='--')
    plt.plot(Injected_value_severeCollision, EXnumbers_severeCollision, '^', color='darkred', linewidth=1, linestyle='--')
    # Change the label according to the selected attack model such as "Delay amount", "Destructiveness"
    plt.xlabel('Noise value ($10^{-5}mW$)', fontsize='22')
    plt.ylabel('Number of experiments', fontsize='22')
    x_ticks = np.arange(attackStartValue, attackEndValue, attackValueStep)
    plt.xticks(x_ticks)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.gcf().autofmt_xdate()
    # plt.title('Received Power after Attack: $P_r^{*} = P_r (1-D)$')
    plt.legend(['Benign', 'Negligible', 'Non-effective', 'Severe_braking', 'Severe_collision'],  ncol=5, loc='upper center', bbox_to_anchor=(0.5, 1.05), prop={"size":16})
    # plt.show()
    if fileName2 != None:
        filePathAbs = str(Path(fileName1).absolute()).split(fileName1)[0] + "ComFASE_data/" + fileName1[0:-4]
        graphFilePath = filePathAbs + '/' + expTypeName + '_NoiseValue_vs_NumberOfExp' +'.png'
        print(graphFilePath)
        plt.savefig(graphFilePath, dpi=plt.gcf().dpi, bbox_inches='tight')
    else:
        plt.show()


if __name__ == '__main__':
    main()
