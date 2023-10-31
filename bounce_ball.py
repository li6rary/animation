import matplotlib.pyplot as plt
import matplotlib.animation as animation

g = -9.81  # m/s^2
dt = 0.01
factor = 0.8  # 碰撞系数
radius = 0.5
vx1, x1, vy1, y1 = 3, 5, 0, 9


def update(index):
    global vx1, x1, vy1, y1
    x1 += vx1 * dt
    vx1 += 0
    y1 += vy1 * dt + 0.5 * g * dt ** 2
    vy1 += g * dt

    if y1 - radius < 0:
        y1 = radius
        vy1 = -vy1 * factor

    if x1 + radius > 10:
        x1 = 10 - radius
        vx1 = -vx1 * factor
    elif x1 - radius < 0:
        x1 = radius
        vx1 = -vx1 * factor

    # ball.center = (5, height)
    ball.set_center((x1, y1))
    return ball,


# Set up the figure and axis
fig, ax = plt.subplots()
# ax.axis('scaled')
ax.set_aspect('equal')
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Set up the ball
ball = plt.Circle((x1, y1), radius, fc='red')
ax.add_patch(ball)
ball2 = plt.Circle((5, 5), radius, fc='green')
ax.add_patch(ball2)

# Create the animation object
anim = animation.FuncAnimation(fig, update, frames=2000, blit=True, interval=5)

# FFwriter = animation.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])
# anim.save('bounce_ball.mp4', writer=FFwriter)

# Show the animation
plt.show()
