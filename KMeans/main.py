from utils import *
from random import randint
import numpy as np
import copy
import matplotlib.pyplot as plt
def get_distance(x1,y1,x2,y2):
    return np.sqrt((x2-x1)**2 + (y2-y1)**2)


def read_data():
    data=[]
    # a list of triplets, first is label, the other 2 are values
    with open("dataset.csv","r") as f:
        for line in f:
            splitted=line.split(",")
            label=splitted[0]
            coordX=float(splitted[1])
            coordY=float(splitted[2])
            data.append([label,coordX,coordY])

    return data

def run_main():
    data=read_data()
    global_best_accuracy=-1
    global_A_line=-1
    global_A_column=-1
    global_B_line = -1
    global_B_column = -1
    global_C_line = -1
    global_C_column = -1
    global_D_line = -1
    global_D_column = -1

    for run in range(0,times_to_run,1):
        unlabeled = copy.deepcopy(data)

        cluster_A_index=randint(0,len(data))
        cluster_B_index = randint(0, len(data))
        cluster_C_index = randint(0, len(data))
        cluster_D_index = randint(0, len(data))


        cluster_A_line = data[cluster_A_index][1]
        cluster_A_column = data[cluster_A_index][2]

        cluster_B_line=data[cluster_B_index][1]
        cluster_B_column = data[cluster_B_index][2]

        cluster_C_line = data[cluster_C_index][1]
        cluster_C_column = data[cluster_C_index][2]

        cluster_D_line = data[cluster_D_index][1]
        cluster_D_column = data[cluster_D_index][2]

        for entry in unlabeled:

            distance_to_A = get_distance(cluster_A_line,cluster_A_column,entry[1],entry[2])
            distance_to_B = get_distance(cluster_B_line, cluster_B_column, entry[1], entry[2])
            distance_to_C = get_distance(cluster_C_line, cluster_C_column, entry[1], entry[2])
            distance_to_D = get_distance(cluster_D_line, cluster_D_column, entry[1], entry[2])

            distances=[distance_to_A,distance_to_B,distance_to_C,distance_to_D]

            min_dist=distances[distances.index(min(distances))]
            if min_dist == distance_to_A:
                #labeled A
                entry[0]="A"
            elif min_dist == distance_to_B:
                #labeled B
                entry[0]="B"
            elif min_dist == distance_to_C:
                entry[0]="C"

            elif min_dist == distance_to_D:
                entry[0]="D"


        keep_going=True
        while keep_going:

            keep_going=False

            tmp_cluster_A_line=0
            tmp_cluster_A_column=0
            clusterAcount=0

            tmp_cluster_B_line = 0
            tmp_cluster_B_column = 0
            clusterBcount = 0

            tmp_cluster_C_line = 0
            tmp_cluster_C_column = 0
            clusterCcount = 0

            tmp_cluster_D_line = 0
            tmp_cluster_D_column = 0
            clusterDcount = 0

            for entry in unlabeled:
                if entry[0]=="A":
                    clusterAcount+=1
                    tmp_cluster_A_line+=entry[1]
                    tmp_cluster_A_column+=entry[2]
                if entry[0]=="B":
                    clusterBcount+=1
                    tmp_cluster_B_line+=entry[1]
                    tmp_cluster_B_column+=entry[2]

                if entry[0]=="C":
                    clusterCcount+=1
                    tmp_cluster_C_line+=entry[1]
                    tmp_cluster_C_column+=entry[2]

                if entry[0]=="D":
                    clusterDcount+=1
                    tmp_cluster_D_line+=entry[1]
                    tmp_cluster_D_column+=entry[2]

            tmp_cluster_A_column=tmp_cluster_A_column/clusterAcount
            tmp_cluster_A_line=tmp_cluster_A_line/clusterAcount

            tmp_cluster_B_column=tmp_cluster_B_column/clusterBcount
            tmp_cluster_B_line = tmp_cluster_B_line / clusterBcount

            tmp_cluster_C_column = tmp_cluster_C_column / clusterCcount
            tmp_cluster_C_line = tmp_cluster_C_line / clusterCcount

            tmp_cluster_D_column = tmp_cluster_D_column / clusterDcount
            tmp_cluster_D_line = tmp_cluster_D_line / clusterDcount

            for entry in unlabeled:
                label=entry[0]
                distance_to_current_cluster=0

                if label=='A':
                    distance_to_current_cluster = get_distance(entry[1],entry[2],tmp_cluster_A_line,tmp_cluster_A_column)
                if label=='B':
                    distance_to_current_cluster = get_distance(entry[1],entry[2],tmp_cluster_B_line,tmp_cluster_B_column)
                if label=='C':
                    distance_to_current_cluster = get_distance(entry[1],entry[2],tmp_cluster_C_line,tmp_cluster_C_column)
                if label=='D':
                    distance_to_current_cluster = get_distance(entry[1],entry[2],tmp_cluster_D_line,tmp_cluster_D_column)

                distance_to_A = get_distance(tmp_cluster_A_line, tmp_cluster_A_column, entry[1], entry[2])
                distance_to_B = get_distance(tmp_cluster_B_line, tmp_cluster_B_column, entry[1], entry[2])
                distance_to_C = get_distance(tmp_cluster_C_line, tmp_cluster_C_column, entry[1], entry[2])
                distance_to_D = get_distance(tmp_cluster_D_line, tmp_cluster_D_column, entry[1], entry[2])

                distances = [distance_to_A, distance_to_B, distance_to_C, distance_to_D]

                min_dist = distances[distances.index(min(distances))]


                if min_dist == distance_to_A and label !='A' and distance_to_A < distance_to_current_cluster:
                    # closest cluster is A and current cluster is not A, entry is closer to A than to it's assigned cluster
                    keep_going=True
                    entry[0] = "A"
                elif min_dist == distance_to_B and label !='B' and distance_to_B < distance_to_current_cluster:
                    # closest cluster is B and current cluster is not B, entry is closer to B than to it's assigned cluster
                    keep_going = True
                    # labeled B
                    entry[0] = "B"
                elif min_dist == distance_to_C and label != 'C' and distance_to_C < distance_to_current_cluster:
                    # closest cluster is C and current cluster is not C, entry is closer to C than to it's assigned cluster
                    keep_going = True
                    entry[0] = "C"


                elif min_dist == distance_to_D and label != 'D' and distance_to_D < distance_to_current_cluster:
                    # closest cluster is D and current cluster is not D, entry is closer to D than to it's assigned cluster
                    keep_going = True
                    entry[0] = "D"

            correct_labels=0
            for i in range(0,len(unlabeled),1):
                if unlabeled[i]==data[i]:
                    correct_labels=correct_labels+1


            if correct_labels/len(unlabeled) > global_best_accuracy:
                global_best_accuracy=correct_labels/len(unlabeled)

                global_A_line=tmp_cluster_A_line
                global_A_column=tmp_cluster_A_column

                global_B_line = tmp_cluster_B_line
                global_B_column = tmp_cluster_B_column

                global_C_line = tmp_cluster_C_line
                global_C_column = tmp_cluster_C_column

                global_D_line = tmp_cluster_D_line
                global_D_column = tmp_cluster_D_column


    final_cluster_lines=[global_A_line,global_B_line,global_C_line,global_D_line]
    final_cluster_columns=[global_A_column,global_B_column,global_C_column,global_D_column]

    data_lines=[]
    data_columns=[]
    for entry in data:
        data_lines.append(entry[1])
        data_columns.append(entry[2])
    plt.scatter(data_lines, data_columns, c='red')
    colors=["red", "blue", "green", "yellow"]

    plt.scatter(final_cluster_lines, final_cluster_columns, c='black')
    plt.xlabel('val1')
    plt.ylabel('val2')
    plt.show()

    true_positivesA=0
    true_negativesA=0

    false_positivesA=0
    false_negativesA=0

    true_positivesB = 0
    true_negativesB = 0

    false_positivesB = 0
    false_negativesB = 0

    true_positivesC = 0
    true_negativesC = 0

    false_positivesC = 0
    false_negativesC = 0

    true_positivesD = 0
    true_negativesD = 0

    false_positivesD = 0
    false_negativesD = 0

    for entry in data:
        if entry[0]=='A':
            if unlabeled[0]=='A':
                true_positivesA+=1
            else:
                false_positivesA+=1
        else:
            if unlabeled[0]=='A':
                false_negativesA+=1
            else:
                true_negativesA+=1

    for entry in data:
        if entry[0]=='B':
            if unlabeled[0]=='B':
                true_positivesB+=1
            else:
                false_positivesB+=1
        else:
            if unlabeled[0]=='B':
                false_negativesB+=1
            else:
                true_negativesB+=1

    for entry in data:
        if entry[0]=='C':
            if unlabeled[0]=='C':
                true_positivesC+=1
            else:
                false_positivesC+=1
        else:
            if unlabeled[0]=='C':
                false_negativesC+=1
            else:
                true_negativesC+=1

    for entry in data:
        if entry[0]=='C':
            if unlabeled[0]=='C':
                true_positivesC+=1
            else:
                false_positivesC+=1
        else:
            if unlabeled[0]=='C':
                false_negativesC+=1
            else:
                true_negativesC+=1

    for entry in data:
        if entry[0]=='D':
            if unlabeled[0]=='D':
                true_positivesD+=1
            else:
                false_positivesD+=1
        else:
            if unlabeled[0]=='D':
                false_negativesD+=1
            else:
                true_negativesD+=1

    print("Statistics: ")
    print("A: ")
    print("Accuracy: ", (true_positivesA+true_negativesA)/(len(data)))
    print("Precision: ", (true_positivesA/(true_positivesA+false_positivesA)))
    print("Rappel: ", (true_positivesA)/(true_positivesA+false_negativesA))
    print("Score: ", 2*(true_positivesA/(true_positivesA+false_positivesA))*(true_positivesA)/(true_positivesA+false_negativesA)/((true_positivesA/(true_positivesA+false_positivesA))) + (true_positivesA)/(true_positivesA+false_negativesA))






























run_main()




















