import numpy as np
import matplotlib.pyplot as plt

import matplotlib
from matplotlib.animation import Animation, FuncAnimation
import IPython

# definition of the matrices and example of control
g = 9.81
integration_dt = 0.01
dt = 0.1

def step(x,u):
    """
    this function return x_n+1 given x and u
    """
    for i in range(10):
        x_next = (x[0] + integration_dt * x[1])%(2*np.pi)
        v_next = np.clip(x[1] + integration_dt * (u-g*np.sin(x[0])), -6.,6.)
        x = np.array([x_next,v_next])
    return x

def animate_robot(x0, controller, push = False, save_movie = False):
    """
    This function makes an animation showing the behavior of the pendulum
    takes as input the result of a simulation - dt is the sampling time (0.1s normally)
    """
    N = 100
    assert(x0.shape[0]==2)
    x = np.zeros((2,N))
    x[:,0] = x0[:,0]
    for i in range(N-1):
        u = controller(x[:,i])
        x[:,i+1] = step(x[:,i],u)
        if push and (i == 45 or i == 70):
            x[1,i+1] = 4*np.pi*(np.random.rand(1) - 0.5)
        
    # here we check if we need to down-sample the data for display
    #downsampling (we want 100ms DT or higher)
    min_dt = 0.1
    if(dt < min_dt):
        steps = int(min_dt/dt)
        use_dt = int(min_dt * 1000)
    else:
        steps = 1
        use_dt = int(dt * 1000)
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

    cart_height = 0.25

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


    ani = FuncAnimation(fig, animate, np.arange(0, len(plotx[0,:])),
        interval=use_dt, blit=True, init_func=init)
    if save_movie:
        ani.save('pendulum_movie.mp4')
    plt.close(fig)
    plt.close(ani._fig)
    IPython.display.display_html(IPython.core.display.HTML(ani.to_html5_video()))
