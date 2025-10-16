# 柱状图中添加折线图反应趋势
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from typing import Optional

def draw_bar_with_plot(
    data_bar: dict,
    data_line: Optional[dict] = None,
    xlabel: str = '',
    ylabel: str = '',
    title: str = '',
    line_color: str = '#e63946',
    bar_color: str = '#457b9d',
    **kwargs
) -> Figure:
    """
    画柱状图 + 折线图叠加图（共享同一个Y轴）
    折线点精确对齐柱顶中心。
    """
    keys = list(data_bar.keys())
    bar_values = list(data_bar.values())

    if data_line is None:
        data_line = data_bar
    line_values = [data_line.get(k, 0) for k in keys]

    fig, ax = plt.subplots()

    bar_width = 0.7
    x = range(len(keys))

    # --- 柱状图 ---
    bars = ax.bar(x, bar_values, color=bar_color, alpha=0.75, width=bar_width, label='Bar')

    # --- 折线图：共享Y轴 ---
    # ✅ 用每根柱子的中心点作为折线的x位置
    line_x = [bar.get_x() + bar.get_width() / 2 for bar in bars]
    ax.plot(line_x, line_values, color=line_color, marker='o', linewidth=2.5, label='Line')

    # --- 坐标轴与标题 ---
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks(x)
    ax.set_xticklabels(keys)
    ax.set_title(title)
    ax.set(**kwargs)

    # --- 图例 ---
    ax.legend(loc='upper left')

    fig.tight_layout()
    return fig
