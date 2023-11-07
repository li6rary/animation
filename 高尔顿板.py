# 高尔顿板模拟程序，可以自由改变小球的数量、半径、钉子层数、间距以及各碰撞系数等。
import random
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation

try:
    radius = 0.6  # 小球半径
    ballnum = 100  # 小球数量
    g = -9.81  # m/s^2
    dt = 0.01  # 取的小时间微元
    # 设置xy轴范围
    xmin = -32
    ymin = -44
    ymax = 32
    xmax = 32
    # 定义高尔顿板钉子的参数
    rnail = 0.2  # 钉子的半径
    dx = 4.8  # 横向间距
    dy = 2.5  # 纵向间距
    cn = 12  # 层数
    # 定义侧板位置
    sx, sy = 2, 33
    # 定义各碰撞系数
    factor = 0.1  # 与边界的碰撞系数
    railfactor = 0.98  # 与钉子碰撞的碰撞系数
    funnelfactor = 0.8  # 与漏斗碰撞的碰撞系数
    parfactor = 0.5  # 与下方隔板的碰撞系数
    p = []  # 用于存放各小球的速度与位置
    # 随机生成小球的位置
    for i in range(ballnum):
        exec('vx%d,x%d,vy%d,y%d=0,random.uniform(xmin+radius,xmax-radius),0,random.uniform(14,ymax-radius)' % (
            i + 1, i + 1, i + 1, i + 1))
        eval('p.append([vx%d, x%d, vy%d, y%d])' % (i + 1, i + 1, i + 1, i + 1))
    # 生成update函数返回内容
    balllist = ""
    for i in range(ballnum):
        exec("balllist = balllist + 'ball' + str(i+1) +', '")
    nailpo = []
    naillist = ""
    for i in range(cn):
        for j in range(i + 1):
            exec("naillist = naillist + 'nail' + str(i) + str(j) +', '")
            nailpo.append([dx * j - dx * i / 2, -dy * i])
    nailnum = len(nailpo)  # 钉子总数


    # 定义自由落体函数
    def freefall(vx, x, vy, y):
        x += vx * dt
        y += vy * dt
        vy += g * dt
        return [vx, x, vy, y]


    # 定义碰撞边界时的运动
    def bouncewall(vx, x, vy, y):
        # 判断球撞地
        if y - radius < ymin:
            y = radius + ymin
            vy = -vy * factor
        # 判断球撞天花板
        elif y + radius > ymax:
            y = ymax - radius
            vy = -vy * factor
        # 判断球撞右墙
        if x + radius > xmax:
            x = xmax - radius
            vx = -vx * factor
        # 判断球撞左墙
        elif x - radius < xmin:
            x = radius + xmin
            vx = -vx * factor
        return [vx, x, vy, y]


    # 定义碰撞钉子
    def bouncenail(vbx1, xb1, vby1, yb1, xb2, yb2):
        a = (yb1 - yb2) / (xb1 - xb2)
        xb1 = (xb1 + xb2) / 2 + radius * (xb1 - xb2) / ((xb1 - xb2) ** 2 + (yb1 - yb2) ** 2) ** 0.5
        yb1 = (yb1 + yb2) / 2 + radius * (yb1 - yb2) / ((xb1 - xb2) ** 2 + (yb1 - yb2) ** 2) ** 0.5
        vbxf = railfactor * ((a ** 2 + a * a) * vbx1 - 2 * a * vby1) / (a * a + 2 + a * a)
        vbyf = railfactor * vby1 + a * (-2 * vbx1 - 2 * a * vby1) / (a * a + 2 + a * a)
        vbx1 = vbxf
        vby1 = vbyf
        return [vbx1, xb1, vby1, yb1]


    # 定义碰撞上方漏斗
    def bouncefunnel(vx, x, vy, y):
        # 判断碰到左侧上壁
        if x + y < -sx + 1.414 * radius and x < -sx + radius / 1.414 and y > radius / 1.414:
            xf = 1.414 * radius - sx - y
            yf = 1.414 * radius - sx - x
            x = xf
            y = yf
            vxf = -vy
            vyf = -vx
            vx = funnelfactor * vxf
            vy = funnelfactor * vyf
        # 判断碰到右侧上壁
        elif y - x < -sx + 1.414 * radius and x > sx - radius / 1.414 and y > radius / 1.414:
            xf = -1.414 * radius + sx + y
            yf = 1.414 * radius - sx + x
            x = xf
            y = yf
            vxf = vy
            vyf = vx
            vx = funnelfactor * vxf
            vy = funnelfactor * vyf
        # 判断碰到左侧下壁
        elif y - x > sx - 1.414 * radius and x < -sx + radius / 1.414 and y < -radius / 1.414:
            xf = 1.414 * radius - sx + y
            yf = -1.414 * radius + sx + x
            x = xf
            y = yf
            vxf = vy
            vyf = vx
            vx = funnelfactor * vxf
            vy = funnelfactor * vyf
        # 判断碰到右侧下壁
        elif x + y > sx - 1.414 * radius and x > sx - radius / 1.414 and y < -radius / 1.414:
            xf = -1.414 * radius + sx - y
            yf = -1.414 * radius + sx - x
            x = xf
            y = yf
            vxf = -vy
            vyf = -vx
            vx = funnelfactor * vxf
            vy = funnelfactor * vyf
        return [vx, x, vy, y]


    # 小球与下方隔板的碰撞
    def bouncepartip(vx, x, vy, y):
        for i in range(cn):
            if dx * i - dx * (cn + 1) / 2 < x < dx * i - dx * (cn - 1) / 2 < x + radius and y < -dy * (cn - 1) - 2:
                x = dx * i - dx * (cn - 1) / 2 - radius
                vx = -vx * parfactor
            elif dx * i - dx * (cn - 1) / 2 > x > dx * i - dx * (cn + 1) / 2 > x - radius and y < -dy * (cn - 1) - 2:
                x = radius + dx * i - dx * (cn + 1) / 2
                vx = -vx * parfactor
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
        for i in range(ballnum):
            # 自由落体
            p[i] = freefall(p[i][0], p[i][1], p[i][2], p[i][3])

        for i in range(ballnum):
            # 判断是否触及边界、漏斗与隔板
            p[i] = bouncewall(p[i][0], p[i][1], p[i][2], p[i][3])
            p[i] = bouncefunnel(p[i][0], p[i][1], p[i][2], p[i][3])
            p[i] = bouncepartip(p[i][0], p[i][1], p[i][2], p[i][3])

        for i in range(ballnum):
            # 判断小球是否触及钉子
            for j in range(nailnum):
                if (p[i][1] - nailpo[j][0]) ** 2 + (p[i][3] - nailpo[j][1]) ** 2 < (rnail + radius) ** 2:
                    p[i] = bouncenail(p[i][0], p[i][1], p[i][2], p[i][3], nailpo[j][0], nailpo[j][1])
            # 判断两小球相撞
            for k in range(i + 1, ballnum):
                if (p[i][1] - p[k][1]) ** 2 + (p[i][3] - p[k][3]) ** 2 < 4 * radius ** 2:
                    p[i], p[k] = bounceeachother(p[i][0], p[i][1], p[i][2], p[i][3], p[k][0], p[k][1], p[k][2], p[k][3])
            # 循环定义各球的位置
            eval('ball%d.set_center((p[i][1], p[i][3]))' % (i + 1))

        # 定义漏斗
        line1.set_data([sx, sy], [0, sy - sx])
        line2.set_data([-sx, -sy], [0, sy - sx])
        line3.set_data([sx, sy], [0, -(sy - sx)])
        line4.set_data([-sx, -sy], [0, -(sy - sx)])

        # 循环定义各钉子的位置
        for i in range(cn):
            for j in range(i + 1):
                eval('nail%d%d.set_center((dx*j-dx*i/2, -dy*i))' % (i, j))

        # 循环定义下方隔板
        for i in range(cn):
            eval('gline%d.set_data([dx*i-dx*(cn-1)/2, dx*i-dx*(cn-1)/2],[ymin, -dy*(cn-1)-2])' % (i + 1))

        return eval(balllist + naillist + 'line1, line2, line3, line4')


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
        exec("ball{} = plt.Circle((x{}, y{}), radius, fc=colorlist[i%8], color='black')"
             .format(str(i + 1), str(i + 1), str(i + 1)))
        eval('ax.add_patch(ball%d)' % (i + 1))
    # 绘制钉子
    for i in range(cn):
        for j in range(i + 1):
            exec("nail%d%d = plt.Circle((dx*j-dx*i/2, -dy*i), rnail, fc='black')" % (i, j))
            eval('ax.add_patch(nail%s%s)' % (str(i), str(j)))

    anim = animation.FuncAnimation(fig, update, frames=200, blit=True, interval=10)
    plt.show()

except Exception as e:
    print(e)
