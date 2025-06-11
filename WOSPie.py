from PySide6.QtWidgets import *
from PySide6.QtCharts import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from qtawesome import icon as qtIcon

from command.WOSUtil import get_desktop_path

class ChartWindow(QMainWindow):
    # topshow表示显示几个为真正的名字，剩下的打包到其他
    def __init__(self, data : dict, title : str, topshow : int = 9):
        super().__init__()
        self.setWindowTitle("Discipline Distribution Pie Chart")
        self.resize(1600, 1200)

        total = sum(data.values())
        series = QPieSeries()

        # 保证按数量从大到小排序（如果传入没排好）
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        topshow = min(topshow, len(sorted_data))
        top_items = sorted_data[:topshow]
        other_items = sorted_data[topshow:]
        others_total = sum(value for _, value in other_items)

        # 添加前top个类别
        for label, value in top_items:
            percent = (value / total) * 100
            display_label = f"{percent:.1f}%"
            legend_label = f"{label if label else 'Others'} ({value})"

            slice_ = series.append(display_label, value)
            slice_.setLabelVisible(True)
            slice_.setProperty("legendLabel", legend_label)

        # 添加“其他”
        if others_total > 0:
            percent = (others_total / total) * 100
            display_label = f"{percent:.1f}%"
            legend_label = f"Others ({others_total})"

            slice_ = series.append(display_label, others_total)
            slice_.setLabelVisible(True)
            slice_.setProperty("legendLabel", legend_label)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(title)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignRight)

        for marker in chart.legend().markers(series):
            legend_label = marker.slice().property("legendLabel")
            if legend_label:
                marker.setLabel(legend_label)

        chart_view = QChartView(chart)
        chart_view.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.TextAntialiasing |
            QPainter.RenderHint.SmoothPixmapTransform
        )

        layout = QVBoxLayout()
        layout.addWidget(chart_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.chartview = chart_view
        self.chart = chart

    def contextMenuEvent(self, event : QContextMenuEvent):
        menu = QMenu()
        submenu = QMenu('设置主题')

        for i, (theme, name) in {
            0: (QChart.ChartTheme.ChartThemeLight, "Light"),
            1: (QChart.ChartTheme.ChartThemeBlueCerulean, "Blue Cerulean"),
            2: (QChart.ChartTheme.ChartThemeDark, "Dark"),
            3: (QChart.ChartTheme.ChartThemeBrownSand, "Brown Sand"),
            4: (QChart.ChartTheme.ChartThemeBlueNcs, "Blue NCS"),
            5: (QChart.ChartTheme.ChartThemeHighContrast, "High Contrast"),
            6: (QChart.ChartTheme.ChartThemeBlueIcy, "Blue Icy"),
            7: (QChart.ChartTheme.ChartThemeQt, "Qt Default"),
        }.items():
            act = QAction(name, self)
            act.triggered.connect(lambda _, t=theme: self.chart.setTheme(t))
            submenu.addAction(act)

        save_img = QAction(qtIcon('fa5.save'), '保存图片')
        menu.addActions([save_img])
        menu.addMenu(submenu)
        save_img.triggered.connect(self._save)
        global_pos = event.globalPos()
        menu.exec(global_pos)

    def _save(self):
        filePath, _ = QFileDialog.getSaveFileName(
            self,
            '选择保存路径',
            get_desktop_path(),
            filter="PNG Files (*.png);;JPG Files (*.jpg);;JPEG Files (*.jpeg)"
        )
        if not filePath:
            QMessageBox.warning(self, '警告', '取消保存！', QMessageBox.StandardButton.Ok)
        else:
            p = self.chartview.grab()
            p.save(filePath)

def draw_pie_more(data : dict, title : str, topshow : int = 9):
    app = QApplication([])
    app.setApplicationName('右键可以操作')
    app.setFont(QFont('Times New Roman'))
    window = ChartWindow(data, title, topshow)
    window.show()
    app.exec()
