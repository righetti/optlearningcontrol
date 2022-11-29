# a few packages we need to import

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation
import IPython 

NUMBER_STATES = 2
NUMBER_CONTROLS = 1

MAX_VELOCITY = 6.

DELTA_T = 0.1

## internal constants - DO NOT USE
_INTERNAL_DT = 0.01
_INTEGRATION_RATIO = 10
_GRAVITY = 9.81


def get_next_state(x,u):
    """
    This function integrates the pendulum for one step of DELTA_T seconds

    Inputs:
    x: state of the pendulum (theta,omega) as a 2D numpy array
    u: control as a scalar

    Output:
    the state of the pendulum as a 2D numpy array at the end of the integration
    """
    x_next = x[0]
    v_next = x[1]
    for i in range(_INTEGRATION_RATIO):
        xx_next = (x_next + _INTERNAL_DT * v_next)%(2*np.pi)
        v_next = np.clip(v_next + _INTERNAL_DT * (u-_GRAVITY*np.sin(x_next)-0.2*v_next), -MAX_VELOCITY, MAX_VELOCITY)
        x_next = xx_next
    return np.array([x_next,v_next])


def simulate(x0, policy, T):
    """
    This function simulates the pendulum for T seconds from initial state x0 using a policy (i.e. a function of x). It means that policy is called as policy(x) and returns one control)

    Inputs:
    x0: the initial conditions of the pendulum as a 2D array (angle and velocity)
    policy: a function that get a state as an input and return a scalar
    T: the time to integrate for

    Output:
    x (2D array) and u (1D array) containing the time evolution of states and control
    """
    horizon_length = int(T/DELTA_T)
    x=np.empty([2, horizon_length+1])
    x[:,0] = x0
    u=np.empty([horizon_length])
    t = np.zeros([horizon_length+1])
    for i in range(horizon_length):
        u[i] = policy(x[:,i])
        x[:,i+1] = get_next_state(x[:,i], u[i])
        t[i+1] = t[i] + DELTA_T
    return t, x, u


def animate_robot(x):
    """
    This function makes an animation showing the behavior of the pendulum
    takes as input the result of a simulation - dt is the sampling time (0.1s normally)
    """

    # here we check if we need to down-sample the data for display
    #downsampling (we want 100ms DT or higher)
    steps = 1
    use_dt = int(DELTA_T * 1000)
    plotx = x[:,::steps]

    fig = matplotlib.figure.Figure(figsize=[6,6])
    matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
    ax = fig.add_subplot(111, autoscale_on=False, xlim=[-1.3,1.3], ylim=[-1.3,1.3])
    ax.grid()

    list_of_lines = []

    #create the cart pole
    line, = ax.plot([], [], 'k', lw=2)
    list_of_lines.append(line)
    line, = ax.plot([], [], 'o', lw=2)
    list_of_lines.append(line)

    def animate(i):
        for l in list_of_lines: #reset all lines
            l.set_data([],[])

        x_pend = np.sin(plotx[0,i])
        y_pend = -np.cos(plotx[0,i])

        list_of_lines[0].set_data([0., x_pend], [0., y_pend])
        list_of_lines[1].set_data([x_pend, x_pend], [y_pend, y_pend])

        return list_of_lines

    def init():
        return animate(0)


    ani = animation.FuncAnimation(fig, animate, np.arange(0, len(plotx[0,:])),
        interval=use_dt, blit=True, init_func=init)
    plt.close(fig)
    plt.close(ani._fig)
    IPython.display.display_html(IPython.core.display.HTML(ani.to_html5_video()))