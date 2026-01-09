import sys, os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from matplotlib import rcParams, pyplot as plt

from WOSDrawCore import *
from WOSPie import *
from WOSUtil import *

rcParams['font.family'] = 'Times New Roman'
plt.rcParams['axes.labelsize'] = 18  # 轴标签字体大小
plt.rcParams['xtick.labelsize'] = 14  # x轴刻度字体大小
plt.rcParams['ytick.labelsize'] = 12  # y轴刻度字体大小

figsize = (20, 12)
dpi = 300

out = os.path.dirname(os.path.abspath(__file__)) + r'\out'

def example_run():
    app = QApplication([])
    app.setApplicationName('右键可以操作')
    app.setFont(QFont('Times New Roman'))

    records = load('src/1.9.txt')
    # 年份统计
    years = [match_py(e) for e in records]
    years_data = get_count_single(years)
    years_data = SliceableDict(sort_by_key(years_data))[:]
    # 纵向柱状图
    fig = draw_bar_v(years_data, 'Year', 'Number of published articles', 'Published articles by year')
    fig.set_size_inches(*figsize)
    fig.set_dpi(dpi)
    fig.savefig(f'{out}/年份变化_v.png')
    plt.show()
    # 横向柱状图
    fig = draw_bar_h(years_data, 'Number of published articles', 'Year', 'Published articles by year')
    fig.set_size_inches(*figsize)
    fig.set_dpi(dpi)
    fig.gca().tick_params(axis='y', labelsize=8)
    fig.savefig(f'{out}/年份变化_h.png')
    plt.show()

    # 期刊收集统计
    journals = [match_so(e) for e in records]
    journals_data = get_count_single(journals)
    journals_data = sort_by_value(journals_data, reverse=True)
    # 期刊全系列词云
    draw_word_cloud(journals_data, None)
    fig.savefig(f'{out}/期刊词云.png')
    plt.show()
    # 期刊前20，考虑到期刊名字较长，图会偏移，需要适当调整，只能横向，纵向太太太丑了
    journals_data_top20 = SliceableDict(journals_data)[:20]
    fig = draw_bar_h(journals_data_top20, 'Journal collection', 'Journal', 'Top 20 journals indexed')
    fig.set_size_inches(*figsize)
    fig.set_dpi(dpi)
    plt.title(fig.gca().get_title(), x=-.25)
    plt.subplots_adjust(left=0.6)
    fig.gca().tick_params(axis='y', labelsize=8)
    fig.savefig(f'{out}/期刊前20.png')
    plt.show()

    # 引用前20名的表格，带DOI和引用数
    reference = sort_by_z9(records)
    reference_with_doi = sort_by_z9_doi(records, True)
    reference_top20_with_doi = SliceableDict(sort_by_point_value(reference_with_doi, 0))[:40]
    gen_word_table(reference_top20_with_doi, f'{out}/table_top40_reference')

    # 学科分类
    # 这个也只能画横向柱状图
    subjects = get_count_mult([match_wc(e) for e in records])
    subjects_data = SliceableDict(sort_by_value(subjects, reverse=True))[:]
    fig = draw_bar_h(subjects_data, 'Number of records', 'Subject', 'Statistics by discipline')
    fig.gca().tick_params(axis='y', labelsize=8)
    fig.set_size_inches(*figsize)
    fig.set_dpi(dpi)
    fig.savefig(f'{out}/学科分类_h.png')
    plt.show()
    # 学科分类全系列词云
    draw_word_cloud(subjects_data, None)
    fig.savefig(f'{out}/学科分类全系列词云.png')
    plt.show()
    # 饼状图
    w = ChartWindow(subjects_data, 'Statistics by discipline', 20)
    w.show()

    # 研究领域
    # 这个也只能画横向柱状图
    researchArea = []
    for e in records:
        k = match_sc(e)
        if k:
            researchArea.append(match_sc(e))
    researchArea_data = get_count_mult(researchArea)
    researchArea_data = SliceableDict(sort_by_value(researchArea_data, reverse=True))[:]
    fig = draw_bar_h(researchArea_data, 'Quantity', 'Field for research', 'Research field statistics')
    fig.set_size_inches(*figsize)
    fig.set_dpi(dpi)
    fig.gca().tick_params(axis='y', labelsize=8)
    fig.savefig(f'{out}/研究领域_h.png')
    plt.show()
    # 研究领域全系列词云
    draw_word_cloud(researchArea_data, None)
    fig.savefig(f'{out}/研究领域全系列词云.png')
    plt.show()
    # 画饼状图
    w = ChartWindow(researchArea_data, 'Research field statistics', 12)
    w.show()

    # 出版商
    # 这个也只能画横向柱状图
    publisher = [match_pu(r) for r in records]
    publisher_data = get_count_single(publisher)
    publisher_data = SliceableDict(sort_by_value(publisher_data, True))[:]
    fig = draw_bar_h(publisher_data, 'Quantity', 'Name', 'Article attribution to publisher statistics')
    fig.gca().tick_params(axis='y', labelsize=8)
    fig.set_size_inches(*figsize)
    fig.set_dpi(dpi)
    fig.gca().tick_params(axis='y', labelsize=8)
    fig.savefig(f'{out}/出版商统计_h.png')
    plt.show()
    # 出版商全系列词云
    draw_word_cloud(researchArea_data, None)
    fig.savefig(f'{out}/出版商全系列词云.png')
    plt.show()
    # 画饼状图
    w = ChartWindow(publisher_data, 'Article attribution to publisher statistics')
    w.show()

    app.exec()

# if __name__ == '__main__':
#     records = load(r'src/main.txt')
#     publisher = [match_pu(r) for r in records]
#     publisher_data = get_count_single(publisher)
#     publisher_data = SliceableDict(sort_by_value(publisher_data, True))[:]
#     a = QApplication([])
#     a.setFont(QFont('Times New Roman', 24))
#     # 画饼状图
#     w = ChartWindow(publisher_data, '', topshow=9)
#
#     w.show()
#     a.exec()

if __name__ == '__main__':
    example_run()