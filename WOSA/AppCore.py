from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt

from SideBar import SideBar
from IndexdStack import IndekedStack

from core import complete_task

class AppCore(QMainWindow):
    def __init__(self):
        super().__init__()

        self.sidebar = SideBar()
        self.mainSplitter = QSplitter()
        self.stack = IndekedStack()

        self.tabs = self.stack.tabs
        self.toolbar = self.stack.toolbar

        self.__setUI()

    def __setUI(self) -> None:
        self.mainSplitter.addWidget(self.sidebar)
        self.mainSplitter.addWidget(self.stack)
        self.mainSplitter.setOrientation(Qt.Orientation.Horizontal)
        self.mainSplitter.setSizes([100, 700])

        self.setCentralWidget(self.mainSplitter)
        self.setStatusBar(QStatusBar())
        self.setMinimumSize(1000, 800)

        # 链接打开
        self.toolbar.openBtn.clicked.connect(lambda: complete_task(self))

if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon('src/logo.ico'))
    app.setApplicationName('WOS文献计量可视化')
    ui = AppCore()
    ui.show()
    app.exec()