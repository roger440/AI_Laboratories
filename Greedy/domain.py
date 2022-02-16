from constants import *
from random import *
import numpy as np
class Drone():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.roadGreedy = {}
        self.roadAStar = {}
        self.actualCosts = {}

class Map():
    def __init__(self, n=20, m=20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))
        self.sensors=[]

    def randomMap(self, fill=0.15):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

    def add_sensor(self, x,y):
        self.sensors.append([x,y])

    def get_neighbours(self, xi, yi):
        possibilities = [(xi + 1, yi), (xi - 1, yi), (xi, yi + 1), (xi, yi - 1)]

        # squares have coordinates between 0 and 19
        first_cut = list(filter(lambda t: (0 <= t[0] <= 19 and 0 <= t[1] <= 19), possibilities))

        return list(filter(lambda t: (self.surface[t[0]][t[1]] == 0 or self.surface[t[0]][t[1]] >= 2), first_cut))

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def valid_move(self,x,y):
        if x>=0 and x<=19 and y>=0 and y<=19 and self.surface[x][y]==0:
            return True
        return False

    def get_sight(self,x,y,energy):
        vision=0

        auxX=x-1
        auxEnergy=energy
        #look up until we find wall or end of map
        while auxX>=0 and self.surface[auxX][y]==0 and auxEnergy:
            vision+=1
            auxX-=1
            auxEnergy-=1

        #look down until we find wall or end of map
        auxX=x+1

        auxEnergy = energy
        while auxX <=19 and self.surface[auxX][y]==0 and auxEnergy:
            vision+=1
            auxX+=1
            auxEnergy-=1

        #look left

        auxY=y-1

        auxEnergy = energy
        while auxY >=0 and self.surface[x][auxY]==0 and auxEnergy:
            vision+=1
            auxY-=1
            auxEnergy-=1

        #look right

        auxY=y+1
        auxEnergy = energy
        while auxY <=19 and self.surface[x][auxY]==0 and auxEnergy:
            vision+=1
            auxY+=1
            auxEnergy-=1

        return vision


class ant:
    def __init__(self, initial,energy,size):
        # constructor pentru clasa ant
        self.initial=initial
        self.path=[]
        self.path.append(initial)
        self.energy=energy
        self.size=size



    def nextMoves(self, current_sensor_index ,distances):
        # returneaza o lista de posibile mutari corecte de la pozitia a
        new = []
        for j in range(0,self.size,1):
            if j not in self.path and distances[current_sensor_index][j] < self.energy:
                new.append(j)

        return new.copy()

    def distMove(self, a,distances,max_cost):
        return max_cost-distances[self.path[len(self.path)-1]][a]

    def addMove(self, q0, trace, alpha, beta,distances,max_cost):
        # adauga o noua pozitie in solutia furnicii daca este posibil
        p = [0 for i in range(self.size)]
        current_pos=self.path[len(self.path)-1]
        # pozitiile ce nu sunt valide vor fi marcate cu zero
        nextSteps = self.nextMoves(self.path[len(self.path) - 1], distances).copy()
        # determina urmatoarele pozitii valide in nextSteps
        # daca nu avem astfel de pozitii iesim
        if (len(nextSteps) == 0):
            return False
        # punem pe pozitiile valide valoarea distantei empirice
        for i in nextSteps:
            p[i] = self.distMove(i,distances,max_cost)
        # calculam produsul trace^alpha si vizibilitate^beta
        p = [(p[i] ** beta) * (trace[self.path[-1]][i] ** alpha) for i in range(len(p))]
        if (random() < q0):
            # adaugam cea mai buna dintre mutarile posibile
            p = [[i, p[i]] for i in range(len(p))]
            p = max(p, key=lambda a: a[1])
            self.path.append(p[0])
            self.energy=self.energy-distances[current_pos][p[0]]
        else:
            # adaugam cu o probabilitate un drum posibil (ruleta)
            s = sum(p)
            if (s == 0):
                return choice(nextSteps)
            p = [p[i] / s for i in range(len(p))]
            p = [sum(p[0:i + 1]) for i in range(len(p))]
            r = random()
            i = 0
            while (r > p[i]):
                i = i + 1
            self.path.append(i)
            self.energy = self.energy - distances[current_pos][i]
        return True
    def fitness(self):
        # un drum e cu atat mai bun cu cat este mai lung
        return (self.size-len(self.path)+2)
