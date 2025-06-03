import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

from PySide6.QtWidgets import (
    QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
)
from PySide6.QtGui import (
    QImage, QPixmap, QPainter, QPen, QWheelEvent
)
from PySide6.QtCore import Qt, QRectF


class MapView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.zoom_level = 1.0
        self.zoom_min = 0.2
        self.zoom_max = 5.0

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setUI()

    def setUI(self) -> None:
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.TextAntialiasing |
            QPainter.RenderHint.SmoothPixmapTransform
        )
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        grid_size = 50
        pen = QPen(Qt.GlobalColor.lightGray)
        pen.setWidth(1)
        painter.setPen(pen)

        left = int(rect.left()) - (int(rect.left()) % grid_size)
        top = int(rect.top()) - (int(rect.top()) % grid_size)
        right = int(rect.right())
        bottom = int(rect.bottom())

        for x in range(left, right, grid_size):
            painter.drawLine(x, top, x, bottom)

        for y in range(top, bottom, grid_size):
            painter.drawLine(left, y, right, y)

    def wheelEvent(self, event: QWheelEvent):
        zoom_factor = 1.2
        if event.angleDelta().y() > 0:
            if self.zoom_level < self.zoom_max:
                self.scale(zoom_factor, zoom_factor)
                self.zoom_level *= zoom_factor
        else:
            if self.zoom_level > self.zoom_min:
                self.scale(1 / zoom_factor, 1 / zoom_factor)
                self.zoom_level /= zoom_factor

    def add_matplotlib_plot(self, pos=(0, 0)):
        # 1. 生成 Matplotlib 图
        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        x = np.linspace(0, 2 * np.pi, 100)
        ax.plot(x, np.sin(x))
        ax.set_title("Sine Curve")
        canvas = FigureCanvasAgg(fig)
        canvas.draw()

        # 2. 转为 QPixmap
        width, height = fig.get_size_inches() * fig.get_dpi()  # figsize * dpi
        buf = canvas.buffer_rgba()
        img = QImage(buf, int(width), int(height), QImage.Format.Format_RGBA8888)
        img = img.copy()  # 拷贝防止 buffer 生命周期问题
        pixmap = QPixmap.fromImage(img)

        # 3. 加入图形项
        item = QGraphicsPixmapItem(pixmap)
        item.setPos(*pos)
        item.setFlags(
            QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsPixmapItem.GraphicsItemFlag.ItemIsSelectable
        )
        self.scene.addItem(item)

        plt.close(fig)  # 关闭 matplotlib 窗口资源


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = MapView()
    view.resize(1000, 800)
    view.setWindowTitle("Matplotlib 图嵌入 QGraphicsView 并支持拖动")
    view.show()

    # 添加图像
    view.add_matplotlib_plot(pos=(0, 0))
    view.add_matplotlib_plot(pos=(600, 300))  # 添加第二个图也可拖动

    sys.exit(app.exec())
