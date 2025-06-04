import re
from typing import *
from collections import OrderedDict

from matplotlib.pyplot import ylabel
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

# 将每个记录单独写入
def write_record(fileName : str, text : str) -> None:
    with open(fileName, 'w', encoding='U8') as f:
        f.write(text)
    f.close()

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

# 文章被引用次数统计，不考虑主流引用，考虑综合引用 -> {文章名字：被引次数}
def get_cite_count(items : list[str]) -> dict[str, int]:
    rt = {}
    for item in items:
        name = re.search(r'^TI (.+)', item, flags=re.MULTILINE)
        z9_match = re.search(r'^Z9\s+(\d+)', item, flags=re.MULTILINE)
        z9 = int(z9_match.group(1)) if z9_match else 0
        rt[name.group(1).strip()] = z9
    return rt

# 自定义匹配
def self_define_pattern(entry : str, key : str):
    so = re.search(key, entry, flags=re.MULTILINE)
    return so.group(1).strip() if so else None

# 自定义统计，键必须和数量有关才行
def self_define_statistics(items : list[str], key : str):
    selves = {}
    for item in items:
        rt = self_define_pattern(item, key)
        if selves.get(rt):
            selves[rt] += 1
        else:
            selves[rt] = 1
    return selves

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
    fig.subplots_adjust(left=0, right=1, top=0.9, bottom=0)

    if title:
        ax.set_title(title)

    return fig

# 画柱状图
def draw_bar(
    data : dict,
    title : Optional[str] = '',
    figsize : Optional[tuple[int, int]] = None,
    barColor : str = '#128fab',
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
        plt.xticks(rotation=rotation)
    else:
        plt.barh(keys, values, color=barColor)
    if title:
        plt.title(title)
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.tight_layout()
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
    finished = Signal(dict)  # 线程结束后发射数据给主线程

    def __init__(self, data: dict, state: dict, prefix: str):
        super().__init__()
        self.data = data
        self.state = state
        self.prefix = prefix  # 'so' 或 'py'

    def run(self):
        len_data = len(self.data)
        spin_data = min(self.state['spin'], len_data)
        spin_data = len_data if spin_data == 0 else spin_data

        # 根据不同前缀和选择排序
        if self.prefix == 'so':
            if self.state['select'] == '从小到大':
                self.data = sort_value(self.data, reverse=False)
            elif self.state['select'] == '从大到小':
                self.data = sort_value(self.data, reverse=True)
        elif self.prefix == 'py':  # py系列
            if self.state['select'] == '从早到晚':
                self.data = sort_key(self.data, reverse=False)
            elif self.state['select'] == '从晚到早':
                self.data = sort_key(self.data, reverse=True)

        data_slice = SliceableDict(self.data)[:spin_data]

        # 线程结束后把数据和状态发给主线程，主线程来做UI操作
        self.finished.emit({
            'prefix': self.prefix,
            'data_slice': data_slice,
            'state': self.state,
            'length': len_data,
        })

def complete_task(app):
    filePath = open_file(app)
    if not filePath:
        QMessageBox.warning(
            app,
            '警告',
            '您取消了选择文件',
            QMessageBox.StandardButton.Ok
        )
        return

    # 先清屏
    app.tabs.recover()
    for i in range(app.tabs.count() - 1):
        app.tabs.removeTab(1)

    data_so, data_py = journal_statistics(load(filePath))
    states = get_state(app)
    state_so, state_py = states['so'], states['py']

    results = {}

    def on_worker_finished(result : dict):
        prefix = result['prefix']
        data_slice = result['data_slice']
        state = result['state']

        # UI操作必须在主线程
        # 输出Json
        if state['json']:
            app.tabs.addTab(JsonPage(data_slice), qtIcon('mdi.code-json'), 'Json格式')
        # 画纵向柱状图
        if state['bar']:
            app.tabs.addTab(MpWdiegt(draw_bar(
                data_slice,
                title=state['title'],
                horizontal=False,
                xlabel='Year',
                rotation=45,
                ylabel='Number of related articles published in the current year'
            )), qtIcon('fa5s.chart-bar'), 'Bar')
        # 画横向柱状图
        if state['barh']:
            app.tabs.addTab(MpWdiegt(draw_bar(
                data_slice,
                title=state['title'],
                horizontal=True,
                xlabel='Number of journals collected',
                ylabel='Journals',
            )), qtIcon('fa6.chart-bar'), 'Barh')
        # 画词云图
        if state['cloud']:
            app.tabs.addTab(MpWdiegt(draw_word_cloud(
                data_slice,
                title=state['title'],
            )), qtIcon('ei.cloud'), '词云图')

        results[prefix] = result['length']

        if 'so' in results and 'py' in results:
            app.tabs.refresh(results.get('py'), results.get('so'))
            QMessageBox.information(
                app,
                '通知',
                '导入成功',
                QMessageBox.StandardButton.Ok
            )

    if state_so['checked']:
        app.worker_so = Worker(data_so, state_so, 'so')
        app.worker_so.finished.connect(on_worker_finished)
        app.worker_so.start()
    if state_py['checked']:
        app.worker_py = Worker(data_py, state_py, 'py')
        app.worker_py.finished.connect(on_worker_finished)
        app.worker_py.start()

