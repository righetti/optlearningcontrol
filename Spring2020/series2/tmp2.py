#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 22:41:49 2020

@author: y56
"""

# THIS CODE IS MODIFIED FROM PROFESSOR 2019'S CODE
import numpy as np
import matplotlib.pyplot as plt
v
HORIZON_LENGTH = 100
def solve_ricatti_equations(A,B,Q,R,HORIZON_LENGTH):
    """
    This function solves the backward Riccatti equations for regulator problems of the form
    min sum(xQx + uRu) + xQx subject to xn+1 = Axn + Bun
    
    Arguments:
    A, B, Q, R: numpy arrays defining the problem
    HORIZON_LENGTH: length of the horizon
    
    Returns:
    P: list of numpy arrays containing Pn from 0 to N
    K: list of numpy arrays containing Kn from 0 to N-1
    """
    P = [] #will contain the list of Ps from N to 0
    K = [] #will contain the list of Ks from N-1 to 0

    P.append(Q) #PN
    
    for i in range(HORIZON_LENGTH):
        Knew = -1.0 * np.linalg.inv(B.transpose().dot(P[i]).dot(B) + R).dot(B.transpose()).dot(P[i]).dot(A)
        Pnew = Q + A.transpose().dot(P[i]).dot(A) + A.transpose().dot(P[i]).dot(B).dot(Knew)
        K.append(Knew)
        P.append(Pnew)
    
    return P[::-1],K[::-1]

def calculate_system_no_controller(A,B,x0,K):
    """
    This function calculates the state xn for each step with 0 control
    xn+1 = Axn 
    un=Kn*xn
    Arguments:
    A, B, x0, K 
    
    Returns:
    X: list of numpy arrays containing states xn from 0 to N
    time: list of numpy arrays containing time step from 0 to N
    """
    X=np.zeros([x0.size,HORIZON_LENGTH])
    xn=x0
    time=[]
    for i in range(HORIZON_LENGTH):
        X[:, i] = xn
        xn=A.dot(xn)
        time.append(i)
    return X, time
def calculate_system(A,B,x0,K):
    X=np.zeros([x0.size,HORIZON_LENGTH])
    u=[]
    xn=x0
    time=[]
    for i in range(HORIZON_LENGTH):
        X[:, i] = xn
        u.append(K[i].dot(xn))
        xn=A.dot(xn)+ B.dot(K[i].dot(xn))
        time.append(i)
    return X, u,time

def check_controllability(A,B):
    c=np.concatenate([B, np.dot(A, B), np.dot(A, A).dot(B)], axis=1)
    R=np.linalg.matrix_rank(c)
    print('rank is',R)
    if R< np.linalg.matrix_rank(A):
        print('is not controllable')
    else:print('is controllable')

def plot_x(time, X, X_no_contrl):
    plt.figure()
    plt.plot(time,X[0,:])
    plt.plot(time,X[1,:])
    plt.plot(time,X[2,:])
    plt.title('With optimal controller')
    plt.ylabel('x')
    plt.figure()
    plt.plot(time,X_no_contrl[0,:])
    plt.plot(time,X_no_contrl[1,:])
    plt.plot(time,X_no_contrl[2,:])
    plt.title('No controller')
    plt.ylabel('x')
    plt.xlabel('Time')
    plt.show()

def main():
    # optimal gain
    # simulate uncontrolled and controlled system x0 = [10, 10, 10]
    # plot time evolution of xn and un
    # system a
    Q=100*np.eye(3)
    R=np.eye(1)
    A1=np.array([[0.5,0.,0.5],[0.,0.,-2],[4.,2.,1.]])
    B1=np.array([[0., 0.],[1., 0.],[0., 1.]])
    check_controllability(A1,B1)
    HORIZON_LENGTH=100
    x0=np.array([10.,10.,10.])
    P1,K1=solve_ricatti_equations(A1, B1, Q, R, HORIZON_LENGTH)
    X, u,time=calculate_system(A1,B1,x0,K1)
    X_no_contrl,time=calculate_system_no_controller(A1,B1,x0,K1)
    plt.figure(figsize=(6, 6.5))
    plt.subplots_adjust(wspace =0, hspace =0.5)
    plot_x(time, X, X_no_contrl)

    # system b
    Q=100*np.eye(3)
    R=np.eye(1)
    A1=np.array([[0.5,0.,0.5],[0.,0.,-0.5],[0.5, 0.5, 0.5]])
    B1=np.array([[0., 0.],[1., 0.],[0., 1.]])
    check_controllability(A1,B1)
    HORIZON_LENGTH=100
    x0=np.array([10.,10.,10.])
    P1,K1=solve_ricatti_equations(A1, B1, Q, R, HORIZON_LENGTH)
    X, u,time=calculate_system(A1,B1,x0,K1)
    X_no_contrl,time=calculate_system_no_controller(A1,B1,x0,K1)
    plt.figure(figsize=(6, 6.5))
    plt.subplots_adjust(wspace =0, hspace =0.5)
    plot_x(time, X, X_no_contrl)

    # system C
    Q=100*np.eye(3)
    R=np.eye(1)
    A1=np.array([[2,0.,0],[0.,0.,-2],[1.,1.,0.]])
    B1=np.array([[0., 0.],[1., 0.],[0., 1.]])
    check_controllability(A1,B1)
    HORIZON_LENGTH=100
    x0=np.array([10.,10.,10.])
    P1,K1=solve_ricatti_equations(A1, B1, Q, R, HORIZON_LENGTH)
    X, u,time=calculate_system(A1,B1,x0,K1)
    X_no_contrl,time=calculate_system_no_controller(A1,B1,x0,K1)
    plt.figure(figsize=(6, 6.5))
    plt.subplots_adjust(wspace =0, hspace =0.5)
    plot_x(time, X, X_no_contrl)

if __name__ == "__main__":
    main()