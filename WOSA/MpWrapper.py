import os, platform

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt

from matplotlib import use as matplotlib_use
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt

matplotlib_use('Qt5Agg')

# 桌面路径
def get_desktop_path():
    system = platform.system()
    if system == "Windows":
        return os.path.join(os.environ['USERPROFILE'], 'Desktop')
    elif system == "Darwin":  # macOS
        return os.path.join(os.path.expanduser("~"), "Desktop")
    else:  # Linux
        return os.path.join(os.path.expanduser("~"), "桌面")  # 有些Linux中文系统桌面文件夹叫“桌面”

class MpWdiegt(QWidget):
    def __init__(
        self,
         figure : Figure,
         **kwargs
     ):
        super().__init__(**kwargs)

        self.figure = figure
        self.canvas = FigureCanvasQTAgg(self.figure)  # 这是一个Widget

        self.__setUI()
    def __setUI(self) -> None:
        lay = QVBoxLayout()
        lay.addWidget(self.canvas)
        self.canvas.draw()
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(lay)

        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self, pos: QPoint):
        menu = QMenu(self)
        menu.addAction("保存图片", self.saveAs)
        menu.exec(self.mapToGlobal(pos))

    def saveAs(self):
        filePath, _ = QFileDialog.getSaveFileName(
            self,
            '选中保存路径',
            get_desktop_path(),
            "PNG 图片 (*.png);;JPEG 图片 (*.jpg *.jpeg)"
        )
        if not filePath:
            QMessageBox.warning(
                self,
                '警告',
                '您取消了选择保存操作。',
                QMessageBox.StandardButton.Ok
            )
        else:
            self.figure.savefig(filePath)

if __name__ == '__main__':
    def func():
        fig = plt.figure(figsize=(8, 6))
        plt.plot([1, 2, 3, 4], [2, 3, 4, 5])
        return fig
    app = QApplication([])
    ui = MpWdiegt(func())
    ui.show()
    app.exec()