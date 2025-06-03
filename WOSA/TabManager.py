# TabManager是一个单例
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt
from qtawesome import icon as qtIcon

class TabManager(QTabWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.defaultpage = QLabel()

        self.__setUI()
    def __setUI(self) -> None:
        self.defaultpage.setText('''
        <p style="color : #000fff;font-size : 32px;font-weight : 900;text-align:center;">
        场景中的图片提供右键操作菜单栏。
        </p>
        ''')
        self.setAcceptDrops(True)
        self.setTabShape(QTabWidget.TabShape.Triangular)
        self.setTabsClosable(True)
        self.addTab(self.defaultpage, qtIcon('mdi.domain'), '默认')

if __name__ == '__main__':
    app = QApplication([])
    ui = TabManager()
    ui.show()
    app.exec()