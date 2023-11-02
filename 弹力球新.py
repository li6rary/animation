import matplotlib.pyplot as plt
import matplotlib.animation as animation

g = -9.81  # m/s^2
dt = 0.01  # 取的小时间微元
factor = 1  # 碰撞系数
radius = 0.5  # 半径
# xmin=0
# ymin=0 编写过程中默认取0
ymax = 10  # 设置垂直高度
xmax = 10  # 设置水平距离
vx1, x1, vy1, y1 = 3, 2, 0, 8
vx2, x2, vy2, y2 = -5, 5, 0, 5
vx3, x3, vy3, y3 = 5, 8, 0, 2
vx4, x4, vy4, y4 = -2, 8, 0, 4


def freefall(vx, x, vy, y):
    x += vx * dt
    vx += 0
    y += vy * dt + 0.5 * g * dt ** 2
    vy += g * dt
    return vx, x, vy, y


def bouncewall(vx, x, vy, y):
    # 判断球1撞地
    if y - radius < 0:
        y = radius
        vy = -vy * factor
    # 判断球2撞天花板
    elif y + radius > ymax:
        y = ymax - radius
        vy = -vy * factor
    # 判断球1撞右墙
    if x + radius > xmax:
        x = xmax - radius
        vx = -vx * factor
    # 判断球1撞左墙
    elif x - radius < 0:
        x = radius
        vx = -vx * factor

    return vx, x, vy, y


def bounceeachother(vbx1, xb1, vby1, yb1, vbx2, xb2, vby2, yb2):
    a = (yb1 - yb2) / (xb1 - xb2)
    vx1f = ((a ** 2 + a * a) * vbx1 - 2 * a * vby1 + 2 * vbx2 + 2 * a * vby2) / (
            a * a + 2 + a * a)
    vy1f = vby1 + a * (-2 * vbx1 - 2 * a * vby1 + 2 * vbx2 + 2 * a * vby2) / (a * a + 2 + a * a)
    vx2f = -(-2 * vbx1 - 2 * a * vby1 + 2 * vbx2 + 2 * a * vby2) / (a * a + 2 + a * a) + vbx2
    vy2f = -a * (-2 * vbx1 - 2 * a * vby1 + 2 * vbx2 + 2 * a * vby2) / (
            a * a + 2 + a * a) + vby2
    vbx1 = vx1f
    vbx2 = vx2f
    vby1 = vy1f
    vby2 = vy2f
    return vbx1, vby1, vbx2, vby2


def update(index):
    global vx1, x1, vy1, y1, vx2, x2, vy2, y2, vx3, x3, vy3, y3, vx4, x4, vy4, y4
    # 自由落体
    vx1, x1, vy1, y1 = freefall(vx1, x1, vy1, y1)
    vx2, x2, vy2, y2 = freefall(vx2, x2, vy2, y2)
    vx3, x3, vy3, y3 = freefall(vx3, x3, vy3, y3)
    vx4, x4, vy4, y4 = freefall(vx4, x4, vy4, y4)
    # 判断球1撞地
    if y1 - radius < 0 or y1 + radius > ymax or x1 + radius > xmax or x1 - radius < 0:
        vx1, x1, vy1, y1 = bouncewall(vx1, x1, vy1, y1)

    if y2 - radius < 0 or y2 + radius > ymax or x2 + radius > xmax or x2 - radius < 0:
        vx2, x2, vy2, y2 = bouncewall(vx2, x2, vy2, y2)

    if y3 - radius < 0 or y3 + radius > ymax or x3 + radius > xmax or x3 - radius < 0:
        vx3, x3, vy3, y3 = bouncewall(vx3, x3, vy3, y3)

    if y4 - radius < 0 or y4 + radius > ymax or x4 + radius > xmax or x4 - radius < 0:
        vx4, x4, vy4, y4 = bouncewall(vx4, x4, vy4, y4)

    # 判断相撞
    if (x1 - x2) ** 2 + (y1 - y2) ** 2 < 4 * radius ** 2:
        x1, y1, x2, y2 = x1, y1, x2, y2
        vx1, vy1, vx2, vy2 = bounceeachother(vx1, x1, vy1, y1, vx2, x2, vy2, y2)

    if (x1 - x3) ** 2 + (y1 - y3) ** 2 < 4 * radius ** 2:
        x1, y1, x3, y3 = x1, y1, x3, y3
        vx1, vy1, vx3, vy3 = bounceeachother(vx1, x1, vy1, y1, vx3, x3, vy3, y3)

    if (x2 - x3) ** 2 + (y2 - y3) ** 2 < 4 * radius ** 2:
        x2, y2, x3, y3 = x2, y2, x3, y3
        vx2, vy2, vx3, vy3 = bounceeachother(vx2, x2, vy2, y2, vx3, x3, vy3, y3)

    if (x1 - x4) ** 2 + (y1 - y4) ** 2 < 4 * radius ** 2:
        x1, y1, x4, y4 = x1, y1, x4, y4
        vx1, vy1, vx4, vy4 = bounceeachother(vx1, x1, vy1, y1, vx4, x4, vy4, y4)

    if (x2 - x4) ** 2 + (y2 - y4) ** 2 < 4 * radius ** 2:
        x2, y2, x4, y4 = x2, y2, x4, y4
        vx2, vy2, vx4, vy4 = bounceeachother(vx2, x2, vy2, y2, vx4, x4, vy4, y4)

    if (x3 - x4) ** 2 + (y3 - y4) ** 2 < 4 * radius ** 2:
        x3, y3, x4, y4 = x3, y3, x4, y4
        vx3, vy3, vx4, vy4 = bounceeachother(vx3, x3, vy3, y3, vx4, x4, vy4, y4)

    # ball.center = (5, height)
    ball.set_center((x1, y1))
    ball2.set_center((x2, y2))
    ball3.set_center((x3, y3))
    ball4.set_center((x4, y4))
    return ball, ball2, ball3, ball4


# Set up the figure and axis
fig, ax = plt.subplots()
# ax.axis('scaled')
ax.set_aspect('equal')
ax.set_xlim(0, xmax)
ax.set_ylim(0, ymax)

# Set up the ball
ball = plt.Circle((x1, y1), radius, fc='red')
ax.add_patch(ball)
ball2 = plt.Circle((x2, y2), radius, fc='green')
ax.add_patch(ball2)
ball3 = plt.Circle((x3, y3), radius, fc='blue')
ax.add_patch(ball3)
ball4 = plt.Circle((x4, y4), radius, fc='orange')
ax.add_patch(ball4)

# Create the animation object
anim = animation.FuncAnimation(fig, update, frames=200, blit=True, interval=5)

# FFwriter = animation.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])
# anim.save('bounce_ball.gif', writer=FFwriter)

# Show the animation

plt.show()
