
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
k=-0.1
dt=0.01
n=10
factor=1
xmax=10
ymax=10
g=np.array([0,-9.8])
class Ball():
    radius = (xmax-0)/(5*n)
    def __init__(self,r,v):
        self.r=np.array(r)
        self.v=np.array(v)

# temp_ball=ball
# print(ball[0].r,ball[0].v)
# print(ball[1].r,ball[1].v)
# for i in range(2):
#     a=np.array([0,0])
#     for j in range(2):
#         if j!=i :
#             a=a+k*(temp_ball[i].r-temp_ball[j].r)*(np.linalg.norm(temp_ball[i].r-temp_ball[j].r)**(3))
#     ball[i].r=temp_ball[i].r+temp_ball[i].v*dt
#     ball[i].v=temp_ball[i].v+a*dt
#     # print(a)

def getvertical_vector(vec):
    return np.array([vec[1],-vec[0]])
def beo(b1,b2):
    vτ1=np.array([0,0])
    en=(b1.r-b2.r)/(np.linalg.norm(b1.r-b2.r))
    eτ=getvertical_vector(en)
    # print(eτ,en)
    vτ1=eτ*np.dot(b1.v,eτ)
    vτ2=eτ*np.dot(b2.v,eτ)
    vn1=en*np.dot(b1.v,en)
    vn2=en*np.dot(b2.v,en)
    b1.v=vτ1+vn2
    b2.v=vτ2+vn1
    r0=(b1.r+b2.r)/2
    b1.r=r0+Ball.radius*en
    b2.r=r0-Ball.radius*en
    return b1,b2
# ball[0],ball[1]=beo_v(ball[0],ball[1])
# print(ball[0].r,ball[0].v)
# print(ball[1].r,ball[1].v)
def bw(ball):
    tb=ball
    for i in range(n):
        if ball[i].r[0] - Ball.radius < 0 :
           tb[i].r[0] = Ball.radius
           tb[i].v[0] = -ball[i].v[0]*factor
        elif ball[i].r[0]+Ball.radius-xmax  > 0 :
           tb[i].r[0] = xmax-Ball.radius
           tb[i].v[0] = -ball[i].v[0]*factor
        if ball[i].r[1] - Ball.radius < 0 :
           tb[i].r[1] = Ball.radius
           tb[i].v[1] = -ball[i].v[1]*factor
        elif ball[i].r[1]+Ball.radius-ymax  > 0 :
           tb[i].r[1] = ymax-Ball.radius
           tb[i].v[1] = -ball[i].v[1]*factor
    return tb 
def freefall(ball):
    tb=ball
    for i in range(n):
        tb[i].r=ball[i].r+ball[i].v*dt
        tb[i].v=ball[i].v+g*dt
    return tb
def move(ball):
    temp_ball=ball
    for i in range(n):
        a=np.array([0,0])
        for j in range(n):
            if j!=i :
                # print(np.linalg.norm(temp_ball[i].r-temp_ball[j].r)**(3))
                a=a+k*(temp_ball[i].r-temp_ball[j].r)*(np.linalg.norm(temp_ball[i].r-temp_ball[j].r)**(0))
        ball[i].r=temp_ball[i].r+temp_ball[i].v*dt
        ball[i].v=temp_ball[i].v+a*dt
    return ball
def update(index):
    global ball 
    ball=move(ball)
    print(ball[1].r)
    ball=bw(ball)
    for i in range(n):
        for j in range(i + 1, n):
            if np.linalg.norm(ball[i].r-ball[j].r)-2*Ball.radius<=0 :
                ball[i],ball[j] = beo(ball[i],ball[j])
    #循环定义各球的位置
    
    for i in range(n):
        # print(ball[0].r)
        balls[i].set_center((ball[i].r))
    return balls

ball=[]

for i in range(n):
    xi=random.uniform(Ball.radius,10-Ball.radius)
    yi=random.uniform(Ball.radius,10-Ball.radius)
    vxi=random.uniform(0,0.1)
    vyi=random.uniform(0,0.1)
    r=[xi,yi]
    v=[vxi,vyi]
    ball.append(Ball(r,v))

balls=[]
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(0, xmax)
ax.set_ylim(0, ymax)
ax.set_title("bouncing balls")
color=['red','blue','black']
for i in range(n):
    balls.append(plt.Circle((ball[i].r), Ball.radius, fc=color[i%3]))
    ax.add_patch(balls[i])
# balls.append(plt.Circle((ball[0].r[0], ball[0].r[1]), Ball.radius, fc='red'))
# ax.add_patch(balls[0])
# balls.append(plt.Circle((ball[1].r[0], ball[1].r[1]), Ball.radius, fc='red'))
# ax.add_patch(balls[1])
anim = animation.FuncAnimation(fig, update, frames=200, blit=True, interval=5)
plt.show()