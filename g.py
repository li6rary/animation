import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Set up the figure and axis
fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Set up the ball
ball = plt.Circle((5, 5), 0.5, fc='r')
ax.add_patch(ball)

# Define the physics of the ball's motion
g = 9.81  # m/s^2
t = np.linspace(0, 10, 1000)
y = 5 - 0.5 * g * t**2

# Define the animation function
def animate(i):
    ball.center = (5, y[i])
    return ball,

# Create the animation object
ani = animation.FuncAnimation(fig, animate, frames=len(t), interval=10)

# Show the animation
plt.show()