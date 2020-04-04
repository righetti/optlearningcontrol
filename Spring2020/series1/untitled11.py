#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 20:28:10 2020

@author: y56
"""

def x_next(x,u):
    if -2 <= -x+1+u and -x+1+u <= 2:
        return -x+1+u
    if -x+1+u > 2:
        return 2
    return -2

dict_need_control_for = {}

x_l = [-2, -1, 0, 1, 2]
u_l = [-1, 0, 1]
for x in x_l:
    for u in u_l:
        print(x, x_next(x,u))
        if (x, x_next(x,u)) in dict_need_control_for:
            if abs(u) < abs(dict_need_control_for[(x, x_next(x,u))]):
                dict_need_control_for[(x, x_next(x,u))] = u
        else:
            dict_need_control_for[(x, x_next(x,u))] = u

#{(-2, 2): [-1, 0, 1],
# (-1, 1): [-1],
# (-1, 2): [0, 1],
# (0, 0): [-1],
# (0, 1): [0],
# (0, 2): [1],
# (1, -1): [-1],
# (1, 0): [0],
# (1, 1): [1],
# (2, -2): [-1],
# (2, -1): [0],
# (2, 0): [1]}