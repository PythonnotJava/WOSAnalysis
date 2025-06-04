from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt
from qtawesome import icon as qtIcon

from ToolBar import ToolBar
from TabScene import TabScene

class AppView(QSplitter):
    def __init__(self):
        super().__init__()

        self.toolbar = ToolBar()
        self.tabscene = TabScene()

        self.__setUI()
    def __setUI(self) -> None:
        self.addWidget(self.toolbar)
        self.addWidget(self.tabscene)

        self.setOrientation(Qt.Orientation.Vertical)
        self.setSizes([150, 650])

if __name__ == '__main__':
    app = QApplication([])
    ui = AppView()
    ui.show()
    app.exec()