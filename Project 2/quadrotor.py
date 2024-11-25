import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter

import matplotlib as mp
import IPython

        


# constant
MASS = 0.500
INERTIA = 0.1
LENGTH = 0.15
DT = 0.04         # integration step
GRAVITY_CONSTANT = 9.81

DIM_STATE = 6
DIM_CONTROL = 2

# Obstacle definition
OBSTACLE_CENTERS = [np.array([0, 2.]), np.array([0., 0.]), np.array([0, -2.])]
OBSTACLE_RADIUS = 0.5 

# x-y target
TARGET = [2, 0]



def next_state(z, u):
    """
    Inputs:
    z: state of the cart pole syste as a numpy array (px , px dot, py , py dot, theta, omega)
    u: 2d control
    
    Output:
    the new state of the pendulum as a numpy array
    """
    x = z[0]
    vx = z[1]
    y = z[2]
    vy = z[3]
    theta = z[4]
    omega = z[5]

    dydt = np.zeros([DIM_STATE,])
    dydt[0] = vx
    dydt[1] = (-(u[0] + u[1]) * np.sin(theta)) / MASS
    dydt[2] = vy
    dydt[3] = ((u[0] + u[1]) * np.cos(theta) - MASS * GRAVITY_CONSTANT) / MASS
    dydt[4] = omega
    dydt[5] = (LENGTH * (u[0] - u[1])) / INERTIA

    z_next = z + dydt * DT
    return z_next



def check_collision(state):
    """
    This function checks if the state is colliding with the obstacles
    
    Inputs:
    state: the current state of the quadrotor as a numpy array (x,vx,y,vy,theta,omega)
    

    Output:
    a boolean value. True if there is contact and False otherwise.
    """
    dist1 = (state[0] - OBSTACLE_CENTERS[0][0]) ** 2 + (state[2] - OBSTACLE_CENTERS[0][1]) ** 2
    dist2 = (state[0] - OBSTACLE_CENTERS[1][0]) ** 2 + (state[2] - OBSTACLE_CENTERS[1][1]) ** 2
    dist3 = (state[0] - OBSTACLE_CENTERS[2][0]) ** 2 + (state[2] - OBSTACLE_CENTERS[2][1]) ** 2
    if dist1 < OBSTACLE_RADIUS + LENGTH:
        return True
    elif dist2 < OBSTACLE_RADIUS + LENGTH:
        return True
    elif dist3 < OBSTACLE_RADIUS + LENGTH:
        return True
    else:
        return False
    


def simulate(z0, controller, horizon_length):
    """
    This function simulates the quadrotor for horizon_length steps from initial state z0
    
    Inputs:
    z0: the initial conditions of the quadrotor as a numpy array (x,vx,y,vy,theta,omega)
    controller: a function that takes a state z as argument and index i of the time step and returns a control u
    horizon_length: the horizon length
    

    Output:
    t[time_horizon+1] contains the simulation time
    z[4xtime_horizon+1] and u[1,time_horizon] containing the time evolution of states and control
    """
    t = np.zeros([horizon_length + 1,])
    z = np.empty([DIM_STATE, horizon_length + 1])
    z[:, 0] = z0
    u = np.zeros([DIM_CONTROL, horizon_length])
    for i in range(horizon_length):
        if check_collision(z[:, i]):
            print("FAILURE: The robot collided with an obstacle")

        u[:, i] = controller(z[:, i], i)
        z[:, i + 1] = next_state(z[:, i], u[:, i])
        t[i + 1] = t[i] + DT
    return t, z, u



def animate_robot(x, u, dt=0.04, save_mp4=False):
    """
    This function makes an animation showing the behavior of the quadrotor
    takes as input the result of a simulation (with dt=0.04s)
    """

    min_dt = 0.04
    if dt < min_dt:
        steps = int(min_dt / dt)
        use_dt = int(np.round(min_dt * 1000))
    else:
        steps = 1
        use_dt = int(np.round(dt * 1000))

    # what we need to plot
    plotx = x[:, ::steps]
    plotx = plotx[:, :-1]
    plotu = u[:, ::steps]

    fig = mp.figure.Figure(figsize=[8.5, 8.5])
    mp.backends.backend_agg.FigureCanvasAgg(fig)
    ax = fig.add_subplot(111, autoscale_on=False, xlim=[-4, 4], ylim=[-4, 4])
    ax.grid()

    list_of_lines = []

    # create the robot
    # the main frame
    (line,) = ax.plot([], [], "k", lw=6)
    list_of_lines.append(line)
    # the left propeller
    (line,) = ax.plot([], [], "b", lw=4)
    list_of_lines.append(line)
    # the right propeller
    (line,) = ax.plot([], [], "b", lw=4)
    list_of_lines.append(line)
    # the left thrust
    (line,) = ax.plot([], [], "r", lw=1)
    list_of_lines.append(line)
    # the right thrust
    (line,) = ax.plot([], [], "r", lw=1)
    list_of_lines.append(line)

    circle1 = plt.Circle((OBSTACLE_CENTERS[0][0], OBSTACLE_CENTERS[0][1]), OBSTACLE_RADIUS, color='k')
    circle2 = plt.Circle((OBSTACLE_CENTERS[1][0], OBSTACLE_CENTERS[1][1]), OBSTACLE_RADIUS, color='k')
    circle3 = plt.Circle((OBSTACLE_CENTERS[2][0], OBSTACLE_CENTERS[2][1]), OBSTACLE_RADIUS, color='k')
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    ax.add_patch(circle3)


    circle1 = plt.Circle((TARGET[0], TARGET[1]), 0.04, color='red')
    ax.add_patch(circle1)
    ax.add_patch(circle2)

    def _animate(i):
        for l in list_of_lines:  # reset all lines
            l.set_data([], [])

        theta = plotx[4, i]
        x = plotx[0, i]
        y = plotx[2, i]
        trans = np.array([[x, x], [y, y]])
        rot = np.array(
            [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]
        )

        main_frame = np.array([[-LENGTH, LENGTH], [0, 0]])
        main_frame = rot @ main_frame + trans

        left_propeller = np.array(
            [[-1.3 * LENGTH, -0.7 * LENGTH], [0.1, 0.1]]
        )
        left_propeller = rot @ left_propeller + trans

        right_propeller = np.array(
            [[1.3 * LENGTH, 0.7 * LENGTH], [0.1, 0.1]]
        )
        right_propeller = rot @ right_propeller + trans

        left_thrust = np.array(
            [[LENGTH, LENGTH], [0.1, 0.1 + plotu[0, i] * 0.04]]
        )
        left_thrust = rot @ left_thrust + trans

        right_thrust = np.array(
            [[-LENGTH, -LENGTH], [0.1, 0.1 + plotu[0, i] * 0.04]]
        )
        right_thrust = rot @ right_thrust + trans

        list_of_lines[0].set_data(main_frame[0, :], main_frame[1, :])
        list_of_lines[1].set_data(left_propeller[0, :], left_propeller[1, :])
        list_of_lines[2].set_data(right_propeller[0, :], right_propeller[1, :])
        list_of_lines[3].set_data(left_thrust[0, :], left_thrust[1, :])
        list_of_lines[4].set_data(right_thrust[0, :], right_thrust[1, :])

        return list_of_lines

    def _init():
        return _animate(0)

    ani = mp.animation.FuncAnimation(
        fig,
        _animate,
        np.arange(0, len(plotx[0, :])),
        interval=use_dt,
        blit=True,
        init_func=_init,
    )
    
    plt.close(fig)
    plt.close(ani._fig)
    
    if save_mp4:
        # Create an instance of FFMpegWriter
        writer = FFMpegWriter(fps=int(1/dt))
        
        # Save the animation
        ani.save('./animation.mp4', writer=writer)

    IPython.display.display_html(IPython.core.display.HTML(ani.to_html5_video()))

    

