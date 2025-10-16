import matplotlib.pyplot as plt
from matplotlib.axes import Axes

# 画横向柱状图
def draw_bar_h_matplotlib(data : dict, xlabel : str, ylabel : str, title : str, **kwargs):
    keys = list(data.keys())
    values = list(data.values())
    fig = plt.figure()
    ax : Axes = fig.gca()
    ax.barh(keys, values)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set(**kwargs)
    plt.tight_layout()
    return fig
