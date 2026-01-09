import random
from typing import Optional

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib import rcParams
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from WOSPie import ChartWindow, draw_pie_more
from WOSUtil import *

# 设置字体族，首选 'Times New Roman' (类似“新罗马”)
rcParams['font.family'] = 'Times New Roman'
# 设置中文字体优先级
# rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial']
# 负号正常显示
rcParams['axes.unicode_minus'] = False

# 画横向柱状图
def draw_bar_h(data : dict, xlabel : str, ylabel : str, title : str, **kwargs):
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

def dark_blue_black_purple(*args, **kwargs):
    # 候选深色
    colors = [
        "#2e2e6f",  # 深蓝
        "#000080",  # 藏青
        "#4b0082",  # 靛蓝
        "#301934",  # 深紫
        "#191970",  # 午夜蓝
        "#2c003e" ,
        "#8dda91",
        "#fbeb4e",
        "#2e6e8e"
    ]
    return random.choice(colors)

# 画词云图
def draw_word_cloud(
    data : dict,
    title : Optional[str] = '',
    width=1600,
    height=1000,
    bgc : str = 'mintcream',
    color_func=None,
        max_font_size=300,  # 最大字号更大
        relative_scaling=0.5,  # 越大差距越明显
    **kwargs
) -> Figure:
    wordcloud : WordCloud = WordCloud(
        width=width,
        height=height,
        background_color=bgc,
        margin=0,
        prefer_horizontal=1.0,
        color_func=color_func,
        max_font_size=300,  # 最大字号更大
        relative_scaling=0.3,  # 越大差距越明显
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

import plotly.graph_objects as go

# 新引擎
def draw_bar_with_plot_by_plotly(
    data_bar: dict,
    data_line: Optional[dict] = None,
    xlabel: str = '',
    ylabel: str = '',
    title: str = '',
    bar_color: str = '#457b9d',
    line_color: str = '#e63946',
    **kwargs
):
    keys = list(data_bar.keys())
    bar_values = list(data_bar.values())

    if data_line is None:
        data_line = data_bar
    line_values = [data_line.get(k, 0) for k in keys]

    fig = go.Figure()

    # --- 柱状图 ---
    fig.add_trace(go.Bar(
        x=keys,
        y=bar_values,
        name=ylabel or 'Bar',
        marker_color=bar_color,
        opacity=0.75
    ))

    # --- 折线图（共享y轴） ---
    fig.add_trace(go.Scatter(
        x=keys,
        y=line_values,
        mode='lines+markers',
        name='Trend',
        line=dict(color=line_color, width=3),
        marker=dict(size=8)
    ))

    # --- 美化布局 ---
    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        template='plotly_white',
        legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0)', bordercolor='rgba(0,0,0,0)'),
        **kwargs
    )

    # 可以保存为静态图或 HTML
    # fig.write_image("out/年份变化.png", scale=3)
    # fig.write_html("out/年份变化.html")

    return fig

from pyecharts.charts import WordCloud as WordCloud_pyecharts
from pyecharts import options as opts

def draw_word_cloud_by_pyecharts(
    data: dict,
    title: str = '',
    width: int = 1600,
    height: int = 1000,
    bgc: str = 'rgba(255,255,255,0)',  # 背景透明
    color_func=None,
    **kwargs
) -> WordCloud_pyecharts:
    """
    绘制现代词云（使用 pyecharts 引擎）
    """
    words = [(k, int(v)) for k, v in data.items()]
    wc = (
        WordCloud_pyecharts(init_opts=opts.InitOpts(width=f"{width}px", height=f"{height}px", bg_color=bgc))
        .add(
            "",
            words,
            word_size_range=[12, 80],
            shape="circle",  # 可改为 "diamond", "star", "pentagon"
            rotate_step=30,
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=title,
                title_textstyle_opts=opts.TextStyleOpts(font_size=22),
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    )
    return wc

# records = load('savedrecs.txt')

# 年份统计
# years = [match_py(e) for e in records]
# years_data = get_count_single(years)
# years_data = SliceableDict(sort_by_key(years_data))[:]
# fig = draw_bar_v(years_data, 'Year', 'Number of published articles', 'Published articles by year')
# fig.set_size_inches(10, 8)
# fig.set_dpi(150)
# fig.savefig('out/年份变化.png')
# plt.show()

# 期刊收集统计
# journals = [match_so(e) for e in records]
# journals_data = get_count_single(journals)
# journals_data = sort_by_value(journals_data, reverse=True)
# journals_data_top20 = SliceableDict(journals_data)[:20]
# 期刊全系列词云
# fig = draw_word_cloud(journals_data, None)
# fig.savefig('out/期刊词云.png')
# 期刊前20，考虑到期刊名字较长，图会偏移，需要适当调整
# fig = draw_bar_h(journals_data_top20, 'Journal collection', 'Journal', 'Top 20 journals indexed')
# fig.set_size_inches(10, 8)
# fig.set_dpi(150)
# plt.title(fig.gca().get_title(), x=-.25)
# plt.subplots_adjust(left=0.6)
# fig.savefig('out/期刊前20.png')
# plt.show()

# 引用前20名的表格，带DOI和引用数
# reference = sort_by_z9(records)
# reference_top20 = SliceableDict(reference)[:20]
# reference_with_doi = sort_by_z9_doi(records, True)
# reference_top20_with_doi = SliceableDict(sort_by_point_value(reference_with_doi, 0))[:20]
# gen_word_table(reference_top20_with_doi, 'out')

# 学科分类
# subjects = get_count_mult([match_wc(e) for e in records])
# subjects_data = SliceableDict(sort_by_value(subjects, reverse=True))[:]
# fig = draw_bar_h(subjects_data, 'Number of records', 'Subject', 'Statistics by discipline')
# fig.gca().tick_params(axis='y', labelsize=8)
# fig.savefig('out/学科分类.png')
# fig.set_size_inches(10, 8)
# fig.set_dpi(150)
# plt.show()
# 饼状图
# draw_pie_more(subjects_data, 'Statistics by discipline', 20)

# 研究领域
# researchArea = []
# for e in records:
#     k = match_sc(e)
#     if k:
#         researchArea.append(match_sc(e))
# researchArea_data = get_count_mult(researchArea)
# researchArea_data = SliceableDict(sort_by_value(researchArea_data, reverse=True))[:]
# fig = draw_bar_h(researchArea_data, 'Quantity', 'Field for research', 'Research field statistics')
# fig.set_size_inches(10, 8)
# fig.set_dpi(150)
# fig.savefig('out/研究领域.png')
# plt.show()
# 画饼状图
# draw_pie_more(researchArea_data, 'Research field statistics', 12)

# 出版商
# publisher = [match_pu(r) for r in records]
# publisher_data = get_count_single(publisher)
# publisher_data = SliceableDict(sort_by_value(publisher_data, True))[:]
# fig = draw_bar_h(publisher_data, 'Quantity', 'Name', 'Article attribution to publisher statistics')
# fig.gca().tick_params(axis='y', labelsize=8)
# fig.set_size_inches(10, 8)
# fig.set_dpi(150)
# fig.savefig('out/出版商统计.png')
# plt.show()
# 画饼状图
# draw_pie_more(publisher_data, 'Article attribution to publisher statistics')

if __name__ == '__main__':
    # rcParams['font.family'] = 'Times New Roman'
    rcParams['font.family'] = 'Microsoft YaHei'

    plt.rcParams['axes.labelsize'] = 18  # 轴标签字体大小
    plt.rcParams['xtick.labelsize'] = 16  # x轴刻度字体大小
    plt.rcParams['ytick.labelsize'] = 16  # y轴刻度字体大小
    rcParams['axes.labelsize'] = 16  # 设置坐标轴标签大小（这里 12pt = 小四号）

    # file = merge_large_text_file('src/1.txt', 'src/2.txt', 'src/main.txt')

    records = load('src/1.9.txt')


    # years = [match_py(e) for e in records]
    # years_data = get_count_single(years)
    # {'2022': 97, '2024': 124, '2017': 51, '2025': 142, '2023': 117, '2014': 45, '2021': 82, '2018': 66, '2020': 69,
    #  '2016': 43, '2019': 75, '2015': 39}
    # years_data = SliceableDict(sort_by_key(years_data))[:]
    # fig = draw_bar_with_plot(years_data, xlabel='Year', ylabel='Number of published articles', title='Published articles by year', bar_color='#864CE4')
    # fig.set_size_inches(10, 8)
    # fig.set_dpi(150)
    # fig.savefig('out/年份变化.png')
    # plt.show()
    # fig = draw_bar_with_plot_by_plotly(years_data, xlabel='Year', ylabel='Number of published articles',
    #                          title='Published articles by year', bar_color='rgba(76, 94, 228, 0.7)')

    # fig.show()
    # 新
    # years = [match_py(e) for e in records]
    # years_data = get_count_single(years)
    # years_data = SliceableDict(sort_by_key(years_data))[:]
    # fig = draw_bar_v(years_data, 'Year', 'Number of related articles published in the current year', '')
    # fig.set_size_inches(10, 8)
    # fig.set_dpi(150)
    # fig.savefig('out/年份变化.png')
    # plt.show()

    # 新
    # publisher = [match_pu(r) for r in records]
    # publisher_data = get_count_single(publisher)
    # publisher_data = SliceableDict(sort_by_value(publisher_data, True))[:]
    # draw_pie_more(publisher_data, '', )

    # subjects = get_count_mult([match_wc(e) for e in records])
    # subjects_data = SliceableDict(sort_by_value(subjects, reverse=True))[:]
    # fig = draw_word_cloud(subjects_data, None, bgc="#f5fffa", color_func=dark_blue_black_purple)
    # fig.savefig('out/c1.png')
    # plt.show()
    # #f5fffa

    # fig = draw_word_cloud(publisher_data)
    # # fig.gca().tick_params(axis='y', labelsize=8)
    # fig.set_size_inches(8, 6)
    # fig.set_dpi(200)
    # fig.savefig('out/出版商统计.png')
    # plt.show()
    # 画饼状图
    # draw_pie_more(publisher_data, 'Article attribution to publisher statistics')

    # fig = draw_bar_h(subjects_data, 'Number of records', 'Subject', '')
    # fig.gca().tick_params(axis='y', labelsize=8)
    #
    # fig.set_size_inches(12, 8)
    # fig.set_dpi(160)

    # plt.savefig('学科分类全系列词云.png', bbox_inches='tight', pad_inches=0.1)


    # 饼状图
    # a = QApplication([])
    # a.setFont(QFont('Times New Roman', 20))
    # # 画饼状图
    # w = ChartWindow(publisher_data, '', topshow=15)
    #
    # w.show()
    # a.exec()
    # out = os.path.dirname(os.path.abspath(__file__)) + r'\out'
    # journals = [match_so(e) for e in records]
    # journals_data = get_count_single(journals)
    # journals_data = sort_by_value(journals_data, reverse=True)
    # 期刊全系列词云
    # fig = draw_word_cloud_by_pyecharts(journals_data, )
    # fig.render("out/词云.html")  # ✅ 保存为交互式HTML
    # fig.savefig(f'{out}/期刊词云.png')
    # plt.show()

    # reference_with_doi = sort_by_z9_doi(records, True)
    # reference_top20_with_doi = SliceableDict(sort_by_point_value(reference_with_doi, 0))[:60]
    # gen_word_table(reference_top20_with_doi, f'{out}/table_top60_reference')

    subjects = get_count_mult([match_wc(e) for e in records])
    subjects_data = SliceableDict(sort_by_value(subjects, reverse=True))[:]

    draw_pie_more(subjects_data, ' ', 20)

