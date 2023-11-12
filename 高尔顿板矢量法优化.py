import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D
import numpy as np
from numpy.linalg import norm
import random
from numba import jit


class Ball:
    def __init__(self, r, v):
        self.r = np.array(r)
        self.v = np.array(v)


class Nail:
    def __init__(self, r):
        self.r = np.array(r)


# # 获取特定向量的垂直向量
# def getvertical_vector(vec):
#     return np.array([vec[1], -vec[0]])


# 自由落体
@jit(nopython=True)
def freefall(r, v):
    r += v * 0.002
    v += np.array([0, -981]) * 0.002  # cm/s^2
    return r, v


# 定义碰撞边界、漏斗、隔板
def bouncewall(ball):
    for i in range(ballnum):
        # 碰撞天花板
        if ball[i].r[1] > ymax - radius:
            factor = 0.98  # 与天花板的碰撞系数
            ball[i].r[1] = ymax - radius
            ball[i].v[1] = -ball[i].v[1] * factor
        elif ymin + radius < ball[i].r[1] < -sy + sx + radius:
            factor = 0.98  # 与左右边界的碰撞系数
            # 碰撞左右边界
            if ball[i].r[0] - radius < xmin:
                ball[i].r[0] = xmin + radius
                ball[i].v[0] = -ball[i].v[0] * factor
            elif ball[i].r[0] + radius > xmax:
                ball[i].r[0] = xmax - radius
                ball[i].v[0] = -ball[i].v[0] * factor
        # 碰撞底板，完全非弹性碰撞，竖直速度变为0
        elif ball[i].r[1] < ymin + radius:
            ball[i].r[1] = ymin + radius
            ball[i].v[1] = 0
        # 小球与下方隔板的碰撞
        if ball[i].r[1] < py + radius:
            parfactor = 0.5  # 与下方隔板的碰撞系数
            for j in range(cn):
                if dx * j - dx * (cn + 1) / 2 < ball[i].r[0] < dx * j - dx * (cn - 1) / 2 < ball[i].r[0] + radius:
                    ball[i].r[0] = dx * j - dx * (cn - 1) / 2 - radius
                    ball[i].v[0] = -ball[i].v[0] * parfactor
                elif dx * j - dx * (cn - 1) / 2 > ball[i].r[0] > dx * j - dx * (cn + 1) / 2 > ball[i].r[0] - radius:
                    ball[i].r[0] = dx * j - dx * (cn + 1) / 2 + radius
                    ball[i].v[0] = -ball[i].v[0] * parfactor
        # 碰撞上漏斗
        elif ball[i].r[1] > 0:
            funnelfactor = 0.8  # 与上漏斗碰撞的碰撞系数
            # 判断碰到左侧上壁
            if ball[i].r[0] + ball[i].r[1] < -sx + 1.414 * radius and ball[i].r[0] < -sx + radius / 1.414:
                en = np.array([1 / 1.414, 1 / 1.414])
                ef = np.array([1 / 1.414, -1 / 1.414])
                ball[i].r = np.array([1.414 * radius - sx - ball[i].r[1], 1.414 * radius - sx - ball[i].r[0]])
                ball[i].v = np.dot(ball[i].v, ef) * ef - funnelfactor * np.dot(ball[i].v, en) * en
            # 判断碰到右侧上壁
            elif ball[i].r[1] - ball[i].r[0] < -sx + 1.414 * radius and ball[i].r[0] > sx - radius / 1.414:
                en = np.array([-1 / 1.414, 1 / 1.414])
                ef = np.array([1 / 1.414, 1 / 1.414])
                ball[i].r = np.array([-1.414 * radius + sx + ball[i].r[1], 1.414 * radius - sx + ball[i].r[0]])
                ball[i].v = np.dot(ball[i].v, ef) * ef - funnelfactor * np.dot(ball[i].v, en) * en
        # 碰撞下漏斗
        else:
            funnelfactor = 0.95  # 与下漏斗碰撞的碰撞系数
            # 判断碰到左侧下壁
            if ball[i].r[1] - ball[i].r[0] > sx - 1.414 * radius and ball[i].r[0] < -sx + radius / 1.414:
                en = np.array([1 / 1.414, -1 / 1.414])
                ef = np.array([-1 / 1.414, -1 / 1.414])
                ball[i].r = np.array([1.414 * radius - sx + ball[i].r[1], -1.414 * radius + sx + ball[i].r[0]])
                ball[i].v = np.dot(ball[i].v, ef) * ef - funnelfactor * np.dot(ball[i].v, en) * en

            # 判断碰到右侧下壁
            elif ball[i].r[0] + ball[i].r[1] > sx - 1.414 * radius and ball[i].r[0] > sx - radius / 1.414:
                en = np.array([-1 / 1.414, -1 / 1.414])
                ef = np.array([-1 / 1.414, 1 / 1.414])
                ball[i].r = np.array([-1.414 * radius + sx - ball[i].r[1], -1.414 * radius + sx - ball[i].r[0]])
                ball[i].v = np.dot(ball[i].v, ef) * ef - funnelfactor * np.dot(ball[i].v, en) * en
    return ball


# 定义碰撞钉子
def bouncenail(ball):
    railfactor = 0.8  # 与钉子碰撞的碰撞系数
    for i in range(ballnum):
        if ball[i].r[1] < 0:
            for k in range(int(cn * (cn + 1) / 2)):
                d = norm(ball[i].r - nail[k].r)
                # 判断小球是否触及钉子
                if d < radius + rnail:
                    en = (ball[i].r - nail[k].r) / d
                    ef = np.array([en[1], -en[0]])
                    ball[i].v = np.dot(ball[i].v, ef) * ef - railfactor * np.dot(ball[i].v, en) * en
                    ball[i].r = nail[k].r + en * (radius + rnail)
    return ball


# 定义互相碰撞
def bounceeachother(ball):
    k1 = 1  # 两小球碰撞因子
    for i in range(ballnum):
        for j in range(i + 1, ballnum):
            if ball[i].r[0] - ball[j].r[0] < 2 * radius and ball[i].r[1] - ball[j].r[1] < 2 * radius:
                d = norm(ball[i].r - ball[j].r)
                # 判断小球是否碰撞
                if d < 2 * radius:
                    en = (ball[i].r - ball[j].r) / d
                    ef = np.array([en[1], -en[0]])
                    ball[i].v, ball[j].v = np.dot(ball[i].v, ef) * ef + k1 * np.dot(ball[j].v, en) * en, \
                                           np.dot(ball[j].v, ef) * ef + k1 * np.dot(ball[i].v, en) * en
                    r0 = (ball[i].r + ball[j].r) / 2
                    ball[i].r = r0 + radius * en
                    ball[j].r = r0 - radius * en
    return ball


def update(index):
    global ball
    for i in range(ballnum):
        ball[i].r, ball[i].v = freefall(ball[i].r, ball[i].v)
    ball = bouncewall(ball)
    ball = bouncenail(ball)
    ball = bounceeachother(ball)
    for i in range(ballnum):
        balls[i].set_center(ball[i].r)
    return balls


radius = 0.7  # 小球半径
ballnum = 200  # 小球数量
# 设置xy轴范围
xmin = -32
ymin = -44
ymax = 32
xmax = 32
# 定义高尔顿板钉子的参数
rnail = 0.3  # 钉子半径
ny0 = -1  # 第一个钉子的y坐标
dx = 3.5  # 横向间距
dy = 1.8  # 纵向间距
cn = 18  # 层数
sx, sy = 1.5, 34  # 定义侧板位置
py = -35  # 定义隔板位置

ball = []
nail = []

for i in range(ballnum):
    xi = random.uniform(xmin + radius + 1, xmax - radius - 1)
    yi = random.uniform(10, ymax - radius - 1)
    vxi = random.uniform(0, 0)
    vyi = random.uniform(0, 0)
    r = [xi, yi]
    v = [vxi, vyi]
    ball.append(Ball(r, v))

# 循环定义各钉子的位置
for i in range(cn):
    for j in range(i + 1):
        r = [dx * j - dx * i / 2, -dy * i + ny0]
        nail.append(Nail(r))

balls = []
nails = []

# 建立图形，设置横纵轴范围，要求横纵轴等长
fig, ax = plt.subplots()
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
    balls.append(plt.Circle((ball[i].r), radius, fc=colorlist[i % 12], color='black', linewidth=0.5))
    ax.add_patch(balls[i])
# 绘制钉子
for i in range(int(cn * (cn + 1) / 2)):
    nails.append(plt.Circle((nail[i].r), rnail, fc='black'))
    ax.add_patch(nails[i])

anim = animation.FuncAnimation(fig, update, blit=True, interval=2)
plt.show()







