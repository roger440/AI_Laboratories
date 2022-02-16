import torch
import math
from numpy import random
def get_function_value(x1,x2):
    return float(torch.sin_(x1 + (x2/math.pi)))

def fill_database():
    #create 1000 touples of x1 and x2 and compute their f associated value
    with open("database.txt",'w') as f:
        x1list=torch.randint(-10000000,10000000,(1000,))
        x2list=torch.randint(-10000000,10000000,(1000,))
        for i in range(0,1000,1):
            x1=x1list[i]


            x2=x2list[i]

            function_value=float(get_function_value(x1/1000000,x2/1000000))
            f.write(str(int(x1)/1000000) + ',' + str(int(x2)/1000000) + ',' + str(function_value) +'\n')



def get_data():
    data=[]
    with open("database.txt", 'r') as f:
        for line in f:
            line=line.split(',')
            row=[]
            row.append(float(line[0]))
            row.append(float(line[1]))
            row.append(float(line[2]))
            data.append(row)
    return data


fill_database()