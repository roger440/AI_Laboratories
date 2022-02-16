# -*- coding: utf-8 -*-
from util import *
"""
In this file your task is to write the solver function!

"""


def compute_fuzzy_triangle(value, left, right, mean=None):
    if mean is None:
        mean=(left+right)/2
    if left is not None and left <= value < mean:
        return (value-left) / (mean-left)
    elif right is not None and mean <= value < right:
        return (right - value ) / (right - mean)
    else:
        return 0

def get_fuzzy_values(t,ranges):
    fuzzy_values=dict()
    for key,value in ranges.items():
        if len(value)==2:
            #we are not given a mean
            fuzzy_values[key]=compute_fuzzy_triangle(t,value[0],value[1])
        elif len(value)==3:
            fuzzy_values[key]=compute_fuzzy_triangle(t,value[0],value[1],value[2])
    return fuzzy_values

def solver(t,w):
    """
    Parameters
    ----------
    t : TYPE: float
        DESCRIPTION: the angle theta
    w : TYPE: float
        DESCRIPTION: the angular speed omega

    Returns
    -------
    F : TYPE: float
        DESCRIPTION: the force that must be applied to the cart
    or
    
    None :if we have a division by zero

    """
    #The first step is to compute the membership degrees for t and w

    #add the values one by one
    theta_degrees=get_fuzzy_values(t,thetaRanges)
    omega_degrees=get_fuzzy_values(w,omegaRanges)

    degree_F = {}

    for thetaSet in fuzzyTable:

        for omegaSet, fSet in fuzzyTable[thetaSet].items(): # omegaSet = key, fSet = values

            # we take the minimum of the membership values of the index set
            value = min(theta_degrees[thetaSet], omega_degrees[omegaSet])
            if fSet not in degree_F:
                degree_F[fSet] = value
            else:
                # The membership degree of F to each class will be the maximum value for that class taken from the rules’ table
                degree_F[fSet] = max(value, degree_F[fSet])
    print(degree_F)

    s = sum(degree_F.values())
    if s == 0:
        return None

    # defuzzify the results for F using a weighted average of the membership degrees
    # and the b values of the sets
    F = 0
    for fSet in degree_F.keys():
        F += degree_F[fSet] * vectors[fSet]
    F /= s

    return F

solver(5,5)