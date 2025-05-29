from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt
from qtawesome import icon as qtIcon

class SideBar(QWidget):
    def __init__(self):
        super().__init__()

        self.homepage = QToolButton()
        self.setting = QToolButton()

        self.__setUI()

    def __setUI(self) -> None:
        lay = QVBoxLayout()
        lay.addWidget(self.homepage)
        lay.addWidget(self.setting)
        lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(lay)

        self.homepage.setText('主页')
        self.setting.setText('设置')
        self.setting.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.homepage.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.homepage.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.setting.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.homepage.setIcon(qtIcon('fa5s.home'))
        self.setting.setIcon(qtIcon('mdi.cookie-settings-outline'))

if __name__ == '__main__':
    app = QApplication([])
    ui = SideBar()
    ui.show()
    app.exec()