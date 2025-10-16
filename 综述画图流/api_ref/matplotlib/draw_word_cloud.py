from typing import *
from wordcloud import WordCloud
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

# 画词云图
def draw_word_cloud(
    data : dict,
    title : Optional[str] = '',
    width=1600,
    height=1000,
    bgc : str = 'mintcream',
    color_func=None,
    max_font_size=300,  # 最大字号更大
    relative_scaling=0.3,  # 越大差距越明显
    **kwargs
) -> Figure:
    wordcloud : WordCloud = WordCloud(
        width=width,
        height=height,
        background_color=bgc,
        margin=0,
        prefer_horizontal=1.0,
        color_func=color_func,
        max_font_size=max_font_size,  # 最大字号更大
        relative_scaling=relative_scaling,  # 越大差距越明显
    ).generate_from_frequencies(data)

    fig = plt.figure(figsize=(width / 100, height / 100), dpi=100)
    ax : Axes = fig.gca()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_axis_off()
    fig.subplots_adjust(left=0, right=1, top=0.9, bottom=0)

    if title:
        ax.set_title(title)
    ax.set(**kwargs)
    return fig

