import sys
from PyQt5.QtWidgets import (
    QApplication, QGraphicsView, QGraphicsScene,
    QGraphicsPixmapItem, QWidget, QVBoxLayout,
    QPushButton, QComboBox
)
from PyQt5.QtGui import QImage, QPixmap
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

class MplScene(QWidget):
    def __init__(self):
        super().__init__()

        # 初始化场景和视图
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)

        # 创建 matplotlib 图形
        self.fig = Figure(figsize=(4, 3))
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.plot([0, 1, 2], [1, 4, 9])

        # 绘制并显示到 QGraphicsScene
        self.image_item = QGraphicsPixmapItem()
        self.scene.addItem(self.image_item)
        self.update_scene()

        # UI 控件
        self.bg_selector = QComboBox()
        self.bg_selector.addItems(["white", "lightgray", "black"])
        self.bg_selector.currentTextChanged.connect(self.change_bg)

        self.rotate_button = QPushButton("旋转标签角度")
        self.rotate_button.clicked.connect(self.rotate_labels)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.bg_selector)
        layout.addWidget(self.rotate_button)
        self.setLayout(layout)

    def update_scene(self):
        """重新渲染图形并显示到 QGraphicsScene"""
        self.canvas.draw()
        w, h = self.canvas.get_width_height()
        buf = np.frombuffer(self.canvas.buffer_rgba(), dtype=np.uint8).reshape(h, w, 4)
        image = QImage(buf.data, w, h, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(image)
        self.image_item.setPixmap(pixmap)

    def change_bg(self, color):
        """修改背景颜色"""
        self.fig.patch.set_facecolor(color)
        self.ax.set_facecolor(color)
        self.update_scene()

    def rotate_labels(self):
        """旋转 X 轴标签角度"""
        for label in self.ax.get_xticklabels():
            label.set_rotation(45)
        self.update_scene()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MplScene()
    window.setWindowTitle("动态调试 Matplotlib in QGraphicsScene")
    window.resize(500, 400)
    window.show()
    sys.exit(app.exec_())
