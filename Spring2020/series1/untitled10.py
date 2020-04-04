#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 20:19:53 2020

@author: y56
"""
def x_next(x,u):
    def x_next_03(x,u):
        if -2 <= -x+0+u and -x+1+u <= 2:
            return -x+0+u
        if -x+0+u > 2:
            return 2
        return -2
    def x_next_07(x,u):
        if -2 <= -x+1+u and -x+1+u <= 2:
            return -x+1+u
        if -x+1+u > 2:
            return 2
        return -2
#    print(0.3*x_next_03(x,u), 0.7*x_next_03(x,u))
    return 0.3*x_next_03(x,u)+ 0.7*x_next_03(x,u)
def cost(x_k,u_k):
        return 2*abs(x_k) + abs(u_k)

for x0 in [-2,-1,0,1,2]:
    collect = []
    cur_min_total_cost = float('inf')
    for u0 in [-1, 0, 1]:
        for u1 in [-1, 0, 1]:
            for u2 in [-1, 0, 1]:
                    x1 = x_next(x0, u0)
                    x2 = x_next(x1, u1)
                    x3 = x_next(x2, u2)
                    total_cost = cost(x0, u0)+cost(x1, u1)+cost(x2, u2)+x3**2
                    collect.append([(x0,x1,x2,x3),(u0,u1,u2),total_cost])
                    if total_cost < cur_min_total_cost:
                        ind = len(collect) - 1
                        cur_min_total_cost = total_cost    
#    for ele in collect:
#        print(ele)
#    print(ind)
    print(collect[ind])