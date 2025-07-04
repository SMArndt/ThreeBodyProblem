"""
ThreeBodyProblem.py - Copyright 2025 S.M.Arndt, Cavroc Pty Ltd

Three-Body Problem Simulation in 3D
--------------------------------------------
This Python script simulates the motion of three planetary bodies through
gravitational interaction in 3D space. It uses Newtonian mechanics and
integrates their positions and velocities over time using the Euler method.
The simulation is visualized in an animated 3D plot with wall projections.
Author: Mostly ChatGPT, prompt by S.M.Arndt

Visit https://cavroc.com/ for more information on IUCM and StopeX

This is free software: you can redistribute it and/or modify it under the terms
of the GNU General Public License as published by the Free Software Foundation.
It is is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
<https://www.gnu.org/licenses/>.
"""

# ---- Import required libraries ----
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D

# ---- Define gravitational constant G [m^3 kg^-1 s^-2]
G = 6.67430e-11

# ---- Define initial conditions ----

# Masses of the three bodies [kg]
masses = np.array([1.0e27, 1.5e27, 0.55e27])

# Initial positions of the three bodies (in meters)
positions = np.array([
    [ 1e10,     0,     0],   # Body 1 starts on the +x axis
    [-1e10,     0,     0],   # Body 2 starts on the -x axis
    [    0,  1e10,     0]    # Body 3 starts on the +y axis
], dtype=float)

# Initial velocities of the three bodies (in m/s)
velocities = np.array([
    [   10,  1000,  -150],   # Body 1
    [  -20, -1500,   100],   # Body 2
    [ 2000,     0,   250]    # Body 3
], dtype=float)

# ---- Simulation settings ----
dt    = 0.25e4  # Time step for integration (in seconds)
steps = 50000   # Number of time steps

# ---- Positions of each body over time (np.array) ----
trajectories = np.zeros((3, steps, 3))

# ---- Function to compute gravitational accelerations ----
def compute_accelerations(pos):
    acc = np.zeros_like(pos)
    for i in range(3):
        for j in range(3):
            if i != j:
                r = pos[j] - pos[i]                     # Vector from body i to body j
                dist = np.linalg.norm(r)                # Distance between bodies
                acc[i] += G * masses[j] * r / dist**3   # Newton's gravitational law
    return acc

# ---- Main integration loop, updates positions and velocities (Euler method) ----
for t in range(steps):
    trajectories[:, t] = positions                      # Save current positions
    acc = compute_accelerations(positions)              # Compute acceleration
    velocities += acc * dt                              # Update velocities
    positions += velocities * dt                        # Update positions

# ---- Set up plot and visualization ----

# Choose soft pastel colors for the three bodies
colors = ['#87CEEB', '#FFFACD', '#98FF98']  # Sky Blue, Lemon Chiffon, Mint Green

# Create a figure and 3D axes
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Set black background
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

# Make axes and grid white for contrast
ax.tick_params(colors='white')
ax.xaxis.set_pane_color((0.05, 0.05, 0.05, 1.0))
ax.yaxis.set_pane_color((0.05, 0.05, 0.05, 1.0))
ax.zaxis.set_pane_color((0.05, 0.05, 0.05, 1.0))
ax.xaxis._axinfo['grid'].update(color='white')
ax.yaxis._axinfo['grid'].update(color='white')
ax.zaxis._axinfo['grid'].update(color='white')

# Hide tick labels
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_zticklabels([])

# ---- Center and scale the plot based on trajectory bounds ----
all_xyz = trajectories.reshape(-1, 3)
mins = all_xyz.min(axis=0)
maxs = all_xyz.max(axis=0)
center = (mins + maxs) / 2
max_range = (maxs - mins) / 2

# Set axis limits so the simulation is nicely framed
ax.set_xlim(center[0] - max_range[0], center[0] + max_range[0])
ax.set_ylim(center[1] - max_range[1], center[1] + max_range[1])
ax.set_zlim(center[2] - max_range[2], center[2] + max_range[2])

# ---- Create plot objects for animation ----

# Lines: trails of each body
lines = [ax.plot([], [], [], color=colors[i])[0] for i in range(3)]
# Points: moving body locations
points = [ax.plot([], [], [], 'o', color=colors[i])[0] for i in range(3)]
# Projections on Z, Y, X walls
proj_bottom = [ax.plot([], [], [], color=colors[i], alpha=0.25)[0] for i in range(3)]
proj_back   = [ax.plot([], [], [], color=colors[i], alpha=0.25)[0] for i in range(3)]
proj_left   = [ax.plot([], [], [], color=colors[i], alpha=0.25)[0] for i in range(3)]

# ---- Initialization function ----
def init():
    for obj in lines + points + proj_bottom + proj_back + proj_left:
        obj.set_data([], [])
        obj.set_3d_properties([])
    return lines + points + proj_bottom + proj_back + proj_left

# ---- Animation update function ----
def update(frame):
    # Slowly rotate the 3D view for better perspective
    ax.view_init(elev=5 + frame * 0.00025, azim=2.5 + frame * 0.00075)

    # Compute bounding box from all previous points up to current frame
    all_points = trajectories[:, :frame].reshape(-1, 3)
    if all_points.shape[0] > 0:
        x_range = all_points[:, 0]
        y_range = all_points[:, 1]
        z_range = all_points[:, 2]
        zlim = ax.get_zlim3d()
        ylim = ax.get_ylim3d()
        ax.set_xlim(np.min(x_range), np.max(x_range))
        ax.set_ylim(np.min(y_range), ylim[1])  # Lock max y
        ax.set_zlim(zlim[0], np.max(z_range))  # Lock min z

    # Position the projection planes slightly inside the bounding box
    zproj = ax.get_zlim3d()[0] + 0.05 * (ax.get_zlim3d()[1] - ax.get_zlim3d()[0])
    yproj = ax.get_ylim3d()[0] + 0.01 * (ax.get_ylim3d()[1] - ax.get_ylim3d()[0])
    xproj = ax.get_xlim3d()[0] + 0.01 * (ax.get_xlim3d()[1] - ax.get_xlim3d()[0])

    # Update all body positions and projections
    for i in range(3):
        trail = trajectories[i, :frame]
        x, y, z = trail[:, 0], trail[:, 1], trail[:, 2]

        lines[i].set_data(x, y)
        lines[i].set_3d_properties(z)

        if len(x) > 0:
            points[i].set_data([x[-1]], [y[-1]])
            points[i].set_3d_properties([z[-1]])

            proj_bottom[i].set_data(x, y)
            proj_bottom[i].set_3d_properties(np.full_like(z, zproj))

            proj_back[i].set_data(x, np.full_like(y, yproj))
            proj_back[i].set_3d_properties(z)

            proj_left[i].set_data(np.full_like(x, xproj), y)
            proj_left[i].set_3d_properties(z)

    return lines + points + proj_bottom + proj_back + proj_left

# ---- Create animation ----
ani = FuncAnimation(fig, update, frames=range(0, steps, 25), init_func=init, blit=False)

# ---- Save animation (MP4 preferred, fallback to GIF) ----
try:
    from matplotlib.animation import FFMpegWriter
    writer = FFMpegWriter(fps=50, bitrate=12000)
    ani.save("ThreeBody_3Dspin.mp4", writer=writer, dpi=100)
    print("Saved as MP4")
except Exception as e:
    print(f"FFMpeg unavailable or failed ({e}), saving as GIF instead...")
    ani.save("ThreeBody3Dspin.gif", writer=PillowWriter(fps=50), dpi=100)
    print("Saved as GIF")
