import re
from typing import *
from collections import OrderedDict

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib import rcParams

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt
from qtawesome import icon as qtIcon

from JsonPage import JsonPage
from MpWrapper import get_desktop_path, MpWdiegt

rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False

# 可切片字典
class SliceableDict(OrderedDict):
    def __init__(self, original_dict : dict):
        super().__init__(original_dict)

    def __getitem__(self, key):
        if isinstance(key, slice):
            keys = list(self.keys())[key]
            return SliceableDict({k: self[k] for k in keys})
        else:
            return super().__getitem__(key)

def load(path : str = 'savedrecs.txt') -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    # 捕获从 PT 开头到 ER（含换行）的一整条记录
    pattern = r"(?=PT )(.*?\nER\n)"
    matches = re.findall(pattern, text, flags=re.DOTALL)

    return matches

# 匹配`SO+一个空格`字符串、`PY+一个空格`字符串
def get_journal_data(entry: str) -> tuple:
    so = re.search(r'^SO (.+)', entry, flags=re.MULTILINE)
    py = re.search(r'^PY\s+(\d{4})', entry, re.MULTILINE)
    return so.group(1).strip() if so else None, py.group(1).strip() if py else None

# 期刊以及发布年份统计，{期刊名字：数量},{年份：数量}
def journal_statistics(items : list[str]):
    sos = {}
    pys = {}
    for item in items:
        so, py = get_journal_data(item)
        if sos.get(so):
            sos[so] += 1
        else:
            sos[so] = 1
        if pys.get(py):
            pys[py] += 1
        else:
            pys[py] = 1
    return sos, pys

# 对值排序 True表示从大到小
def sort_value(data : dict, reverse : bool = True):
    sorted_data = dict(sorted(data.items(), key=lambda item: item[1], reverse=reverse))
    return sorted_data
# 对键排序
def sort_key(data : dict, reverse : bool = True):
    sorted_data = dict(sorted(data.items(), key=lambda item: int(item[0]), reverse=reverse))
    return sorted_data

# 画词云
def draw_word_cloud(
    data : dict,
    title : Optional[str] = '',
    figsize: Optional[tuple[int, int]] = None,
    width=1600,
    height=800,
    bgc : str = 'mintcream'
) -> Figure:
    wordcloud = WordCloud(
        width=width,
        height=height,
        background_color=bgc,
        margin=0,
        prefer_horizontal=1.0
    ).generate_from_frequencies(data)

    fig = plt.figure(figsize=figsize if figsize else (width / 100, height / 100), dpi=100)
    ax = fig.add_subplot(111)
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_axis_off()
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    if title:
        ax.set_title(title)

    return fig

# 画柱状图
def draw_bar(
    data : dict,
    title : Optional[str] = '',
    figsize : Optional[tuple[int, int]] = None,
    barColor : str = 'skyblue',
    horizontal : bool = True,
    xlabel : str = '',
    ylabel : str = '',
    rotation=90
) -> Figure:
    keys = list(data.keys())
    values = list(data.values())
    fig = plt.figure() if not figsize else plt.figure(figsize=figsize)
    if not horizontal:
        plt.bar(keys, values, color=barColor)
    else:
        plt.barh(keys, values, color=barColor)
    if title:
        plt.title(title)
    plt.xticks(rotation=rotation)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
    return fig

# from AppCore import AppCore

# 是否打开文件
def open_file(app) -> Optional[str]:
    filePath, _ = QFileDialog.getOpenFileName(
        app,
        caption='选择记录文件',
        dir=get_desktop_path(),
        filter="Text Files (*.txt)"
    )
    return filePath
# 状态
def get_state(app):
    tool = app.toolbar
    return {
        'so' : {
            'checked' : tool.check_so.isChecked(),
            'select' : tool.select_so.currentText(),
            'json' : tool.draw_json_so.isChecked(),
            'spin' : tool.spin_so.value(),
            'bar' : tool.draw_bar_so.isChecked(),
            'barh': tool.draw_barh_so.isChecked(),
            'cloud' : tool.draw_wordcloud_so.isChecked(),
            'title' : tool.line_so.text()
        },
        'py': {
            'checked': tool.check_py.isChecked(),
            'select': tool.select_py.currentText(),
            'json': tool.draw_json_py.isChecked(),
            'spin': tool.spin_py.value(),
            'bar': tool.draw_bar_py.isChecked(),
            'barh': tool.draw_barh_py.isChecked(),
            'cloud': tool.draw_wordcloud_py.isChecked(),
            'title': tool.line_py.text()
        }
    }

class Worker(QThread):
    finished = Signal(object)

    def __init__(self, data : dict, state : dict, prefix):
        super().__init__()
        self.data = data
        self.state = state
        self.prefix = prefix  # so 或 py，用于区分

    def run(self):
        result = None
        if self.state['checked']:
            length = len(self.data)
            spin = min(self.state['spin'], length)
            spin = length if spin == 0 else spin
            if self.prefix == 'so':
                if self.state['select'] == '从小到大':
                    self.data = sort_value(self.data, reverse=False)
                elif self.state['select'] == '从大到小':
                    self.data = sort_value(self.data, reverse=True)
            else:  # py系列
                if self.state['select'] == '从早到晚':
                    self.data = sort_key(self.data, reverse=False)
                elif self.state['select'] == '从晚到早':
                    self.data = sort_key(self.data, reverse=True)

            data_slice = SliceableDict(self.data)[:spin]
            result = {
                'data_slice': data_slice,
                'state': self.state,
                'prefix': self.prefix,
                'length': length,
            }
        self.finished.emit(result)


def complete_task(app):
    filePath = open_file(app)
    if not filePath:
        QMessageBox.warning(
            app,
            '警告',
            '您取消了选择文件',
            QMessageBox.StandardButton.Ok
        )
    else:
        # 先清屏
        app.tabs.recover()
        for i in range(app.tabs.count() - 1):
            app.tabs.removeTab(1)
        # 继续
        data_so, data_py = journal_statistics(load(filePath))
        states = get_state(app)
        state_so, state_py = states['so'], states['py']
        so1, py1 = None, None
        # so系列
        if state_so['checked']:
            len_so = len(data_so)
            so1 = len_so
            spin_so = min(state_so['spin'], len_so)
            spin_so = len_so if spin_so == 0 else spin_so
            if state_so['select'] == '从小到大':
                data_so = sort_value(data_so, reverse=False)
            elif state_so['select'] == '从大到小':
                data_so = sort_value(data_so, reverse=True)
            else:
                pass
            data_slice_so = SliceableDict(data_so)[:spin_so]
            # 输出Json
            if state_so['json']:
                app.tabs.addTab(JsonPage(data_slice_so), qtIcon('mdi.code-json'), 'Json格式')
            # 画纵向柱状图
            if state_so['bar']:
                app.tabs.addTab(MpWdiegt(draw_bar(
                    data_slice_so,
                    title=state_so['title'],
                    horizontal=False
                )), qtIcon('fa5s.chart-bar'), 'Bar')
            # 画横向柱状图
            if state_so['barh']:
                app.tabs.addTab(MpWdiegt(draw_bar(
                    data_slice_so,
                    title=state_so['title'],
                    horizontal=True
                )), qtIcon('fa6.chart-bar'), 'Barh')
            # 画云图
            if state_so['cloud']:
                app.tabs.addTab(MpWdiegt(draw_word_cloud(
                    data_slice_so,
                    title=state_so['title'],
                )), qtIcon('ei.cloud'), '词云图')
        # py系列
        if state_py['checked']:
            len_py = len(data_py)
            py1 = len_py
            spin_py = min(state_py['spin'], len_py)
            spin_py = len_py if spin_py == 0 else spin_py
            if state_py['select'] == '从早到晚':
                data_py = sort_key(data_py, reverse=False)
            elif state_py['select'] == '从晚到早':
                data_py = sort_key(data_py, reverse=True)
            else:
                pass
            data_slice_py = SliceableDict(data_py)[:spin_py]
            # 输出Json
            if state_py['json']:
                app.tabs.addTab(JsonPage(data_slice_py), qtIcon('mdi.code-json'), 'Json格式')
            # 画纵向柱状图
            if state_py['bar']:
                app.tabs.addTab(MpWdiegt(draw_bar(
                    data_slice_py,
                    title=state_py['title'],
                    horizontal=False
                )), qtIcon('fa5s.chart-bar'), 'Bar')
            # 画横向柱状图
            if state_py['barh']:
                app.tabs.addTab(MpWdiegt(draw_bar(
                    data_slice_py,
                    title=state_py['title'],
                    horizontal=True
                )), qtIcon('fa6.chart-bar'), 'Barh')
            # 画云图
            if state_py['cloud']:
                app.tabs.addTab(MpWdiegt(draw_word_cloud(
                    data_slice_py,
                    title=state_py['title'],
                )), qtIcon('ei.cloud'), '词云图')
        app.tabs.refresh(py1, so1)
        QMessageBox.information(
            app,
            '通知',
            '导入成功',
            QMessageBox.StandardButton.Ok
        )

