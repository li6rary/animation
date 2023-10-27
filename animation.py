# Simulates rain drops on a surface by animating the scale and opacity of 50 scatter points.
# Based on:
# Author: Nicolas P. Rougier （https://matplotlib.org/3.1.1/gallery/animation/rain.html）
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots(figsize=(6, 6), frameon=True)
ax.set_xlim(0, 1), ax.set_xticks([])  # 设置x、y轴范围，取消显示刻度
ax.set_ylim(0, 1), ax.set_yticks([])
np.random.seed(19680801)
n_drops = 50
rain_drops = np.zeros(n_drops, dtype=[('position', float, 2),
                                      ('size', float, 1),
                                      ('growth', float, 1),
                                      ('color', float, 4)])
rain_drops['position'] = np.random.uniform(0, 1, (n_drops, 2))
rain_drops['growth'] = np.random.uniform(50, 200, n_drops)
scat = ax.scatter(rain_drops['position'][:, 0], rain_drops['position'][:, 1],
                  s=rain_drops['size'], lw=0.5, edgecolors=rain_drops['color'],
                  facecolors='none')


def update(frame_number):
    current_index = frame_number % n_drops
    rain_drops['color'][:, 3] -= 1.0 / len(rain_drops)  # 变化到透明（0）
    rain_drops['color'][:, 3] = np.clip(rain_drops['color'][:, 3], 0, 1)
    rain_drops['size'] += rain_drops['growth']
    # 对特定雨滴属性进行初始化，每次只初始化current_index指定的一个雨滴
    rain_drops['position'][current_index] = np.random.uniform(0, 1, 2)
    rain_drops['size'][current_index] = 5
    rain_drops['growth'][current_index] = np.random.uniform(50, 200)  # 增长速度不同
    rain_drops['color'][current_index] = (0, 0, 0, 1)

    scat.set_offsets(rain_drops['position'])
    scat.set_sizes(rain_drops['size'])
    scat.set_edgecolors(rain_drops['color'])


animation = FuncAnimation(fig, update, interval=10)
plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
plt.show()