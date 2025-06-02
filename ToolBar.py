from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt
from qtawesome import icon as qtIcon

class Check(QCheckBox):
    def __init__(self, text: str, **kwargs):
        super().__init__(**kwargs)
        self.setCheckState(Qt.CheckState.Checked)
        self.setText(text)

class Spin(QSpinBox):
    def __init__(self, value : int = 10):
        super().__init__()
        self.setValue(value)
        self.setRange(0, 1000)

class Combo(QComboBox):
    def __init__(self, ls):
        super().__init__()
        self.addItems(ls)

    def wheelEvent(self, e, /): pass

class TB(QToolButton):
    def __init__(self, name, icon, **kwargs):
        super().__init__(**kwargs)
        self.setText(name)
        self.setIcon(icon)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

class ToolBar(QToolBar):
    def __init__(self):
        super().__init__()

        self.check_so = Check('期刊来源')
        self.draw_bar_so = Check('画纵向柱状图')
        self.draw_barh_so = Check('画横向柱状图')
        self.draw_json_so = Check('输出Json')
        self.draw_wordcloud_so = Check('画词云图')
        self.select_so = Combo(['从大到小', '从小到大','乱序'])
        self.spin_so = Spin()

        self.check_py = Check('年份来源')
        self.draw_bar_py = Check('画纵向柱状图')
        self.draw_barh_py = Check('画横向柱状图')
        self.draw_json_py = Check('输出Json')
        self.draw_wordcloud_py = Check('画词云图')
        self.select_py = Combo(['从早到晚', '从晚到早', '乱序'])
        self.spin_py = Spin(value=0)

        self.openBtn = TB('打开', qtIcon('ei.folder-open'))
        self.helpBtn = TB('帮助', qtIcon('mdi.help-box'))

        self.line_so = QLineEdit()
        self.line_py=  QLineEdit()

        self.__setUI()
    def __setUI(self) -> None:
        vbox1 = QVBoxLayout()
        hbox11 = QHBoxLayout()
        hbox12 = QHBoxLayout()
        hbox13 = QHBoxLayout()
        hbox14 = QHBoxLayout()
        vbox1.addLayout(hbox11)
        vbox1.addLayout(hbox12)
        vbox1.addLayout(hbox13)
        vbox1.addLayout(hbox14)
        hbox11.addWidget(self.check_so)
        hbox11.addWidget(self.draw_bar_so)
        hbox12.addWidget(self.select_so)
        hbox12.addWidget(self.draw_barh_so)
        hbox13.addWidget(self.draw_json_so)
        hbox13.addWidget(self.draw_wordcloud_so)
        hbox14.addWidget(self.spin_so)
        hbox14.addWidget(QLabel('前X个'))

        vbox2 = QVBoxLayout()
        hbox21 = QHBoxLayout()
        hbox22 = QHBoxLayout()
        hbox23 = QHBoxLayout()
        hbox24 = QHBoxLayout()
        vbox2.addLayout(hbox21)
        vbox2.addLayout(hbox22)
        vbox2.addLayout(hbox23)
        vbox2.addLayout(hbox24)
        hbox21.addWidget(self.check_py)
        hbox21.addWidget(self.draw_bar_py)
        hbox22.addWidget(self.select_py)
        hbox22.addWidget(self.draw_barh_py)
        hbox23.addWidget(self.draw_json_py)
        hbox23.addWidget(self.draw_wordcloud_py)
        hbox24.addWidget(self.spin_py)
        hbox24.addWidget(QLabel('前X个'))

        hbox = QHBoxLayout()
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)
        group1 = QGroupBox()
        group1.setLayout(hbox)
        self.addWidget(group1)
        self.addSeparator()

        self.line_so.setPlaceholderText('设置期刊图名字，可以空着')
        self.line_py.setPlaceholderText('设置年份图名字，可以空着')
        self.line_so.setMinimumWidth(150)
        self.line_py.setMinimumWidth(150)
        vbox = QVBoxLayout()
        vbox.addWidget(self.line_so)
        vbox.addWidget(self.line_py)
        group2 = QGroupBox()
        group2.setLayout(vbox)
        self.addWidget(group2)
        self.addSeparator()

        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.openBtn)
        vbox3.addWidget(self.helpBtn)
        group3 = QGroupBox()
        group3.setLayout(vbox3)
        self.addWidget(group3)

if __name__ == '__main__':
    app = QApplication([])
    ui = ToolBar()
    ui.show()
    app.exec()