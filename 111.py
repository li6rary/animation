"八个球在给定二维区域内受重力影响下的运动，球与球之间取完全弹性碰撞，球与边界的碰撞受碰撞系数影响"
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random

g = -9.81  # m/s^2
dt = 0.01  # 取的小时间微元
factor = 0.85  # 碰撞系数
n=10 #球的数量
xmin,xmax = 0,10  #定义水平距离
ymin,ymax = 0,10  #定义垂直高度
radius = (ymax-ymin)/(2*n) #半径
#定义小球初始化位置速度的区间
ximin = radius 
ximax = xmax-radius
yimin = radius
yimax = ymax-radius 
vimin,vimax = 0 , 1

#定义Ball类
class Ball():
    def __init__(self,x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
def bw(ball):
# 判断球撞地
    if ball.y - radius < 0:
        ball.y = radius
        ball.vy = -ball.vy * factor
    # 判断球撞天花板
    elif ball.y + radius > ymax:
        ball.y = ymax - radius
        ball.vy = -ball.vy * factor
    # 判断球撞右墙
    if ball.x + radius > xmax:
        ball.x = xmax - radius
        ball.vx = -ball.vx * factor
    # 判断球撞左墙
    elif ball.x - radius < 0:
        ball.x = radius
        ball.vx = -ball.vx * factor
    return ball                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
#创造小球实例
ball=[]
for i in range(n):
    xi=random.uniform(Ball.radius,10-Ball.radius)
    yi=random.uniform(Ball.radius,10-Ball.radius)
    vxi=random.uniform(vimin,vimax)
    vyi=random.uniform(vimin,vimax)
    ball.append(Ball(xi,yi,vxi,vyi))
# 所有ball在dt时间后的物理量
def movedt(ball):
    for i in range(n):
      vi=np.array([ball.vx,ball.vy])
    return [vx, x, vy, y]


# 定义碰撞边界时的运动
def bouncewall(vx, x, vy, y):
    # 判断球撞地
    if y - radius < 0:
        y = radius
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
    global p,xc,yc
    # 自由落体
    xc = 0
    yc = 0
    for i in range(len(p)):
        p[i] = freefall(p[i][0], p[i][1], p[i][2], p[i][3])

    # 判断是否触及边界
    for i in range(len(p)):
        p[i] = bouncewall(p[i][0], p[i][1], p[i][2], p[i][3])

    # 判断两小球相撞
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if (p[i][1] - p[j][1]) ** 2 + (p[i][3] - p[j][3]) ** 2 < 4 * radius ** 2:
                p[i], p[j] = bounceeachother(p[i][0], p[i][1], p[i][2], p[i][3], p[j][0], p[j][1], p[j][2], p[j][3])

    # 循环定义各球的位置
    for i in range(len(p)):
        exec('ball%s.set_center((p[i][1], p[i][3]))' % str(i+1))
    
    for i in range(len(p)):
        xc=xc+p[i][1]/8
        yc=yc+p[i][3]/8
    center.set_center((xc, yc))
    text.set_text('centre of mass:%.4f %.4f'%(xc,yc))
    return ball1, ball2, ball3, ball4, ball5, ball6, ball7, ball8,text,center


# 建立图形，设置横纵轴范围，要求横纵轴等长
fig, ax = plt.subplots()
# ax.axis('scaled')
ax.set_aspect('equal')
ax.set_xlim(0, xmax)
ax.set_ylim(0, ymax)
ax.set_title("bouncing balls")
ax.text(1,8,'factor=%.2f'%factor)
text=plt.text(1,2,'centre of mass:%.4f %.4f'%(xc,yc),alpha=0.5)
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
# 设置质心
center = plt.Circle((xc, yc), 0.1, fc='black')
ax.add_patch(center)

anim = animation.FuncAnimation(fig, update, frames=200, blit=True, interval=5)
plt.show()