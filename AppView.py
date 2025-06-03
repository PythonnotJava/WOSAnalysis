# 画图的场景容器
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt

class AppView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene(self)

        self.__setUI()
    def __setUI(self) -> None:
        self.setScene(self.scene)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.TextAntialiasing |
            QPainter.RenderHint.SmoothPixmapTransform |
            QPainter.RenderHint.LosslessImageRendering
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
    ui = AppView()
    ui.show()
    app.exec()