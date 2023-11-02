import matplotlib.pyplot as plt
import matplotlib.animation as animation

g = -9.81  # m/s^2
dt = 0.01  # 取的小时间微元
factor = 0.98  # 碰撞系数
radius = 0.5  # 半径
# xmin=0
# ymin=0 编写过程中默认取0
ymax = 10  # 设置垂直高度
xmax = 10  # 设置水平距离
# 定义各个小球的初速度与初始位置
vx1, x1, vy1, y1 = 3, 2, 0, 4
vx2, x2, vy2, y2 = -5, 4, 0, 4
vx3, x3, vy3, y3 = 5, 6, 0, 4
vx4, x4, vy4, y4 = -2, 8, 0, 4
vx5, x5, vy5, y5 = -3, 2, 0, 8
vx6, x6, vy6, y6 = -4, 4, 0, 8
vx7, x7, vy7, y7 = 7, 6, 0, 8
vx8, x8, vy8, y8 = 3, 8, 0, 8
p = [[vx1, x1, vy1, y1], [vx2, x2, vy2, y2], [vx3, x3, vy3, y3], [vx4, x4, vy4, y4], [vx5, x5, vy5, y5],
     [vx6, x6, vy6, y6], [vx7, x7, vy7, y7], [vx8, x8, vy8, y8]]


# 定义自由落体函数
def freefall(vx, x, vy, y):
    x += vx * dt
    y += vy * dt
    vy += g * dt
    return [vx, x, vy, y]


# 定义碰撞边界时的运动
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

    return [vx, x, vy, y]


# 两小球发生碰撞时的运动
def bounceeachother(vbx1, xb1, vby1, yb1, vbx2, xb2, vby2, yb2):
    a = (yb1 - yb2) / (xb1 - xb2)
    xb1 = (xb1 + xb2) / 2 + radius * (xb1 - xb2) / ((xb1 - xb2) ** 2 + (yb1 - yb2) ** 2) ** 0.5
    xb2 = (xb1 + xb2) / 2 + radius * (xb2 - xb1) / ((xb1 - xb2) ** 2 + (yb1 - yb2) ** 2) ** 0.5
    yb1 = (yb1 + yb2) / 2 + radius * (yb1 - yb2) / ((xb1 - xb2) ** 2 + (yb1 - yb2) ** 2) ** 0.5
    yb2 = (yb1 + yb2) / 2 + radius * (yb2 - yb1) / ((xb1 - xb2) ** 2 + (yb1 - yb2) ** 2) ** 0.5
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
    return [vbx1, xb1, vby1, yb1], [vbx2, xb2, vby2, yb2]


def update(index):
    global p
    # 自由落体
    for i in range(len(p)):
        p[i] = freefall(p[i][0], p[i][1], p[i][2], p[i][3])

    # 判断是否触及边界
    for i in range(len(p)):
        if p[i][3] - radius < 0 or p[i][3] + radius > ymax or p[i][1] + radius > xmax or p[i][1] - radius < 0:
            p[i] = bouncewall(p[i][0], p[i][1], p[i][2], p[i][3])

    # 判断两小球相撞
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if (p[i][1] - p[j][1]) ** 2 + (p[i][3] - p[j][3]) ** 2 < 4 * radius ** 2:
                # p[i][1], p[j][1], p[i][3], p[j][3] = p[i][1], p[j][1], p[i][3], p[j][3]
                p[i], p[j] = bounceeachother(p[i][0], p[i][1], p[i][2], p[i][3], p[j][0], p[j][1], p[j][2], p[j][3])

    # 循环定义各球的位置
    for i in range(len(p)):
        exec('ball%s.set_center((p[i][1], p[i][3]))' % str(i+1))
    # ball1.set_center((p[0][1], p[0][3]))
    # ball2.set_center((p[1][1], p[1][3]))
    # ball3.set_center((p[2][1], p[2][3]))
    # ball4.set_center((p[3][1], p[3][3]))
    # ball5.set_center((p[4][1], p[4][3]))
    # ball6.set_center((p[5][1], p[5][3]))
    # ball7.set_center((p[6][1], p[6][3]))
    # ball8.set_center((p[7][1], p[7][3]))

    return ball1, ball2, ball3, ball4, ball5, ball6, ball7, ball8


# 建立图形，设置横纵轴范围，要求横纵轴等长
fig, ax = plt.subplots()
# ax.axis('scaled')
ax.set_aspect('equal')
ax.set_xlim(0, xmax)
ax.set_ylim(0, ymax)

# 设置球
ball1 = plt.Circle((x1, y1), radius, fc='red')
ax.add_patch(ball1)
ball2 = plt.Circle((x2, y2), radius, fc='green')
ax.add_patch(ball2)
ball3 = plt.Circle((x3, y3), radius, fc='blue')
ax.add_patch(ball3)
ball4 = plt.Circle((x4, y4), radius, fc='orange')
ax.add_patch(ball4)
ball5 = plt.Circle((x5, y5), radius, fc='pink')
ax.add_patch(ball5)
ball6 = plt.Circle((x6, y6), radius, fc='yellow')
ax.add_patch(ball6)
ball7 = plt.Circle((x7, y7), radius, fc='brown')
ax.add_patch(ball7)
ball8 = plt.Circle((x8, y8), radius, fc='black')
ax.add_patch(ball8)

anim = animation.FuncAnimation(fig, update, frames=200, blit=True, interval=5)
plt.show()
