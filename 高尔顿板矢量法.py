import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D
import numpy as np
import random




class Ball:
    radius = 0.6

    def __init__(self, r, v):
        self.r = np.array(r)
        self.v = np.array(v)


class Nail:
    rnail = 0.2

    def __init__(self, r):
        self.r = np.array(r)


# 获取特定向量的垂直向量
def getvertical_vector(vec):
    return np.array([vec[1], -vec[0]])


# 自由落体
def freefall(ball):
    g = -9.81  # m/s^2
    dt = 0.01  # 取的小时间微元
    tb = ball
    for i in range(ballnum):
        tb[i].r = ball[i].r + ball[i].v * dt
        tb[i].v[1] = ball[i].v[1] + g * dt
        tb[i].v[0] = ball[i].v[0]
    return tb


# 碰撞边界
def bouncewall(ball):
    tb = ball
    factor = 0.2  # 与边界的碰撞系数
    for i in range(ballnum):
        if ball[i].r[0] - Ball.radius < xmin:
            tb[i].r[0] = xmin + Ball.radius
            tb[i].v[0] = -ball[i].v[0] * factor
        elif ball[i].r[0] + Ball.radius > xmax:
            tb[i].r[0] = xmax - Ball.radius
            tb[i].v[0] = -ball[i].v[0] * factor
        if ball[i].r[1] - Ball.radius < ymin:
            tb[i].r[1] = ymin + Ball.radius
            tb[i].v[1] = -ball[i].v[1] * factor
        elif ball[i].r[1] + Ball.radius > ymax:
            tb[i].r[1] = ymax - Ball.radius
            tb[i].v[1] = -ball[i].v[1] * factor
    return tb


# 定义碰撞上方漏斗
def bouncefunnel(ball):
    b1 = ball
    radius = Ball.radius
    funnelfactor = 0.8  # 与漏斗碰撞的碰撞系数
    # 判断碰到左侧上壁
    for i in range(ballnum):
        if b1[i].r[0] + b1[i].r[1] < -sx + 1.414 * radius and b1[i].r[0] < -sx + radius / 1.414 and \
                b1[i].r[1] > radius / 1.414:
            en = np.array([1/1.414, 1/1.414])
            ef = getvertical_vector(en)
            xf = 1.414 * radius - sx - b1[i].r[1]
            yf = 1.414 * radius - sx - b1[i].r[0]
            b1[i].r[0] = xf
            b1[i].r[1] = yf
            vf1 = ef * np.dot(b1[i].v, ef)
            vn1 = en * np.dot(b1[i].v, en)
            b1[i].v = vf1 - funnelfactor * vn1

        # 判断碰到右侧上壁
        elif b1[i].r[1] - b1[i].r[0] < -sx + 1.414 * radius and b1[i].r[0] > sx - radius / 1.414 and \
                b1[i].r[1] > radius / 1.414:
            en = np.array([-1 / 1.414, 1 / 1.414])
            ef = getvertical_vector(en)
            xf = -1.414 * radius + sx + b1[i].r[1]
            yf = 1.414 * radius - sx + b1[i].r[0]
            b1[i].r[0] = xf
            b1[i].r[1] = yf
            vf1 = ef * np.dot(b1[i].v, ef)
            vn1 = en * np.dot(b1[i].v, en)
            b1[i].v = vf1 - funnelfactor * vn1
        # 判断碰到左侧下壁
        elif b1[i].r[1] - b1[i].r[0] > sx - 1.414 * radius and b1[i].r[0] < -sx + radius / 1.414 and \
                b1[i].r[1] < -radius / 1.414:
            en = np.array([1 / 1.414, -1 / 1.414])
            ef = getvertical_vector(en)
            xf = 1.414 * radius - sx + b1[i].r[1]
            yf = -1.414 * radius + sx + b1[i].r[0]
            b1[i].r[0] = xf
            b1[i].r[1] = yf
            vf1 = ef * np.dot(b1[i].v, ef)
            vn1 = en * np.dot(b1[i].v, en)
            b1[i].v = vf1 - funnelfactor * vn1

        # 判断碰到右侧下壁
        elif b1[i].r[0] + b1[i].r[1] > sx - 1.414 * radius and b1[i].r[0] > sx - radius / 1.414 and \
                b1[i].r[1] < -radius / 1.414:
            en = np.array([-1 / 1.414, -1 / 1.414])
            ef = getvertical_vector(en)
            xf = -1.414 * radius + sx - b1[i].r[1]
            yf = -1.414 * radius + sx - b1[i].r[0]
            b1[i].r[0] = xf
            b1[i].r[1] = yf
            vf1 = ef * np.dot(b1[i].v, ef)
            vn1 = en * np.dot(b1[i].v, en)
            b1[i].v = vf1 - funnelfactor * vn1
    return b1


# 定义碰撞钉子
def bouncenail(b1, n1):
    railfactor = 0.8  # 与钉子碰撞的碰撞系数
    en = (b1.r - n1.r) / (np.linalg.norm(b1.r - n1.r))
    ef = getvertical_vector(en)
    vf1 = ef * np.dot(b1.v, ef)
    vn1 = -en * np.dot(b1.v, en)
    b1.v = vf1 + railfactor * vn1
    b1.r = n1.r + en * (Ball.radius + Nail.rnail)
    return b1


# 小球与下方隔板的碰撞
def bouncepartip(ball):
    b1 = ball
    radius = Ball.radius
    parfactor = 0.5  # 与下方隔板的碰撞系数
    for i in range(ballnum):
        for j in range(cn):
            if dx * j - dx * (cn + 1) / 2 < b1[i].r[0] < dx * j - dx * (cn - 1) / 2 < b1[i].r[0] + radius and \
                    b1[i].r[1] < -dy * (cn - 1) - 2 + radius:
                b1[i].r[0] = dx * j - dx * (cn - 1) / 2 - radius
                b1[i].v[0] = -b1[i].v[0] * parfactor
            elif dx * j - dx * (cn - 1) / 2 > b1[i].r[0] > dx * j - dx * (cn + 1) / 2 > b1[i].r[0] - radius and \
                    b1[i].r[1] < -dy * (cn - 1) - 2 + radius:
                b1[i].r[0] = radius + dx * j - dx * (cn + 1) / 2
                b1[i].v[0] = -b1[i].v[0] * parfactor
    return b1


# 定义互相碰撞
def bounceeachother(b1, b2):
    k1 = 0.98  # 两小球碰撞因子
    en = (b1.r - b2.r) / (np.linalg.norm(b1.r - b2.r))
    ef = getvertical_vector(en)
    vf1 = ef * np.dot(b1.v, ef)
    vf2 = ef * np.dot(b2.v, ef)
    vn1 = en * np.dot(b1.v, en)
    vn2 = en * np.dot(b2.v, en)
    b1.v = vf1 + k1 * vn2
    b2.v = vf2 + k1 * vn1
    r0 = (b1.r + b2.r) / 2
    b1.r = r0 + Ball.radius * en
    b2.r = r0 - Ball.radius * en
    return b1, b2


def update(index):
    global ball
    ball = freefall(ball)
    ball = bouncewall(ball)
    ball = bouncefunnel(ball)
    ball = bouncepartip(ball)
    for i in range(ballnum):
        for j in range(i + 1, ballnum):
            if np.linalg.norm(ball[i].r - ball[j].r) - 2 * Ball.radius <= 0:
                ball[i], ball[j] = bounceeachother(ball[i], ball[j])
        # 判断小球是否触及钉子
        for k in range(nailnum):
            if np.linalg.norm(ball[i].r - nail[k].r) - Ball.radius - Nail.rnail <= 0:
                ball[i] = bouncenail(ball[i], nail[k])

    for i in range(ballnum):
        balls[i].set_center(ball[i].r)
    return balls


ballnum = 100  # 小球数量
# 设置xy轴范围
xmin = -32
ymin = -44
ymax = 32
xmax = 32
# 定义高尔顿板钉子的参数
dx = 4.8  # 横向间距
dy = 2.5  # 纵向间距
cn = 14  # 层数
# 定义侧板位置
sx, sy = 4, 34
nailnum = int(cn * (cn + 1) / 2)  # 钉子总数
ball = []
nail = []

for i in range(ballnum):
    xi = random.uniform(xmin + Ball.radius, xmax - Ball.radius)
    yi = random.uniform(10, ymax - Ball.radius)
    vxi = random.uniform(0, 0)
    vyi = random.uniform(0, -10)
    r = [xi, yi]
    v = [vxi, vyi]
    ball.append(Ball(r, v))

# 循环定义各钉子的位置
for i in range(cn):
    for j in range(i + 1):
        r = [dx * j - dx * i / 2, -dy * i]
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
    exec("gline%d = Line2D([dx*i-dx*(cn-1)/2, dx*i-dx*(cn-1)/2], [ymin, -dy*(cn-1)-2], color='black')" % (i + 1))
    eval('ax.add_line(gline%d)' % (i + 1))
# 绘制各小球
colorlist = ['red', 'green', 'blue', 'orange', 'pink', 'yellow', 'brown', 'black']
for i in range(ballnum):
    balls.append(plt.Circle((ball[i].r), Ball.radius, fc=colorlist[i % 8]))
    ax.add_patch(balls[i])
# 绘制钉子
for i in range(nailnum):
    nails.append(plt.Circle((nail[i].r), Nail.rnail, fc='black'))
    ax.add_patch(nails[i])

anim = animation.FuncAnimation(fig, update, frames=200, blit=True, interval=10)
plt.show()
