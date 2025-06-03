from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt

from ToolBar import ToolBar
from Tabs import Tabs

class IndekedStack(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.settingPage = QWidget(styleSheet='background-color:lightblue')
        self.subSplitter = QSplitter()
        self.toolbar = ToolBar()
        self.tabs = Tabs()
        self.__setUI()

    def __setUI(self) -> None:
        self.subSplitter.setOrientation(Qt.Orientation.Vertical)
        self.subSplitter.setSizes([100, 500])
        self.subSplitter.addWidget(self.toolbar)
        self.subSplitter.addWidget(self.tabs)
        self.addWidget(self.subSplitter)
        self.addWidget(self.settingPage)
        self.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication([])
    ui = IndekedStack()
    ui.show()
    app.exec()