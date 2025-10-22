import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import IPython

L1, L2, L3 = 1.0, 0.8, 0.6          # link lengths (m)


def forward_kinematics(theta):
    th1, th2, th3 = theta
    p0 = np.array([0.0, 0.0])
    p1 = p0 + L1 * np.array([np.cos(th1), np.sin(th1)])
    p2 = p1 + L2 * np.array([np.cos(th1+th2), np.sin(th1+th2)])
    p3 = p2 + L3 * np.array([np.cos(th1+th2+th3), np.sin(th1+th2+th3)])
    return p3


def next_state(state, u, dt=0.01):
    return state + dt * u


def simulate(x0, controller, N_steps, dt=0.01):
    t = np.zeros([N_steps + 1,])
    states = np.zeros((3, N_steps+1))
    control = np.zeros((3, N_steps))
    states[:, 0] = x0
    for i in range(N_steps):
        if callable(controller):
            u = controller(states[:,i])
        else:
            u = controller[:,i]
        control[:, i] = u
        states[:, i+1] = next_state(states[:,i], u)
        t[i+1] = t[i] + dt
        
    return t, states, control


# ----------------------------------------------------------------------
# Animation --------------------------------------------------------------
# ----------------------------------------------------------------------
def animate_robot(traj):
    # Prepare Matplotlib figure
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    ax.grid(True, which='both', ls='--', lw=0.5)

    reach = L1 + L2 + L3
    ax.set_xlim(-reach-0.2, reach+0.2)
    ax.set_ylim(-reach-0.2, reach+0.2)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('3‑DOF Planar Manipulator – Dynamic Simulation')

    line, = ax.plot([], [], '-o', lw=3, markersize=8,
                    markerfacecolor='orange', color='steelblue')
    txt = ax.text(0.02, 0.95, '', transform=ax.transAxes,
                  verticalalignment='top')

    states = traj[:,0::5]

    # Animation callback
    def init():
        line.set_data([], [])
        txt.set_text('')
        return line, txt

    def update(frame):
        def FK(theta):
            th1, th2, th3 = theta
            p0 = np.array([0.0, 0.0])
            p1 = p0 + L1 * np.array([np.cos(th1), np.sin(th1)])
            p2 = p1 + L2 * np.array([np.cos(th1+th2), np.sin(th1+th2)])
            p3 = p2 + L3 * np.array([np.cos(th1+th2+th3), np.sin(th1+th2+th3)])
            return np.vstack([p0, p1, p2, p3])

        q = states[:3, frame]
        pts = FK(q)
        line.set_data(pts[:, 0], pts[:, 1])

        # Show current joint angles (degrees) and torques
        # tau = control_torque(q, states[frame, 3:], times[frame])
        deg = np.degrees(q)
        txt.set_text(
            f'θ₁={deg[0]:.1f}°, θ₂={deg[1]:.1f}°, θ₃={deg[2]:.1f}°, tip=({pts[3,0]:.1f},{pts[3,1]:.1f})'
        )
        return line, txt

    ani = FuncAnimation(fig, update, frames=states.shape[1],
                        init_func=init, blit=True, interval=0.05*1000,
                        repeat=False)

    plt.close(fig)
    plt.close(ani._fig)
    IPython.display.display_html(IPython.core.display.HTML(ani.to_html5_video()))

