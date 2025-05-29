from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt
from qtawesome import icon as qtIcon

class Tabs(QTabWidget):
    def __init__(self):
        super().__init__()

        self.defaultpage = QLabel()

        self.__setUI()

    def __setUI(self) -> None:
        self.setAcceptDrops(True)
        self.setTabsClosable(False)
        self.setTabShape(QTabWidget.TabShape.Triangular)

        self.defaultpage.setText('''
        <p style="color : #000fff;font-size : 32px;font-weight : 900;text-align:center;">
            右键图片可以选择保存。
        </p>
        ''')

        # def addTab(self, widget: PySide6.QtWidgets.QWidget, icon: PySide6.QtGui.QIcon | PySide6.QtGui.QPixmap, label: str, /) -> int: ...
        self.addTab(self.defaultpage, qtIcon('mdi6.cursor-default-gesture-outline'), '默认界面')

    def refresh(self, py, so) -> None:
        if py and so:
            self.defaultpage.setText('''
            <p style="color : #000fff;font-size : 32px;font-weight : 900;text-align:center;">
                右键图片可以选择保存。<br>
                来源期刊类别个数：%d; <br>
                发表年份类别个数：%d; <br>
            </p>
            ''' % (so, py))
        elif py and not so:
            self.defaultpage.setText('''
            <p style="color : #000fff;font-size : 32px;font-weight : 900;text-align:center;">
                右键图片可以选择保存。<br>
                来源期刊类别个数：未考虑; <br>
                发表年份类别个数：%d; <br>
            </p>
            ''' % py)
        elif not py and so:
            self.defaultpage.setText('''
            <p style="color : #000fff;font-size : 32px;font-weight : 900;text-align:center;">
                右键图片可以选择保存。<br>
                来源期刊类别个数：%d; <br>
                发表年份类别个数：未考虑; <br>
            </p>
           ''' % so)
        else:
            pass

    def recover(self) -> None:
        self.defaultpage.setText('''
        <p style="color : #000fff;font-size : 32px;font-weight : 900;text-align:center;">
            右键图片可以选择保存。
        </p>
        ''')



if __name__ == '__main__':
    app = QApplication([])
    ui = Tabs()
    ui.show()
    app.exec()