import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
def main():
    fig,ax=plt.subplot(1,1)
    ax.set_title('physical proceudre')
    ax.set_xlim(0, 1), ax.set_xticks([])  # 设置x、y轴范围，取消显示刻度
    ax.set_ylim(0, 1), ax.set_yticks([])
    
if __name__ == '__main__':
    main()