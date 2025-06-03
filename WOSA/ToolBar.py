import pickle
from typing import *
from dataclasses import dataclass

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt
from qtawesome import icon as qtIcon

from AppTyping import *

# 专门记录每个文献的记录并且动态保存关于对于某个字段解析的内容
class RecordType:
    length : int
    items : list[str]

    def to_pickle(self, filename: str) -> None:
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def from_pickle(cls, filename: str) -> 'RecordType':
        with open(filename, 'rb') as f:
            return pickle.load(f)

# '', '', '', '', '',
#         '', '', '被引用次数', '综合被引次数', '发表年份'
WOSModels = {
    '出版类型' : ['Json格式', '横向柱状图', '纵向柱状图', '饼状图', '词云图'],
    '文献标题' : ['纯文本格式'],
    '期刊名' : ['Json格式', '横向柱状图', '纵向柱状图', '饼状图'],
    '文献类型描述' : ['Json格式', '横向柱状图', '纵向柱状图', '饼状图'],
    '作者关键词' : ['纯文本格式'],
    '摘要' : ['纯文本格式'],
    '参考文献数' : ['Json格式'],

}

# 记录类型是专门备份当前打开文件和解析到的内容
class ToolBar(QToolBar):
    def __init__(self):
        super().__init__()

        self.records : dict[str, str] = {}
        self.current_file = None
        self.current_record = None

        self.file_path_lineedit = LineEdit(150)
        self.file_path_button = TButton(text='打开', icon=qtIcon('ei.folder-open'))

        self.selectmodels = []

        self.__setUI()
    def __setUI(self) -> None:

        grid = QGridLayout()
        index = 0
        WOSModels = [
            '出版类型', '文献标题', '期刊名', '文献类型描述', '作者关键词',
            '摘要', '参考文献数', '被引用次数', '综合被引次数', '发表年份'
        ]
        for row in range(2):
            for col in range(5):
                checkBox = Check()
                self.selectmodels.append(checkBox)
                h = QHBoxLayout()
                h.addWidget(checkBox)
                h.addWidget(QLabel(WOSModels[index]))
                grid.addLayout(h, row, col, Qt.AlignmentFlag.AlignLeft)
                index += 1

        group2 = QGroupBox()
        group2.setLayout(grid)
        self.addWidget(group2)

        self.file_path_lineedit.setReadOnly(True)
        self.file_path_lineedit.setEnabled(False)
        self.file_path_lineedit.setPlaceholderText('暂无路径')
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel('当前路径：'))
        hbox1.addWidget(self.file_path_lineedit)
        hbox1.addWidget(self.file_path_button)
        group1 = QGroupBox()
        group1.setLayout(hbox1)
        self.addWidget(group1)

if __name__ == '__main__':
    app = QApplication([])
    ui = ToolBar()
    ui.show()
    app.exec()