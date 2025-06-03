# 画图的场景容器
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt

def draw_a_bar() -> Figure:
    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
    ax.bar(['A%d' % d for d in range(1, 6)], [4, 2, 8, 5, 3])
    ax.set_title("Bar Test")
    return fig

class TabScene(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.defaultfig = draw_a_bar()

        self.__setUI()
    def __setUI(self) -> None:
        self.setMinimumWidth(600)
        self.setScene(self.scene)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.TextAntialiasing |
            QPainter.RenderHint.SmoothPixmapTransform |
            QPainter.RenderHint.LosslessImageRendering
        )
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.transToGraphic(self.defaultfig)

    def transToGraphic(self, fig : Figure):
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        width, height = fig.get_size_inches() * fig.get_dpi()  # figsize * dpi
        buf = canvas.buffer_rgba()
        img = QImage(buf, int(width), int(height), QImage.Format.Format_RGBA8888)
        img = img.copy()
        pixmap = QPixmap.fromImage(img)
        item = QGraphicsPixmapItem(pixmap)
        item.setPos(0, 0)
        item.setFlags(
            QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsPixmapItem.GraphicsItemFlag.ItemIsSelectable
        )
        self.scene.addItem(item)

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
        super().drawBackground(painter, rect)

    def wheelEvent(self, event: QWheelEvent):
        zoom_factor = 1.2
        zoom_level = 1.0
        zoom_min = 0.2
        zoom_max = 5.0
        if event.angleDelta().y() > 0:
            if zoom_level < zoom_max:
                self.scale(zoom_factor, zoom_factor)
                zoom_level *= zoom_factor
        else:
            if zoom_level > zoom_min:
                self.scale(1 / zoom_factor, 1 / zoom_factor)
                zoom_level /= zoom_factor
        super().wheelEvent(event)


if __name__ == '__main__':
    app = QApplication([])
    ui = TabScene()
    ui.show()
    app.exec()