import numpy as np
import matplotlib.pyplot as plt

import matplotlib as mp
from matplotlib.animation import Animation, FuncAnimation
import IPython

# definition of the matrices and example of control
m = 0.5
I = 0.1
r = 0.15
g = 9.81
dt = 0.01
length = 0.15

A = np.eye(6)
A[0,1] = dt
A[1,4] = -g * dt
A[2,3] = dt
A[4,5] = dt

B = np.zeros((6,2))
B[3,0] = dt/m
B[3,1] = dt/m
B[5,0] = length * dt/I
B[5,1] = -length * dt/I



def animate_robot(x0, u, goal):
    """
    This function makes an animation showing the behavior of the quadrotor
    takes as input the result of a simulation (with dt=0.01s)
    """

    assert(u.shape[0]==2)
    assert(x0.shape[0]==6)
    N = u.shape[1] + 1
    x = np.zeros((6,N))
    x[:,0] = x0[:,0]
    for i in range(N-1):
        x[:,i+1] = A @ x[:,i] + B @ u[:,i]
        
    min_dt = 0.1
    if(dt < min_dt):
        steps = int(min_dt/dt)
        use_dt = int(np.round(min_dt * 1000))
    else:
        steps = 1
        use_dt = int(np.round(dt * 1000))

    #what we need to plot
    plotx = x[:,::steps]
    plotx = plotx[:,:-1]
    plotu = u[:,::steps]

    fig = mp.figure.Figure(figsize=[6,6])
    mp.backends.backend_agg.FigureCanvasAgg(fig)
    ax = fig.add_subplot(111, autoscale_on=False, xlim=[-4,4], ylim=[-4,4])
    ax.grid()

    list_of_lines = []

    #create the robot
    # the main frame
    line, = ax.plot([], [], 'k', lw=6)
    list_of_lines.append(line)
    # the left propeller
    line, = ax.plot([], [], 'b', lw=4)
    list_of_lines.append(line)
    # the right propeller
    line, = ax.plot([], [], 'b', lw=4)
    list_of_lines.append(line)
    # the left thrust
    line, = ax.plot([], [], 'r', lw=1)
    list_of_lines.append(line)
    # the right thrust
    line, = ax.plot([], [], 'r', lw=1)
    list_of_lines.append(line)
    # the goal
    ax.plot([goal[0]], [goal[1]], 'og', lw=2)
    
    def _animate(i):
        for l in list_of_lines: #reset all lines
            l.set_data([],[])

        theta = plotx[4,i]
        x = plotx[0,i]
        y = plotx[2,i]
        trans = np.array([[x,x],[y,y]])
        rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

        main_frame = np.array([[-length, length], [0,0]])
        main_frame = rot @ main_frame + trans 
        
        left_propeller = np.array([[-1.3 * length, -0.7*length], [0.1,0.1]])
        left_propeller = rot @ left_propeller + trans
        
        right_propeller = np.array([[1.3 * length, 0.7*length], [0.1,0.1]])
        right_propeller = rot @ right_propeller + trans
        
        left_thrust = np.array([[length, length], [0.1, 0.1+plotu[0,i]*0.04]])
        left_thrust = rot @ left_thrust + trans
        
        right_thrust = np.array([[-length, -length], [0.1, 0.1+plotu[0,i]*0.04]])
        right_thrust = rot @ right_thrust + trans

        list_of_lines[0].set_data(main_frame[0,:], main_frame[1,:])
        list_of_lines[1].set_data(left_propeller[0,:], left_propeller[1,:])
        list_of_lines[2].set_data(right_propeller[0,:], right_propeller[1,:])
        list_of_lines[3].set_data(left_thrust[0,:], left_thrust[1,:])
        list_of_lines[4].set_data(right_thrust[0,:], right_thrust[1,:])

        return list_of_lines

    def _init():
        return _animate(0)


    ani = FuncAnimation(fig, _animate, np.arange(0, len(plotx[0,:])),
        interval=use_dt, blit=True, init_func=_init)
    plt.close(fig)
    plt.close(ani._fig)
    IPython.display.display_html(IPython.core.display.HTML(ani.to_html5_video()))
