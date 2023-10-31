import matplotlib.pyplot as plt
import matplotlib.animation as animation


g = -9.81  # m/s^2
dt = 0.01
factor = 0.95  # 碰撞系数
radius = 0.5
vx1, x1, vy1, y1 = 3, 5, 0, 9
vx2, x2, vy2, y2 = -5, 8, 0, 9
k = 1  # 两小球质量比，球2比球1


def update(index):
    global vx1, x1, vy1, y1, vx2, x2, vy2, y2
    x1 += vx1 * dt
    vx1 += 0
    y1 += vy1 * dt + 0.5 * g * dt ** 2
    vy1 += g * dt

    x2 += vx2 * dt
    vx2 += 0
    y2 += vy2 * dt + 0.5 * g * dt ** 2
    vy2 += g * dt

    if y1 - radius < 0:
        y1 = radius
        vy1 = -vy1 * factor

    if x1 + radius > 10:
        x1 = 10 - radius
        vx1 = -vx1 * factor
    elif x1 - radius < 0:
        x1 = radius
        vx1 = -vx1 * factor

    if y2 - radius < 0:
        y2 = radius
        vy2 = -vy2 * factor

    if x2 + radius > 10:
        x2 = 10 - radius
        vx2 = -vx2 * factor
    elif x2 - radius < 0:
        x2 = radius
        vx2 = -vx2 * factor

    if (x1 - x2) ** 2 + (y1 - y2) ** 2 < 4 * radius ** 2:
        a = (y1 - y2) / (x1 - x2)
        x1 = (x1 + x2) / 2 + radius * (x1 - x2) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        x2 = (x1 + x2) / 2 + radius * (x2 - x1) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        y1 = (y1 + y2) / 2 + radius * (y1 - y2) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        y2 = (y1 + y2) / 2 + radius * (y2 - y1) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        vx10 = ((1 + a ** 2 - k + a * a * k) * vx1 - 2 * k * a * vy1 + 2 * k * vx2 + 2 * a * k * vy2) / (
                a * a * k + k + 1 + a * a)
        vy10 = vy1 + a * (-2 * k * vx1 - 2 * k * a * vy1 + 2 * k * vx2 + 2 * a * k * vy2) / (a * a * k + k + 1 + a * a)
        vx20 = -(-2 * k * vx1 - 2 * k * a * vy1 + 2 * k * vx2 + 2 * a * k * vy2) / (a * a * k + k + 1 + a * a) / k + vx2
        vy20 = -a * (-2 * k * vx1 - 2 * k * a * vy1 + 2 * k * vx2 + 2 * a * k * vy2) / (
                a * a * k + k + 1 + a * a) / k + vy2
        vx1 = vx10
        vx2 = vx20
        vy1 = vy10
        vy2 = vy20

    # ball.center = (5, height)
    ball.set_center((x1, y1))
    ball2.set_center((x2, y2))
    return ball, ball2


# Set up the figure and axis
fig, ax = plt.subplots()
# ax.axis('scaled')
ax.set_aspect('equal')
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Set up the ball
ball = plt.Circle((x1, y1), radius, fc='red')
ax.add_patch(ball)
ball2 = plt.Circle((x2, y2), radius, fc='green')
ax.add_patch(ball2)

# Create the animation object
anim = animation.FuncAnimation(fig, update, frames=200, blit=True, interval=5)

# FFwriter = animation.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])
# anim.save('bounce_ball.gif', writer=FFwriter)

# Show the animation

plt.show()

