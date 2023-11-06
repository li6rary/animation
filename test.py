import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random

factor=0.85
ymax=10
xmax=10
ymin=0
xmim=0
n=5
vximax=2
vyimax=2
vximin=0
vyimin=0
dt=0.1
k=0.001
class Ball():
    radius = (ymax-ymin)/(2*n)
    def __init__(self,r,v):
        self.r=np.array(r)
        self.v=np.array(v)
ball=[]
for i in range(n):
    xi=random.uniform(Ball.radius,10-Ball.radius)
    yi=random.uniform(Ball.radius,10-Ball.radius)
    vxi=random.uniform(vximin,vximax)
    vyi=random.uniform(vyimin,vyimax)
    r=[xi,yi]
    v=[vxi,vyi]
    ball.append(Ball(r,v))

def bouncewall(ball):
    for i in range(n):
        if ball[i].r[0] - Ball.radius < 0 :
           ball[i].r[0] = Ball.radius
           ball[i].v[0] = -ball[i].v[0]*factor
        if ball[i].r[0]+Ball.radius-xmax  < 0 :
           ball[i].r[0] = xmax-Ball.radius
           ball[i].v[0] = -ball[i].v[0]*factor
        if ball[i].r[1] - Ball.radius < 0 :
           ball[i].r[1] = Ball.radius
           ball[i].v[1] = -ball[i].v[1]*factor
        if ball[i].r[1]+Ball.radius-ymax  < 0 :
           ball[i].r[1] = ymax-Ball.radius
           ball[i].v[1] = -ball[i].v[1]*factor
    return ball
def getvertical_vector(vec):
    return np.array([vec[1],-vec[0]])
#小球受力运动dt时间
def move(ball):
    temp_ball=ball
    for i in range(n):
        a=np.array([0,0])
        for j in range(n):
            if j!=i :
                print(np.linalg.norm(temp_ball[i].r-temp_ball[j].r)**(3))
                a=a+k*(temp_ball[i].r-temp_ball[j].r)*(np.linalg.norm(temp_ball[i].r-temp_ball[j].r)**(3))
        ball[i].r=temp_ball[i].r+temp_ball[i].v*dt
        ball[i].v=temp_ball[i].v+a*dt
    return ball
#计算球相撞后速度变化
def beo_v(b1,b2):
    vτ1=np.array([0,0])
    en=(b1.r-b2.r)/(np.linalg.norm(b1.r-b2.r))
    eτ=getvertical_vector(en)
    vτ1=eτ*np.dot(b1.v,eτ)
    vτ2=eτ*np.dot(b2.v,eτ)
    vn1=en*np.dot(b1.v,en)
    vn2=en*np.dot(b2.v,en)
    b1.v=vτ1+vn2
    b2.v=vτ2+vn1
    return b1,b2
#初始化球相撞后的位置
def beo_r(b1,b2):
    en=(b1.r-b2.r)/(np.linalg.norm(b1.r-b2.r))
    r0=(b1.r+b2.r)/2
    b1.r=r0-Ball.radius*en
    b2.r=r0+Ball.radius*en
    return b1,b2




def update(index):
    global ball
    # 自由落体
    for i in range(n):
        ball = move(ball)

    # 判断是否触及边界
    ball=bouncewall(ball)
    # 判断两小球相撞
    for i in range(n):
        for j in range(i + 1, n):
            if np.linalg.norm(ball[i].r-ball[j].r)-Ball.radius<0 :
                ball[i],ball[j] = beo_v(ball[i],ball[j])
                ball[i],ball[j] = beo_r(ball[i],ball[j])

    # 循环定义各球的位置
    # for i in range(n):
    #     balls[i].set_center((ball[i].r[0] , ball[i].r[1]))
    
    # for i in range(n):
    #     exec('ball%s.set_center((ball[i].r[0], ball[i].r[1]))' % str(i+1))
    print('%.3f %.3f'%(ball[0].r[0],ball[0].r[1]))
    ball0.set_center((ball[0].r[0], ball[0].r[1]))
    ball1.set_center((ball[1].r[0], ball[1].r[1]))

    return ball0,ball1


# 建立图形，设置横纵轴范围，要求横纵轴等长
fig, ax = plt.subplots()

ax.set_aspect('equal')
ax.set_xlim(0, xmax)
ax.set_ylim(0, ymax)
ax.set_title("bouncing balls")

balls=[]
ball=[]


ball0 = plt.Circle((ball[0].r[0], ball[0].r[1]), Ball.radius, fc='red')
ax.add_patch(ball0)
ball1 = plt.Circle((ball[1].r[0], ball[1].r[1]), Ball.radius, fc='green')
ax.add_patch(ball1)
# ball3 = plt.Circle((x3, y3), Ball.radius, fc='blue')
# ax.add_patch(ball3)
# ball4 = plt.Circle((x4, y4), Ball.radius, fc='orange')
# ax.add_patch(ball4)
# ball5 = plt.Circle((x5, y5), Ball.radius, fc='pink')
# ax.add_patch(ball5)


anim = animation.FuncAnimation(fig, update, frames=20000000, blit=True, interval=5)
plt.show()