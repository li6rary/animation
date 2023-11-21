# 高尔顿板模拟程序，可以自由改变小球的数量、半径、钉子层数、间距以及各碰撞系数等。
import random
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation
import matplotlib.patches as patch
from numba import jit


# 定义自由落体函数
@jit(nopython=True)
def freefall(vx, x, vy, y):
    x += vx * dt
    y += vy * dt
    vy += g * dt
    return [vx, x, vy, y]


# 定义碰撞边界、漏斗、隔板
@jit(nopython=True, nogil=True)  # 多线程并发
def bouncewall(vx, x, vy, y):
    # 碰撞天花板
    if y > ymax - radius:
        factor = 0.98  # 与天花板的碰撞系数
        y = ymax - radius
        vy = -vy * factor
    elif ymin + radius < y < -sy + sx + radius:
        factor = 0.98  # 与左右边界的碰撞系数
        # 碰撞左右边界
        if x - radius < xmin:
            x = xmin + radius
            vx = -vx * factor
        elif x + radius > xmax:
            x = xmax - radius
            vx = -vx * factor
    # 碰撞底板，完全非弹性碰撞，竖直速度变为0
    elif y < ymin + radius:
        y = ymin + radius
        vy = 0
    # 小球与下方隔板的碰撞
    if y < py + radius:
        parfactor = 0.5  # 与下方隔板的碰撞系数
        for j in range(cn):
            if dx * j - dx * (cn + 1) / 2 < x < dx * j - dx * (cn - 1) / 2 < x + radius:
                x = dx * j - dx * (cn - 1) / 2 - radius
                vx = -vx * parfactor
            elif dx * j - dx * (cn - 1) / 2 > x > dx * j - dx * (cn + 1) / 2 > x - radius:
                x = dx * j - dx * (cn + 1) / 2 + radius
                vx = -vx * parfactor
    # 碰撞上漏斗
    elif y > 0:
        funnelfactor = 0.8  # 与上漏斗碰撞的碰撞系数
        # 判断碰到左侧上壁
        if x + y < -sx + 1.414 * radius and x < -sx + radius / 1.414:
            x, y = 1.414 * radius - sx - y, 1.414 * radius - sx - x
            vx, vy = vx / 2 - vy / 2 - funnelfactor * (vx / 2 + vy / 2), -vx / 2 + vy / 2 - funnelfactor * (
                    vx / 2 + vy / 2)
        # 判断碰到右侧上壁
        elif y - x < -sx + 1.414 * radius and x > sx - radius / 1.414:
            x, y = -1.414 * radius + sx + y, 1.414 * radius - sx + x
            vx, vy = vx / 2 + vy / 2 - funnelfactor * (vx / 2 - vy / 2), vx / 2 + vy / 2 - funnelfactor * (
                    -vx / 2 + vy / 2)
    # 碰撞下漏斗
    else:
        funnelfactor = 0.95  # 与下漏斗碰撞的碰撞系数
        # 判断碰到左侧下壁
        if y - x > sx - 1.414 * radius and x < -sx + radius / 1.414:
            x, y = 1.414 * radius - sx + y, -1.414 * radius + sx + x
            vx, vy = vx / 2 + vy / 2 - funnelfactor * (vx / 2 - vy / 2), vx / 2 + vy / 2 - funnelfactor * (
                    -vx / 2 + vy / 2)
        # 判断碰到右侧下壁
        elif x + y > sx - 1.414 * radius and x > sx - radius / 1.414:
            x, y = -1.414 * radius + sx - y, -1.414 * radius + sx - x
            vx, vy = vx / 2 - vy / 2 - funnelfactor * (vx / 2 + vy / 2), -vx / 2 + vy / 2 - funnelfactor * (
                    vx / 2 + vy / 2)
    return vx, x, vy, y


@jit(nopython=True, nogil=True)
def bouncenail(vbx1, xb1, vby1, yb1, xb2, yb2):
    railfactor = 0.8
    a = (yb1 - yb2) / (xb1 - xb2 + 0.0000001)
    xb1 = (xb1 + xb2) / 2 + radius * (xb1 - xb2) / ((xb1 - xb2 + 0.0000001) ** 2 + (yb1 - yb2) ** 2) ** 0.5
    yb1 = (yb1 + yb2) / 2 + radius * (yb1 - yb2) / ((xb1 - xb2 + 0.0000001) ** 2 + (yb1 - yb2) ** 2) ** 0.5
    vbxf = railfactor * ((a ** 2 + a * a) * vbx1 - 2 * a * vby1) / (a * a + 2 + a * a)
    vbyf = railfactor * vby1 + a * (-2 * vbx1 - 2 * a * vby1) / (a * a + 2 + a * a)
    vbx1 = vbxf
    vby1 = vbyf
    return [vbx1, xb1, vby1, yb1]


# 两小球发生碰撞时的运动
@jit(nopython=True, nogil=True)
def bounceeachother(vbx1, xb1, vby1, yb1, vbx2, xb2, vby2, yb2):
    a = (yb1 - yb2) / (xb1 - xb2 + 0.0000001)
    xb1 = (xb1 + xb2) / 2 + radius * (xb1 - xb2) / ((xb1 - xb2 + 0.0000001) ** 2 + (yb1 - yb2) ** 2) ** 0.5
    xb2 = (xb1 + xb2) / 2 + radius * (xb2 - xb1) / ((xb1 - xb2 + 0.0000001) ** 2 + (yb1 - yb2) ** 2) ** 0.5
    yb1 = (yb1 + yb2) / 2 + radius * (yb1 - yb2) / ((xb1 - xb2 + 0.0000001) ** 2 + (yb1 - yb2) ** 2) ** 0.5
    yb2 = (yb1 + yb2) / 2 + radius * (yb2 - yb1) / ((xb1 - xb2 + 0.0000001) ** 2 + (yb1 - yb2) ** 2) ** 0.5
    vx1f = ((a ** 2 + a * a) * vbx1 - 2 * a * vby1 + 2 * vbx2 + 2 * a * vby2) / (a * a + 2 + a * a)
    vy1f = vby1 + a * (-2 * vbx1 - 2 * a * vby1 + 2 * vbx2 + 2 * a * vby2) / (a * a + 2 + a * a)
    vx2f = -(-2 * vbx1 - 2 * a * vby1 + 2 * vbx2 + 2 * a * vby2) / (a * a + 2 + a * a) + vbx2
    vy2f = -a * (-2 * vbx1 - 2 * a * vby1 + 2 * vbx2 + 2 * a * vby2) / (a * a + 2 + a * a) + vby2
    vbx1 = vx1f
    vbx2 = vx2f
    vby1 = vy1f
    vby2 = vy2f
    return [vbx1, xb1, vby1, yb1], [vbx2, xb2, vby2, yb2]


def update(index):
    global p, nnum
    for i in range(ballnum):
        p[i] = freefall(p[i][0], p[i][1], p[i][2], p[i][3])
        p[i] = bouncewall(p[i][0], p[i][1], p[i][2], p[i][3])

        if p[i][3] < 0:
            for j in range(nailnum):
                if (p[i][1] - nail[j][0]) ** 2 + (p[i][3] - nail[j][1]) ** 2 < (rnail + radius) ** 2:
                    p[i] = bouncenail(p[i][0], p[i][1], p[i][2], p[i][3], nail[j][0], nail[j][1])

        for k in range(i + 1, ballnum):
            if p[i][1] - p[k][1] < 2 * radius and p[i][3] - p[k][3] < 2 * radius:
                if (p[i][1] - p[k][1]) ** 2 + (p[i][3] - p[k][3]) ** 2 < 4 * radius ** 2:
                    p[i], p[k] = bounceeachother(p[i][0], p[i][1], p[i][2], p[i][3], p[k][0], p[k][1], p[k][2], p[k][3])

    # 计数器，记录各隔板之间小球个数
    for j in range(cn + 1):
        nn = 0
        for i in range(ballnum):
            if p[i][3] < py + radius:
                if dx * j - dx * (cn + 1) / 2 < p[i][1] < dx * j - dx * (cn - 1) / 2:
                    nn += 1
                else:
                    nn += 0
        eval('patch%d.set_height(nn)' % (j + 1))  # 设置第j个柱形的高
        eval('text%d.set_text(str(nn))' % (j + 1))  # 显示个数
        eval('text%d.set_position((j-0.4, nn))' % (j + 1))  # 显示在柱形上，位置随数量变化

    # 循环定义各球的位置
    for i in range(ballnum):
        eval('ball%d.set_center((p[i][1], p[i][3]))' % (i + 1))
    return eval(balllist)


# 定义各个参数
radius = 0.7  # 小球半径
ballnum = 200  # 小球数量
g = -981  # cm/s^2
dt = 0.002  # 取的小时间微元
# 设置xy轴范围
xmin = -32
ymin = -44
ymax = 32
xmax = 32
# 定义高尔顿板钉子的参数
rnail = 0.3  # 钉子的半径
ny0 = -1  # 第一个钉子的y坐标
dx = 3.5  # 横向间距
dy = 1.8  # 纵向间距
cn = 18  # 层数
sx, sy = 1.5, 34  # 定义侧板位置
py = -35  # 定义隔板位置
p = []  # 用于存放各小球的速度与位置
# 在漏斗上方随机生成小球的位置
for i in range(ballnum):
    exec('vx%d,x%d,vy%d,y%d=0,random.uniform(xmin+radius+1,xmax-radius-1),0,random.uniform(10,ymax-radius-1)' % (
        i + 1, i + 1, i + 1, i + 1))
    eval('p.append([vx%d, x%d, vy%d, y%d])' % (i + 1, i + 1, i + 1, i + 1))
# 生成update函数返回内容字符串
balllist = ""
for i in range(ballnum):
    exec("balllist = balllist + 'ball' + str(i+1) +', '")
for j in range(cn+1):
    exec("balllist = balllist + 'patch' + str(j+1) +', '")
    exec("balllist = balllist + 'text' + str(j+1) +', '")
nail = []  # 存放各个钉子的坐标
for i in range(cn):
    for j in range(i + 1):
        nail.append([dx * j - dx * i / 2, -dy * i + ny0])
nailnum = len(nail)  # 钉子总数
# 建立图形，设置横纵轴范围，要求横纵轴等长
fig, (ax, ax2) = plt.subplots(1, 2)
ax.set_aspect('equal')
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_title("高尔顿板", fontproperties='SimSun')
# 绘制漏斗
line1 = Line2D([sx, sy], [0, sy - sx], linewidth=2, color='black')
ax.add_line(line1)
line2 = Line2D([-sx, -sy], [0, sy - sx], linewidth=2, color='black')
ax.add_line(line2)
line3 = Line2D([sx, sy], [0, -(sy - sx)], linewidth=2, color='black')
ax.add_line(line3)
line4 = Line2D([-sx, -sy], [0, -(sy - sx)], linewidth=2, color='black')
ax.add_line(line4)
# 绘制下方隔板
for i in range(cn):
    exec("gline%d = Line2D([dx*i-dx*(cn-1)/2, dx*i-dx*(cn-1)/2], [ymin, py], color='black')" % (i + 1))
    eval('ax.add_line(gline%d)' % (i + 1))
# 绘制各小球
colorlist = ['red', 'green', 'blue', 'orange', 'pink', 'yellow', 'brown', 'black', 'cyan', 'magenta', 'gray',
             'purple']
for i in range(ballnum):
    exec("ball{} = plt.Circle((x{}, y{}), radius, fc=colorlist[i%12], color='black', linewidth=0.5)"
         .format(str(i + 1), str(i + 1), str(i + 1)))
    eval('ax.add_patch(ball%d)' % (i + 1))
# 绘制钉子
for i in range(cn):
    for j in range(i + 1):
        exec("nail%d%d = plt.Circle((dx * j - dx * i / 2, -dy * i + ny0), rnail, fc='black')" % (i, j))
        eval('ax.add_patch(nail%s%s)' % (str(i), str(j)))
# 绘制子图
ax2.set_xlim(-1, cn+1)
ax2.set_ylim(0, 30)
ax2.set_title("计数", fontproperties='SimSun')
plt.ylabel("小球个数", fontproperties='SimSun')
plt.xticks([j for j in range(cn+1)])
for j in range(cn + 1):
    exec("patch{} = patch.Rectangle([j-0.45, 0], width=0.9, height=0, fc='cyan')".format(str(j + 1)))
    eval('ax2.add_patch(patch%d)' % (j + 1))
    exec("text{} = plt.text(j-0.4, 0, '0')".format(str(j + 1)))
anim = animation.FuncAnimation(fig, update, blit=True, interval=2)
plt.show()
