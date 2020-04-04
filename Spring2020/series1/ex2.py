#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 21:59:08 2020

@author: y56
"""
 
def dp_solver(N): 
    def x_next(x,u):
        return x+u
    def cost_to_go(x_k,u_k):
        if abs(x_next(x_k, u_k))>4:
            return float('inf')
        return (x_k+4)**2#+u_k**2
    def final_cost(x_N):
#        if x_N==0:
#            return 0
#        return float('inf')
        return 0
    def cost_from_to(this_x, next_x):
        u = next_x - this_x
        if abs(u)>2:
            return float('inf')
        return (this_x+4)**2+u**2
    
    possible_x  = list(range(-4,5))
    control_chart = [x[:] for x in [[None] * 9] * (N)] 
    dp_cost_chart = [x[:] for x in [[None] * 9] * (N+1)] 
    
    for x_N in possible_x:
        dp_cost_chart[N][x_N+4] = final_cost(x_N)
        
    for n in range(N-1,-1,-1):
        for this_x in possible_x:
            cur_min_cost = float('inf')
            best_control = None
            for next_x in possible_x:
                tmp_cost = cost_from_to(this_x, next_x) + dp_cost_chart[n+1][next_x+4]
                
                if cur_min_cost > tmp_cost:
                    cur_min_cost = tmp_cost
                    best_control = next_x - this_x
                
            control_chart[n][this_x+4] = best_control
            dp_cost_chart[n][this_x+4] = cur_min_cost
    
    return dp_cost_chart, control_chart
    
N = 15
dp_cost_chart, control_chart = dp_solver(N)
print("cost to go")
for ele in dp_cost_chart:
    print(ele)
print("optimal controls")
for ele in control_chart:
    print(ele)


state=[0] # initial state
control=[]
i=0
while len(state)<16:
    now =  state[-1]
    state.append(now + control_chart[i][now+4])
    control.append(control_chart[i][now+4])
    i+=1

print(state)
print(control)

state=[1] # initial state
control=[]
i=0
while len(state)<16:
    now =  state[-1]
    state.append(now + control_chart[i][now+4])
    control.append(control_chart[i][now+4])
    i+=1

print(state)
print(control)

state=[-4] # initial state
control=[]
i=0
while len(state)<16:
    now =  state[-1]
    state.append(now + control_chart[i][now+4])
    control.append(control_chart[i][now+4])
    i+=1

print(state)
print(control)