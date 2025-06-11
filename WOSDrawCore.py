from typing import Optional

from matplotlib.axes import Axes
from wordcloud import WordCloud
from matplotlib.figure import Figure
from matplotlib import rcParams
import matplotlib.pyplot as plt

from WOSUtil import match_pu, SliceableDict, sort_by_value, load, get_count_single
from WOSPie import draw_pie_more

# 设置字体族，首选 'Times New Roman' (类似“新罗马”)
rcParams['font.family'] = 'Times New Roman'
# 设置中文字体优先级
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial']
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
    ax.bar(keys, values)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set(**kwargs)
    plt.tight_layout()
    return fig

# 画词云图
def draw_word_cloud(
    data : dict,
    title : Optional[str] = '',
    width=1600,
    height=1000,
    bgc : str = 'mintcream',
    **kwargs
) -> Figure:
    wordcloud : WordCloud = WordCloud(
        width=width,
        height=height,
        background_color=bgc,
        margin=0,
        prefer_horizontal=1.0
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

# 画饼状图
def draw_pie(data : dict, title : str, **kwargs) -> Figure:
    labels = list(data.keys())
    sizes = list(data.values())

    fig = plt.figure()
    ax : Axes = fig.gca()
    ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',  # 显示百分比
        startangle=90,  # 旋转起始角度
    )
    ax.set_title(title)
    ax.set(**kwargs)
    return fig

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
    records = load('savedrecs.txt')
    publisher = [match_pu(r) for r in records]
    publisher_data = get_count_single(publisher)
    publisher_data = SliceableDict(sort_by_value(publisher_data, True))[:]
    draw_pie_more(publisher_data, 'Article attribution to publisher statistics')
