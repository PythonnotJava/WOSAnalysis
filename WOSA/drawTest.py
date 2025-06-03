# 每个Tab由一个左侧的PlotBar和一个右侧的TabScene组成
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt
from qtawesome import icon as qtIcon

from TabScene import TabScene
from PlotBar import PlotBar

class Tab(QSplitter):
    def __init__(self):
        super().__init__()

        self.plotbar = PlotBar()
        self.tabscene = TabScene()
        self.__setUI()

    def __setUI(self) -> None:
        self.setSizes([300, 600])
        self.addWidget(self.plotbar)
        self.addWidget(self.tabscene)
        self.setAcceptDrops(True)



if __name__ == '__main__':
    app = QApplication([])
    ui = Tab()
    ui.show()
    app.exec()

