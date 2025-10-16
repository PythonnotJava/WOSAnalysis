import matplotlib.pyplot as plt
from matplotlib.axes import Axes

# 画纵向柱状图
def draw_bar_v(data : dict, xlabel : str, ylabel : str, title : str, **kwargs):
    keys = list(data.keys())
    values = list(data.values())
    fig = plt.figure()
    ax : Axes = fig.gca()
    ax.bar(keys, values, width=.8)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set(**kwargs)
    plt.tight_layout()
    return fig
