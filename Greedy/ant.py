fill_map_proportion=0.15
from random import *

from Gui import *
from SearchGreedy import *
import pickle ,pygame ,sys
from pygame.locals import *
from constants import *
from service import *
from domain import *





def main():
    map=Map()
    map.randomMap()
    gui=GUI()

    gui.mapImage(map)

    print("Enter drone position")
    print("X= ")
    X=int(input())
    print("Y= ")
    Y=int(input())
    while not map.valid_move(X,Y):
        print("Invalid position")
        print("Enter drone position")
        print("X= ")
        X = int(input())
        print("Y= ")
        Y = int(input())
    print("Enter the drone energy")
    energy=int(input())
    #we consider the first drone to be a sensor in the context of distances
    sensors=[]
    sensors.append([X,Y])

    sensor_count=int(input("Enter the sensor count"))
    distances=[ [0 for i in range(sensor_count+1)] for j in range(sensor_count+1)]
    for i in range(0,sensor_count,1):
        line=int(input("enter line"))
        column=int(input("enter column"))
        while not map.valid_move(line,column):
            print("Invalid position!")
            line = int(input("enter line"))
            column = int(input("enter column"))
        sensors.append([line,column])
    max_cost=0
    for i in range(sensor_count+1):
        for j in range(sensor_count+1):
            d=Drone(sensors[i][0],sensors[i][1])
            distances[i][j]=searchGreedy(map,d,sensors[i][0],sensors[i][1],sensors[j][0],sensors[j][1],manhattanHeuristic)
            max_cost=max(max_cost,distances[i][j])

    sol=[]
    bestSol=[[],0]
    trace=[[1 for i in range(sensor_count+1)] for j in range (sensor_count+1)]
    print("Started!")
    for i in range(noEpoch):
        #def epoca(noAnts, size, initial, energy, distances, trace, alpha, beta, q0, rho):
        sol=epoca(noAnts, sensor_count+1,0,energy,distances, trace, alpha, beta, q0, rho,max_cost)
        if len(sol[0])>len(bestSol[0]):
            bestSol[0]=sol[0].copy()
            bestSol[1]=sol[1]
        elif len(sol[0])==len(bestSol[0]) and sol[1] > bestSol[1]:
            bestSol[0]=sol[0].copy()
            bestSol[1]=sol[1]
    print ("Best order in which to parse sensors: ", bestSol[0])


    squares_seen_by_sensors=0
    visions=[[0 for i in range(6)] for j in range (len(sensors))]
    for i in range(len(sensors)):
        for j in range(0,6,1):
            visions[i][j]=map.get_sight(sensors[i][0],sensors[i][1],j)
    energy_left=bestSol[1]


    spent=[0 for i in range(len(sensors))]

    #establish
    while energy_left:
        current_best=-1
        current_best_index=0
        for i in range(1,len(sensors),1):
            if spent[i] <= 4 and (visions[i][spent[i]+1]-visions[i][spent[i]]) > current_best:
                current_best=visions[i][spent[i]+1]-visions[i][spent[i]]
                current_best_index=i
        if current_best==-1:
            break
        energy_left-=1
        spent[current_best_index]+=1
        squares_seen_by_sensors+=current_best

    print("Energy spent on each sensor: ",spent)
    for i in range(1, sensor_count, 1):
        squares_seen_by_sensors=squares_seen_by_sensors+visions[i][spent[i]]
    print("Total squares seen: ", squares_seen_by_sensors)
    path=[]
    travel=bestSol[0]
    for i in range(0,len(sensors)-1,1):
        d=Drone(sensors[travel[i]][0],sensors[travel[i]][1])
        current_path=searchGreedyP(map,d,sensors[travel[i]][0],sensors[travel[i]][1],sensors[travel[i+1]][0],sensors[travel[i+1]][1],manhattanHeuristic)
        for move in current_path:
            path.append(move)

    gui.movingDrone(map,path)






main()






