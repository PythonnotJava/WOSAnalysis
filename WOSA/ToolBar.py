import pickle
from typing import *
from dataclasses import dataclass

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt
from qtawesome import icon as qtIcon

from AppTyping import *
from WOSUtil import *

# 专门记录每个文献的记录并且动态保存关于对于某个字段解析的内容
@dataclass
class RecordType:
    length : int
    items : list[str]
    filePath : str

    def to_pickle(self, filename: str) -> None:
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def from_pickle(cls, filename: str) -> 'RecordType':
        with open(filename, 'rb') as f:
            return pickle.load(f)

# 记录类型是专门备份当前打开文件和解析到的内容
class ToolBar(QWidget):
    def __init__(self):
        super().__init__()

        self.records : dict[str, str] = {}
        self.return_record_type : Optional[RecordType] = None
        self.index = 0

        self.open_file_edit = LineEdit(200, '暂无路径', False)
        self.open_file_button = TButton('打开', qtIcon('ei.folder-open'))

        # 长度不为1的都支持：从小到大、从大到小、乱序三种模式，不共享操作

        self.common_models_mixin = [
            RowWidgetByWidget(Check(), QLabel('Json格式')),
            RowWidgetByWidget(Check(), QLabel('横向柱状图')),
            RowWidgetByWidget(Check(), QLabel('纵向柱状图')),
            RowWidgetByWidget(Check(), QLabel('饼状图')),
            RowWidgetByWidget(Check(), QLabel('词云图'))
        ]

        self.common_models_text = [RowWidgetByWidget(Check(abled=False), QLabel('纯文本格式'))]
        self.common_models_json = [RowWidgetByWidget(Check(abled=False), QLabel('Json格式'))]

        self.WOSModels = {
            '综合被引次数': self.common_models_mixin,
            '出版类型': self.common_models_mixin,
            '文献标题': self.common_models_text,
            '期刊名': self.common_models_mixin,
            '文献类型描述': self.common_models_mixin,
            '作者关键词': self.common_models_text,
            '摘要': self.common_models_text,
            '参考文献数': self.common_models_json,
            '被引用次数': self.common_models_mixin,
            '发表年份': self.common_models_mixin
        }
        self.selcetmodels = SelectBox(0, list(self.WOSModels.keys()))
        self.change_row2_inner = QHBoxLayout()
        self.selectmethods = SelectBox(0, ['按数量从大到小', '按数量从小到大', '乱序', '按年份从早到晚', '按年份从早到晚', '按年份从晚到早'])
        self.selectnumbers = Spin(0, 0, 10000, 1, 1)
        self.selectok = TButton('分析', qtIcon('ei.ok-sign'))
        self.__current_model = '综合被引次数'

        self.help_button = TButton('帮助', qtIcon('mdi.help-circle'))
        self.insert_code_button = TButton('注入', qtIcon('msc.insert'))
        self.cfg_style_button = TButton('样式', qtIcon('fa5s.border-style'))

        self.__setUI()
        self.__link()

    def __setUI(self) -> None:
        row = QHBoxLayout()
        column = QVBoxLayout()
        grid = QGridLayout()


        # 这一步只把记录读取进来然后处理为每个文献每个记录
        row1 = QHBoxLayout()
        row1.addWidget(QLabel('当前路径'))
        row1.addWidget(self.open_file_edit)
        row1.addWidget(self.open_file_button)
        column.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel('匹配模式'))
        row2.addWidget(self.selcetmodels)
        for widget in self.WOSModels[self.__current_model]:
            self.change_row2_inner.addWidget(widget)
        row2.addLayout(self.change_row2_inner)
        row2.addWidget(self.selectmethods)
        row2.addWidget(self.selectnumbers)
        row2.addWidget(QLabel('选择前X个'))
        row2.addWidget(self.selectok)

        column.addLayout(row1)
        column.addLayout(row2)

        grid.addWidget(self.help_button, 0, 0)
        grid.addWidget(self.insert_code_button, 0, 1)
        grid.addWidget(self.cfg_style_button, 1, 0)
        group = QGroupBox()
        group.setLayout(grid)

        row.addLayout(column)
        row.addWidget(group)

        self.setLayout(row)

    def __link(self) -> None:
        self.open_file_button.clicked.connect(self.open_file_button_func)
        self.selcetmodels.currentTextChanged.connect(self.selcetmodels_changed)

    def open_file_button_func(self):
        filePath, _ = QFileDialog.getOpenFileName(self, '选择记录文件', get_desktop_path(), "Text Files (*.txt)")
        if not filePath:
            QMessageBox.warning(self, '警告', '您放弃了选择', QMessageBox.StandardButton.Ok)
        else:
            # 如果有这个文件，就导入
            record_file_path = self.records.get(filePath)
            if record_file_path:
                self.return_record_type = RecordType.from_pickle(record_file_path)
            # 如果没有
            # 如果能读到记录，先把上一个记录保存（如果有），然后创建新纪录
            # 如果读不到，这次读取就报废，仍然保持上一个记录
            else:
                _c_s : list[str] = load(filePath)
                # 读不到
                if not _c_s:
                    QMessageBox.warning(self, '警告', '格式错误，无法读取！', QMessageBox.StandardButton.Ok)
                    return
                # 读到了
                if self.return_record_type:
                    self.return_record_type.to_pickle(self.records[filePath])
                self.open_file_edit.setText(filePath)
                self.records[filePath] = f'records/{self.index}.bin'
                self.return_record_type = RecordType(len(_c_s), _c_s, filePath)

    def selcetmodels_changed(self, text : str) -> None:
        if text == self.__current_model:
            return
        else:
            if self.WOSModels[self.__current_model] != self.WOSModels[text]:
                # 先把上次的隐藏
                for widget in self.WOSModels[self.__current_model]:
                    self.change_row2_inner.removeWidget(widget)
                    widget.setHidden(True)
                # 更新当前操作模型
                self.__current_model = text
                for widget in self.WOSModels[text]:
                    self.change_row2_inner.addWidget(widget)
                    widget.setHidden(False)

if __name__ == '__main__':
    app = QApplication([])
    ui = ToolBar()
    ui.show()
    app.exec()