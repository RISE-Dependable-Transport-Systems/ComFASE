import pandas as pd
import numpy
import numpy as np
import random
import csv
import os
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from matplotlib.ticker import PercentFormatter
from pathlib import Path

def main(fileName1 = None, fileName2 = None, expTypeName = "", startTime = 17.0, endXAxisOn = 11):


    plt.rcParams['figure.figsize'] = 16,7
    import warnings
    warnings.filterwarnings('ignore')
    #==================================================================================#
    #                     Read parsed data for attack campaign                         #
    #==================================================================================#
    # please correct the address accordingly
    if fileName2 != None:
        DA = pd.read_csv(fileName2)
    else:
        DA = pd.read_csv('Parsed Accel-Deceleration_All Vehicles_2024-09-20 14.23.41 ParsedData.csv')
    #DA.info()
    #print("\n\n\n", DA.head(3))
    # Add new columns to include AttackDuration and Categories
    DA['AttackDuration'] = DA['End_time'] - DA['Start_time']
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
            #car_list = ['vtypeauto.0', 'vtypeauto.1', 'vtypeauto.2', 'vtypeauto.3']
            car_list = ['Car 1', 'Car 2', 'Car 3', 'Car 4']
            car_id = decel_list.index(min(decel_list))
            DA['Affected_car'][index] = car_list[car_id]
            #print('car ID', car_id, decel_list[car_id])
            if decel_min <= 1.53:
                DA['Categories'][index] = 'Negligible'
            elif 5.0 >= decel_min > 1.53:
                DA['Categories'][index] = 'Benign'
            elif decel_min > 5.0:
                DA['Categories'][index] = 'Severe_braking'
                # DA['Categories'][index] = 'Severe'
    #==================================================================================#
    #          hh              #
    #==================================================================================#
    #Change the type
    DA.Injected_value = DA.Injected_value.astype('category')
    DA.Start_time = DA.Start_time.astype('category')
    DA.Collision_state = DA.Collision_state.astype('category')
    DA.Categories = DA.Categories.astype('category')
    DA.Affected_car = DA.Affected_car.astype('category')
    #==================================================================================#
    #              print: classified results as severe, benign, etc.                   #
    #==================================================================================#
    print('==========================================\n     classified results \n==========================================')
    print('total:           ', DA.Categories.count())
    print('Severe_braking:  ', DA.Categories[(DA.Categories == "Severe_braking")].count())
    print('Severe_collision:', DA.Categories[(DA.Categories == "Severe_collision")].count())
    print('benign:          ', DA.Categories[(DA.Categories == "Benign")].count())
    print('negligible:      ', DA.Categories[(DA.Categories == "Negligible")].count())
    print('non_effective:   ', DA.Categories[(DA.Categories == "Non_effective")].count())
    print('==========================================\n==========================================')


    #==================================================================================#
    #              print: classified results as severe, benign, etc.                   #
    #==================================================================================#
    #print('==========================================\n     classified results \n==========================================')
    #print('total:           ', DA.Categories.count())
    #print('severe:          ', DA.Categories[(DA.Categories == "severe")].count())
    #print('severe_braking:  ', da.categories[(da.categories == "severe_braking")].count())
    #print('benign:          ', DA.Categories[(DA.Categories == "benign")].count())
    #print('negligible:      ', DA.Categories[(DA.Categories == "negligible")].count())
    #print('non_effective:   ', DA.Categories[(DA.Categories == "non_effective")].count())
    #print('==========================================\n==========================================')
    #==================================================================================#
    #                 Plot: Attack duration vs Experiment numbers                      #
    #==================================================================================#
    # ATTList = DA.Categories.cat.categories
    # print('list for catagories: ', ATTList)
    # List = []
    # Label = []
    #
    # for name in ATTList:
    #     # if name != "Severe_braking":
    #     List.append(DA[DA.Categories == name].AttackDuration)
    #     Label.append(name)
    # print('list elements: ', type(List))
    # sns.set_style('whitegrid')
    # fig, ax = plt.subplots()
    # fig.set_size_inches(11.7, 8.27)  # size of A4 paper
    # #print("newlist", ATTList)
    # #print("listprint", List)
    # #print("labelprint", Label)
    # # patterns = ['x','/','O','+']
    # sns.set_palette(palette="deep")
    # # plt.hist(List, bins=30, color={"green", "blue", "red", "black"}, hatch={'*', 'x', 'o', '+'}, stacked=True, rwidth=0.7,label=Label)
    # plt.hist(List, bins=30, stacked=True, rwidth=0.7,
    #              label=Label)
    #
    # # h = plt.hist(List, bins=30, color = {"green", "blue", "red"}, hatch=(patterns.pop(0)), stacked=True, rwidth=0.7, label=Label)
    # # plt.title('Barrage Jamming: Attack duration vs Result classification', fontsize=14,
    # #           color='DarkBlue', fontname='Arial')
    # # plt.legend(['Non-effective', 'Negligible', 'Benign', 'Severe'], loc='best', bbox_to_anchor=(0.925, 0.5), prop={"size":12})
    # plt.xlabel('Attack duration [s]', fontsize=22, color='black')
    # plt.xticks(fontsize=15)
    # plt.ylabel('Number of experiments', fontsize=22, color='black')
    # #plt.ylim([-1, 2600])
    # plt.yticks(fontsize=15)
    # plt.legend(fontsize=16,  ncol=4, loc='upper center', bbox_to_anchor=(0.5, 1.04))#, mode="expand")  # frameon=False, framealpha=0.5, shadow=True
    # plt.show()

    #==================================================================================#
    #               Plot: Injection Time vs Number of Experiments                      #
    #==================================================================================#
    # def round_2(x):
    #     try:
    #         return round(x, 2)
    #     except:
    #         return x
    # #DA['Start_time'] = DA['Start_time'].round(2)
    # DA['Start_time'] = DA['Start_time'].apply(round_2)
    # #print("meeeeeeeeen\n ", DA['Start_time'])
    # time_nonEffective = []
    # time_negligible = []
    # time_benign = []
    # time_severe = []
    # numbers_nonEffective = []
    # numbers_negligible = []
    # numbers_benign = []
    # numbers_severe = []
    # for ii in numpy.arange(17.0, 21.9, 0.2):
    #     iii= round(ii, 2)
    #     time_nonEffective.append(iii)
    #     numbers_nonEffective.append(DA.Start_time[(DA.Categories == "Non_effective") & (DA['Start_time'] == iii)].count())
    #     time_negligible.append(iii)
    #     numbers_negligible.append(DA.Start_time[(DA.Categories == "Negligible") & (DA['Start_time'] == iii)].count())
    #     # Numbers of Benign
    #     time_benign.append(iii)
    #     numbers_benign.append(DA.Start_time[(DA.Categories == "Benign") & (DA['Start_time'] == iii)].count())
    #     # print('Numbers in %s = ' %iii, DA.Start_time[(DA.Categories == "Benign") & (DA['Start_time'] == iii)].count())
    #     # Numbers of Severe
    #     time_severe.append(iii)
    #     numbers_severe.append(DA.Start_time[(DA.Categories == "Severe") & (DA['Start_time'] == iii)].count())
    # plt.plot(time_benign, np.divide(numbers_benign, 30), '*b', linewidth=1, linestyle='-')
    # plt.plot(time_negligible, np.divide(numbers_negligible, 30),  '+', color='darkorange', linewidth=1, linestyle='dashed')
    # plt.plot(time_nonEffective, np.divide(numbers_nonEffective, 30), '*g', linewidth=1, linestyle='dashed')
    # plt.plot(time_severe, np.divide(numbers_severe, 30), '^r', linewidth=1, linestyle='--')
    # # plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    # plt.xlabel('Attack start time (s)', fontsize='22')
    # plt.ylabel('Number of experiments (%)', fontsize='22')
    # x_ticks = np.arange(17.0, 21.8, 0.2)
    # plt.xticks(x_ticks)
    # y_ticks = np.arange(0, 101, 10)
    # plt.yticks(y_ticks)
    # plt.xticks(fontsize=15)
    # plt.yticks(fontsize=15)
    # plt.gcf().autofmt_xdate()
    # #plt.title('Controller 2 (CACC) - Sender & Receiver - Propagation Delay')
    # plt.legend(['Benign', 'Negligible', 'Non-effective', 'Severe'], ncol=4, loc='upper center', bbox_to_anchor=(0.5, 1.05), prop={"size":16})
    # plt.show()
    #==================================================================================#
    #               Plot: Injected Value vs Number of Experiments                      #
    #==================================================================================#
    # PDelay_nonEffective = []
    # PDelay_negligible = []
    # PDelay_benign = []
    # PDelay_severe = []
    # PDnumbers_nonEffective = []
    # PDnumbers_negligible = []
    # PDnumbers_benign = []
    # PDnumbers_severe = []
    # for ii in numpy.arange(0.01, 1.01, 0.01):
    #     iii= round(ii, 2)
    #     PDelay_nonEffective.append(iii)
    #     PDnumbers_nonEffective.append(DA.Start_time[(DA.Categories == "Non_effective") & (DA['Injected_value'] == iii)].count())
    #     PDelay_negligible.append(iii)
    #     PDnumbers_negligible.append(DA.Start_time[(DA.Categories == "Negligible") & (DA['Injected_value'] == iii)].count())
    #     # Numbers of Benign
    #     PDelay_benign.append(iii)
    #     PDnumbers_benign.append(DA.Start_time[(DA.Categories == "Benign") & (DA['Injected_value'] == iii)].count())
    #     # print('Numbers in %s = ' %iii, DA.Start_time[(DA.Categories == "Benign") & (DA['Injected_value'] == iii)].count())
    #     # Numbers of Severe
    #     PDelay_severe.append(iii)
    #     PDnumbers_severe.append(DA.Start_time[(DA.Categories == "Severe") & (DA['Injected_value'] == iii)].count())
    # plt.plot(PDelay_benign, np.divide(PDnumbers_benign, 7.5), '*b', linewidth=1, linestyle='-')
    # plt.plot(PDelay_negligible, np.divide(PDnumbers_negligible, 7.5), '+', color='darkorange', linewidth=1, linestyle='dashed')
    # plt.plot(PDelay_nonEffective, np.divide(PDnumbers_nonEffective, 7.5), '*g', linewidth=1, linestyle='dashed')
    # plt.plot(PDelay_severe, np.divide(PDnumbers_severe, 7.5), '^r', linewidth=1, linestyle='--')
    # plt.xlabel('Noise value ($10^{-5}mW$)', fontsize='22')
    # plt.ylabel('Number of experiments (%)', fontsize='22')
    # #ax.set_zlabel('Duration (S)', fontsize='10')
    # # ax.view_init(60, 35)
    # y_ticks = np.arange(0, 101, 10)
    # plt.yticks(y_ticks)
    # x_ticks = np.arange(0.00, 1.01, 0.05)
    # plt.xticks(x_ticks)
    # plt.xticks(fontsize=15)
    # plt.yticks(fontsize=15)
    # plt.gcf().autofmt_xdate()
    # #plt.title('Controller 2 (CACC) - Sender & Receiver - Propagation Delay')
    # plt.legend(['Benign', 'Negligible', 'Non-effective', 'Severe'], ncol=4, loc='upper center', bbox_to_anchor=(0.5, 1.05), prop={"size":16})
    # # plt.legend(fontsize=16,  ncol=4, loc='upper center', bbox_to_anchor=(0.5, 1.05))
    # plt.show()
    #==================================================================================#
    #                 Scatter Plot: Attack duration vs Attack Values                      #
    #==================================================================================#
    # ATTList = DA.Categories.cat.categories
    ATTList = ["Non_effective", "Negligible", "Benign", "Severe_braking", "Severe_collision"] #DA.Categories.cat.categories

    print("++++++++++++++++++++++++++++++++++++++++++++++++")
    data_start_time_wanted = DA[DA.Start_time == startTime]
    print('severeBrakingCases@specificStartTime:         ', DA.Categories[(DA.Start_time == startTime) & (DA.Categories == "Severe_braking")].count())
    print('severeCollisionCases@specificStartTime:         ', DA.Categories[(DA.Start_time == startTime) & (DA.Categories == "Severe_collision")].count())

    print("++++++++++++++++++++++++++++++++++++++++++++++++")
    #data_start_time_wanted = DA[(DA.Start_time == 17.8) & (DA.Affected_car == 'Car 4')]
    print('severeCollisionCasesCar1@specificStartTime: ' + str(startTime) + " ", DA.Categories[(DA.Start_time == startTime) & (DA.Categories == "Severe_collision") & (DA.Affected_car == 'Car 1')].count())
    print('severeCollisionCasesCar2@specificStartTime: ' + str(startTime) + " ", DA.Categories[(DA.Start_time == startTime) & (DA.Categories == "Severe_collision") & (DA.Affected_car == 'Car 2')].count())
    print('severeCollisionCasesCar3@specificStartTime: ' + str(startTime) + " ", DA.Categories[(DA.Start_time == startTime) & (DA.Categories == "Severe_collision") & (DA.Affected_car == 'Car 3')].count())
    print('severeCollisionCasesCar4@specificStartTime: ' + str(startTime) + " ", DA.Categories[(DA.Start_time == startTime) & (DA.Categories == "Severe_collision") & (DA.Affected_car == 'Car 4')].count())
    print("++++++++++++++++++++++++++++++++++++++++++++++++")

    for instantaneousStartTime in [17.0,17.4,17.8,18.6,19.0,19.8,20.6,21.0,21.4]:
        this_severe_collision_tot = DA.Categories[(DA.Start_time == instantaneousStartTime) & (DA.Categories == "Severe_collision")].count()
        this_severe_collision_1 = DA.Categories[(DA.Start_time == instantaneousStartTime) & (DA.Categories == "Severe_collision") & (DA.Affected_car == 'Car 1')].count()
        if this_severe_collision_1 != 0:
            raise Exception("Please modify code, severe collision for Car 1 is a non-zero number")
        this_severe_collision_2 = DA.Categories[(DA.Start_time == instantaneousStartTime) & (DA.Categories == "Severe_collision") & (DA.Affected_car == 'Car 2')].count()
        this_severe_collision_3 = DA.Categories[(DA.Start_time == instantaneousStartTime) & (DA.Categories == "Severe_collision") & (DA.Affected_car == 'Car 3')].count()
        this_severe_collision_4 = DA.Categories[(DA.Start_time == instantaneousStartTime) & (DA.Categories == "Severe_collision") & (DA.Affected_car == 'Car 4')].count()

        print(str(instantaneousStartTime)+"                 & x               & x  & x  & x  & x  & "+str(this_severe_collision_tot)+"                  & -  & "+str(this_severe_collision_2)+"  & "+str(this_severe_collision_3)+" & "+str(this_severe_collision_4)+" \\"+ "\\"+"\\hline")

    x = data_start_time_wanted.loc[:, "AttackDuration"].values
    y = data_start_time_wanted.loc[:, "Injected_value"].values
    categories = data_start_time_wanted.loc[:, "Categories"].values



    #print(x)
    #print(y)
    sns.set_style('whitegrid')
    fig, ax = plt.subplots()
    fig.set_size_inches(11.7, 8.27)  # size of A4 paper
    sns.set_palette(palette="deep")
    color_map = {"Non_effective": 'green', "Negligible": 'blue', "Benign": 'darkorange', "Severe_braking": 'red', "Severe_collision": 'darkred'}
    colors = [color_map[category] for category in categories]
    plt.scatter(x, y, c=colors, s=140)
    # plt.hist(List, bins=30, color={"green", "blue", "red", "black"}, hatch={'*', 'x', 'o', '+'}, stacked=True, rwidth=0.7,label=Label)
    #plt.hist(List, bins=19, stacked=True, rwidth=2.17,
    #             label=Label, color={"darkorange", "blue", "green", "darkred"})
    plt.xlabel('Attack duration [s]', fontsize=22, color='black')
    plt.xticks(fontsize=10)
    # plt.ylabel('Number of experiments', fontsize=22, color='black')
    plt.ylabel('Noise value ($10^{-5}mW$)', fontsize=22, color='black')
    #plt.ylim([-1, 2600])
    # x_ticks = np.arange(1, 11, 1)
    # plt.xticks(x_ticks)
    plt.yticks(fontsize=10)
    #y_ticks = np.arange(0, 1.01, 0.025)
    # y_ticks = np.arange(0.01, 1.01, 0.01)
    y_ticks = np.arange(0.2, 1.01, 0.2)
    #print(y_ticks)
    plt.yticks(y_ticks)
    plt.yticks(rotation=25)
    # plt.gcf().autofmt_xdate()
    x_ticks = np.arange(1, endXAxisOn + 0.01, 1)
    plt.xticks(x_ticks)
    plt.gcf().autofmt_xdate()
    color_patch1 = mpatches.Patch(color='green', label="Non_effective")
    color_patch2 = mpatches.Patch(color='blue', label="Negligible")
    color_patch3 = mpatches.Patch(color='darkorange', label="Benign")
    color_patch4 = mpatches.Patch(color='red', label="Severe_braking")
    color_patch5 = mpatches.Patch(color='darkred', label="Severe_collision")
    plt.legend(handles=[color_patch1, color_patch2, color_patch3, color_patch4, color_patch5], ncol=5, loc='upper center', bbox_to_anchor=(0.5, 1.05), prop={"size":12.8})
    if fileName2 != None:
        filePathAbs = str(Path(fileName1).absolute()).split(fileName1)[0] + "ComFASE_data/" + fileName1[0:-4]
        graphFilePath = filePathAbs + '/' + expTypeName + '_Start_Time_' + str(startTime) +'.png'
        print(graphFilePath)
        plt.savefig(graphFilePath, dpi=plt.gcf().dpi)
    else:
        plt.show()


if __name__ == '__main__':
    main()
