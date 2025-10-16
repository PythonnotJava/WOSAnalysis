import matplotlib.pyplot as plt
from matplotlib import rcParams

def init():
    # rcParams['font.family'] = 'Times New Roman'
    rcParams['font.family'] = 'Microsoft YaHei'

    plt.rcParams['axes.labelsize'] = 18  # 轴标签字体大小
    plt.rcParams['xtick.labelsize'] = 16  # x轴刻度字体大小
    plt.rcParams['ytick.labelsize'] = 16  # y轴刻度字体大小
    rcParams['axes.labelsize'] = 16  # 设置坐标轴标签大小（这里 12pt = 小四号）