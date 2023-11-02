import matplotlib.pyplot as plt
import matplotlib.animation as animation


g = -9.81  # m/s^2
dt = 0.01  # 取的小时间微元
factor = 1.05  # 碰撞系数
radius = 0.5   # 半径
# xmin=0
# ymin=0 编写过程中默认取0
ymax = 10 #设置垂直高度
xmax = 10 #设置水平距离
vx1, x1, vy1, y1 = 3, 5, 0, 8
vx2, x2, vy2, y2 = -5, 8, 0, 5
k = 1  # 两小球质量比，球2比球1


def update(index):
    global vx1, x1, vy1, y1, vx2, x2, vy2, y2
    #球1数据更新
    x1 += vx1 * dt
    vx1 += 0
    y1 += vy1 * dt + 0.5 * g * dt ** 2
    vy1 += g * dt
    #球2数据更新
    x2 += vx2 * dt
    vx2 += 0
    y2 += vy2 * dt + 0.5 * g * dt ** 2
    vy2 += g * dt
    #判断球1撞地
    if y1 - radius < 0:
        y1 = radius
        vy1 = -vy1 * factor
    #判断球2撞天花板
    elif y1 + radius > ymax:
        y1 = ymax-radius
        vy1 = -vy1 * factor
    #判断球1撞右墙
    if x1 + radius > xmax:
        x1 = xmax - radius
        vx1 = -vx1 * factor
    #判断球1撞左墙
    elif x1 - radius < 0:
        x1 = radius
        vx1 = -vx1 * factor
    #判断球2撞地
    if y2 - radius < 0:
        y2 = radius
        vy2 = -vy2 * factor
    #判断球2撞天花板
    elif y2 + radius > ymax:
        y2 = ymax -radius
        vy2 = -vy2 * factor
    #判断球2撞右墙
    if x2 + radius > xmax:
        x2 = xmax - radius
        vx2 = -vx2 * factor
    #判断球2撞左墙
    elif x2 - radius < 0:
        x2 = radius
        vx2 = -vx2 * factor
    #判断相撞
    if (x1 - x2) ** 2 + (y1 - y2) ** 2 < 4 * radius ** 2:
        a = (y1 - y2) / (x1 - x2)
        x1 = (x1 + x2) / 2 + radius * (x1 - x2) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        x2 = (x1 + x2) / 2 + radius * (x2 - x1) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        y1 = (y1 + y2) / 2 + radius * (y1 - y2) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        y2 = (y1 + y2) / 2 + radius * (y2 - y1) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        vx1f = ((1 + a ** 2 - k + a * a * k) * vx1 - 2 * k * a * vy1 + 2 * k * vx2 + 2 * a * k * vy2) / (
                a * a * k + k + 1 + a * a)
        vy1f = vy1 + a * (-2 * k * vx1 - 2 * k * a * vy1 + 2 * k * vx2 + 2 * a * k * vy2) / (a * a * k + k + 1 + a * a)
        vx2f = -(-2 * k * vx1 - 2 * k * a * vy1 + 2 * k * vx2 + 2 * a * k * vy2) / (a * a * k + k + 1 + a * a) / k + vx2
        vy2f = -a * (-2 * k * vx1 - 2 * k * a * vy1 + 2 * k * vx2 + 2 * a * k * vy2) / (
                a * a * k + k + 1 + a * a) / k + vy2
        vx1 = vx1f
        vx2 = vx2f
        vy1 = vy1f
        vy2 = vy2f

    # ball.center = (5, height)
    ball.set_center((x1, y1))
    ball2.set_center((x2, y2))
    return ball, ball2


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

# Create the animation object
anim = animation.FuncAnimation(fig, update, frames=200, blit=True, interval=5)

# FFwriter = animation.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])
# anim.save('bounce_ball.gif', writer=FFwriter)

# Show the animation
plt.show()

