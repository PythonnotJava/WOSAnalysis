from typing import *
from dataclasses import dataclass
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt

class SplitterLine(QFrame):
    def __init__(self, horizontal : bool = True, width : int = 2):
        super().__init__()

        if horizontal:
            self.setFrameShape(QFrame.Shape.HLine)
        else:
            self.setFrameShape(QFrame.Shape.VLine)

        self.setFrameShadow(QFrame.Shadow.Sunken)
        self.setLineWidth(width)

class Check(QCheckBox):
    def __init__(self, s : Qt.CheckState = Qt.CheckState.Checked, **kwargs):
        super().__init__(**kwargs)
        self.setCheckState(s)

class Spin(QSpinBox):
    def __init__(self, value : int = 0, range_from : int = 0, range_to : int = 180, step : int = 1):
        super().__init__()

        self.setRange(range_from, range_to)
        self.setSingleStep(step)
        self.setValue(value)

class TButton(QToolButton):
    def __init__(self, text : Optional[str] = None, icon : Optional[QIcon] = None, **kwargs):
        super().__init__(**kwargs)

        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        if icon:
            self.setIcon(icon)
        if text:
            self.setText(text)

class FontDataTButton(TButton):
    def __init__(self, font : QFont, **kwargs):
        super().__init__(**kwargs)

        self.fontData = font

class ColorDataTButton(TButton):
    def __init__(self, color : str, **kwargs):
        super().__init__(**kwargs)

        self.color = color

class SelectBox(QComboBox):
    def __init__(self, defalutIndex, l : list[str]):
        super().__init__()
        self.addItems(l)
        self.setCurrentIndex(defalutIndex)

    def wheelEvent(self, e, /):
        pass

SelectBox_style_grid = {
    0 : '直线',
    1 : '点划线'
}

@dataclass
class DefaultPlotSetting:
    # title
    ctrl_title : Qt.CheckState
    color_title : str
    font_title : QFont
    padding_title : int
    # x
    ctrl_x_axis : Qt.CheckState
    show_x_ticks : Qt.CheckState
    rotation_x_ticks : int
    color_x_ticks : str
    font_x_ticks : QFont
    padding_x_ticks : int
    show_x_label: Qt.CheckState
    rotation_x_label: int
    color_x_label: str
    font_x_label: QFont
    padding_x_label: int
    # y
    ctrl_y_axis: Qt.CheckState
    show_y_ticks: Qt.CheckState
    rotation_y_ticks: int
    color_y_ticks: str
    font_y_ticks: QFont
    padding_y_ticks: int
    # fig
    width_fig : int
    height_fig : int
    dpi_fig : int
    bgcolor_fig : str
    # grid
    show_grid : Qt.CheckState
    color_grid : str
    style_grid : int
    linew_grid : int

class PlotBar(QScrollArea):
    # 放到类属性中，做统一同步

    defaultPlotSetting = DefaultPlotSetting(
        ctrl_title=Qt.CheckState.Checked,
        color_title='#000000',
        font_title=QFont(),
        padding_title=0,
        ctrl_x_axis=Qt.CheckState.Checked,
        show_x_ticks=Qt.CheckState.Checked,
        rotation_x_ticks=0,
        color_x_ticks='#000000',
        font_x_ticks=QFont(),
        padding_x_ticks=0,
        ctrl_y_axis=Qt.CheckState.Checked,
        show_y_ticks=Qt.CheckState.Checked,
        rotation_y_ticks=0,
        color_y_ticks='#000000',
        font_y_ticks=QFont(),
        padding_y_ticks=0,
        width_fig=10,
        height_fig=8,
        dpi_fig=100,
        bgcolor_fig='#ffffff',
        show_grid=Qt.CheckState.Checked,
        color_grid='#ffffff',
        style_grid=0,
        linew_grid=1,
        show_x_label=Qt.CheckState.Checked,
        rotation_x_label=0,
        color_x_label='#000000',
        font_x_label=QFont(),
        padding_x_label=0
    )

    def __init__(self):
        super().__init__()

        # 标题
        self.ctrl_title = Check(self.defaultPlotSetting.ctrl_title)
        self.color_title = ColorDataTButton(self.defaultPlotSetting.color_title)
        self.font_title = FontDataTButton(self.defaultPlotSetting.font_title)
        self.padding_title = Spin(self.defaultPlotSetting.padding_title)

        # x轴系列
        self.ctrl_x_axis = Check(self.defaultPlotSetting.ctrl_x_axis)  # 总控
        self.show_x_ticks = Check(self.defaultPlotSetting.show_x_ticks)
        self.rotation_x_ticks = Spin(self.defaultPlotSetting.rotation_x_ticks)
        self.color_x_ticks = ColorDataTButton(self.defaultPlotSetting.color_x_ticks)
        self.font_x_ticks = FontDataTButton(self.defaultPlotSetting.font_x_ticks)
        self.padding_x_ticks = Spin(self.defaultPlotSetting.padding_x_ticks)
        self.show_x_label = Check(self.defaultPlotSetting.show_x_label)
        self.rotation_x_label = Spin(self.defaultPlotSetting.rotation_x_label)
        self.color_x_label = ColorDataTButton(self.defaultPlotSetting.color_x_label)
        self.font_x_label = FontDataTButton(self.defaultPlotSetting.font_x_label)
        self.padding_x_label = Spin(self.defaultPlotSetting.padding_x_label)

        # y轴系列
        self.ctrl_y_axis = Check(self.defaultPlotSetting.ctrl_y_axis)
        self.show_y_ticks = Check(self.defaultPlotSetting.show_y_ticks)
        self.rotation_y_ticks = Spin(self.defaultPlotSetting.rotation_y_ticks)
        self.color_y_ticks = ColorDataTButton(self.defaultPlotSetting.color_y_ticks)
        self.font_y_ticks = FontDataTButton(self.defaultPlotSetting.font_y_ticks)
        self.padding_y_ticks = Spin(self.defaultPlotSetting.padding_y_ticks)

        # 画布
        self.width_fig = Spin(self.defaultPlotSetting.width_fig)
        self.height_fig = Spin(self.defaultPlotSetting.height_fig)
        self.dpi_fig = Spin(self.defaultPlotSetting.dpi_fig, 70, 900, 10)
        self.bgcolor_fig = ColorDataTButton(self.defaultPlotSetting.bgcolor_fig)

        # 网格线
        self.show_grid = Check(self.defaultPlotSetting.show_grid)
        self.color_grid = ColorDataTButton(self.defaultPlotSetting.color_grid)
        self.style_grid = SelectBox(self.defaultPlotSetting.style_grid, list(SelectBox_style_grid.values()))
        self.linew_grid = Spin(self.defaultPlotSetting.linew_grid, 0, 10, 1)

        self.__setUI()
    def __setUI(self) -> None:
        lay = QFormLayout()

        self.addH(lay, QLabel('标题设置'))
        # lay.addWidget()
        lay.addRow(self.ctrl_title, QLabel('标题控制'))
        lay.addRow(self.color_title, QLabel('颜色'))
        lay.addRow(self.font_title, QLabel('字体'))
        lay.addRow(self.padding_title, QLabel('偏移'))
        lay.addRow(SplitterLine())

        self.addH(lay, QLabel('X轴设置'))
        lay.addRow(self.ctrl_x_axis, QLabel('X轴控制'))
        lay.addRow(self.show_x_ticks, QLabel('标签显示'))
        lay.addRow(self.rotation_x_ticks, QLabel('标签角度'))
        lay.addRow(self.font_x_ticks, QLabel('标签字体'))
        lay.addRow(self.padding_x_ticks, QLabel('标签偏移'))
        lay.addRow(self.show_x_label, QLabel('名称显示'))
        lay.addRow(self.rotation_x_label, QLabel('名称角度'))
        lay.addRow(self.font_x_label, QLabel('名称字体'))
        lay.addRow(self.padding_x_label, QLabel('名称偏移'))
        lay.addRow(SplitterLine())

        self.addH(lay, QLabel('Y轴设置'))
        lay.addRow(self.ctrl_y_axis, QLabel('Y轴控制'))
        lay.addRow(self.show_y_ticks, QLabel('显示'))
        lay.addRow(self.rotation_y_ticks, QLabel('角度'))
        lay.addRow(self.font_y_ticks, QLabel('字体'))
        lay.addRow(self.padding_y_ticks, QLabel('偏移'))
        lay.addRow(SplitterLine())

        self.addH(lay, QLabel('画布设置'))
        lay.addRow(self.width_fig, QLabel('宽'))
        lay.addRow(self.width_fig, QLabel('高'))
        lay.addRow(self.dpi_fig, QLabel('DPI'))
        lay.addRow(self.bgcolor_fig, QLabel('背景颜色'))
        lay.addRow(SplitterLine())

        self.addH(lay, QLabel('网格设置'))
        lay.addRow(self.show_grid, QLabel('显示'))
        lay.addRow(self.color_grid, QLabel('颜色'))
        lay.addRow(self.style_grid, QLabel('样式'))
        lay.addRow(self.linew_grid, QLabel('线宽'))
        lay.addRow(SplitterLine())

        center_container = QWidget()
        center_layout = QHBoxLayout(center_container)
        center_layout.addStretch()
        inner_widget = QWidget()
        inner_widget.setLayout(lay)
        inner_widget.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        center_layout.addWidget(inner_widget)
        center_layout.addStretch()
        self.setWidgetResizable(True)
        self.setWidget(center_container)

    @staticmethod
    def addH(l : QFormLayout, w : QWidget):
        h = QHBoxLayout()
        h.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l.addRow(h)
        h.addWidget(w)

if __name__ == '__main__':
    app = QApplication([])
    ui = PlotBar()
    ui.show()
    app.exec()
