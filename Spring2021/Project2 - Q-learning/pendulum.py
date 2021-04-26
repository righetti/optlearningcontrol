# a few packages we need to import

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation
import IPython 


class Pendulum:
    """
    This class describes an inverted pendulum and provides some helper functions
    """
    
    def __init__(self):
        """
        constructor of the class
        """
        #gravity constant
        self.g=9.81
        
        # number of dimensions (angle and angular velocity)
        self.state_dims = 2
        
        # the maximum velocity
        self.vmax = 6.
        # the range of allowable states
        self.state_range = np.array([[0, 2*np.pi],[-self.vmax, self.vmax]])

        #simulation step
        self.delta_t = 0.1
        # internal integration step
        self._internaldt = 0.01
        self._integration_ratio = int(round(self.delta_t / self._internaldt))
        
    def next_state(self,x,u):
        """
        This function integrates the pendulum for one step of self.delta_t seconds
        
        Inputs:
        x: state of the pendulum (x,v) as a 2D numpy array
        u: control as a scalar
        
        Output:
        the state of the pendulum as a 2D numpy array at the end of the integration
        """
        x_next = x[0]
        v_next = x[1]
        for i in range(self._integration_ratio):
            xx_next = (x_next + self._internaldt * v_next)%(2*np.pi)
            v_next = np.clip(v_next + self._internaldt * (u-self.g*np.sin(x_next)), -self.vmax, self.vmax)
            x_next = xx_next
        return np.array([x_next,v_next])
    
    def simulate(self, x0, policy, T):
        """
        This function simulates the pendulum for T seconds from initial state x0 using a policy
        (policy is called as policy(x) and returns one control)
        
        Inputs:
        x0: the initial conditions of the pendulum as a 2D array (angle and velocity)
        T: the time to integrate for
        
        Output:
        x (2D array) and u (1D array) containing the time evolution of states and control
        """
        horizon_length = int(T/self.delta_t)
        x=np.empty([2, horizon_length+1])
        x[:,0] = x0
        u=np.empty([horizon_length])
        for i in range(horizon_length):
            u[i] = policy(x[:,i])
            x[:,i+1] = self.next_state(x[:,i], u[i])
        return x, u
    
    def animate_robot(self, x, dt = 0.01):
        """
        This function makes an animation showing the behavior of the pendulum
        takes as input the result of a simulation - dt is the sampling time (0.1s normally)
        """

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


        ani = animation.FuncAnimation(fig, animate, np.arange(0, len(plotx[0,:])),
            interval=use_dt, blit=True, init_func=init)
        plt.close(fig)
        plt.close(ani._fig)
        IPython.display.display_html(IPython.core.display.HTML(ani.to_html5_video()))