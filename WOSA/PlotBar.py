from typing import *
from dataclasses import dataclass
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt

from AppTyping import *

SelectBox_style_grid = {
    '直线' : '-',
    '点划线' : '-.',
    '虚线' : '--',
    '点线' : ':',
    '隐藏线条' : ''
}

SelectBox_position_title = {
    '靠左' : 'left',
    '居中' : 'center',
    '靠右' : 'right'
}

SelectBox_tick_direction = {
    '外部' : 'out',
    '内部' : 'in',
    '两侧' : 'inout'
}

SelectBox_which_grid = {
    '都有' : 'both',
    '主轴' : 'major',
    '次轴' : 'minor'
}

SelectBox_location_legend = {
    "最佳": "best",
    "右上": "upper right",
    "左上": "upper left",
    "左下": "lower left",
    "右下": "lower right",
    "右侧": "right",
    "左侧中部": "center left",
    "右侧中部": "center right",
    "下方中部": "lower center",
    "上方中部": "upper center",
    "正中": "center"
}

BLACK = "#000000"
WHITE = '#ffffff'

@dataclass
class DefaultPlotSetting:
    # title
    title : str = ''
    color_title : str = BLACK
    font_title : QFont = QFont()
    padding_left_title : int = 0
    padding_top_title: int = 0
    padding_right_title: int = 0
    padding_bottom_title: int = 0
    position_title : int = 0

    # x
    ctrl_x_axis : Qt.CheckState = Qt.CheckState.Checked
    show_x_ticks : Qt.CheckState = Qt.CheckState.Checked
    rotation_x_ticks : int = 0
    color_x_ticks : str = BLACK
    font_x_ticks : QFont = QFont()
    padding_left_x_ticks : int = 0
    padding_right_x_ticks : int = 0
    padding_top_x_ticks : int = 0
    padding_bottom_x_ticks : int = 0
    color_x_axis: str = BLACK
    linew_x_axis: int = 1
    direction_x_axis : int = 0
    x_label: str = ''
    rotation_x_label: int = 0
    color_x_label: str = BLACK
    font_x_label: QFont = QFont()
    padding_left_x_label: int = 0
    padding_right_x_label : int = 0
    padding_top_x_label: int = 0
    padding_bottom_x_label: int = 0

    # y
    ctrl_y_axis: Qt.CheckState = Qt.CheckState.Checked
    show_y_ticks: Qt.CheckState = Qt.CheckState.Checked
    rotation_y_ticks: int = 0
    color_y_ticks: str = BLACK
    font_y_ticks: QFont = QFont()
    padding_left_y_ticks: int = 0
    padding_right_y_ticks: int = 0
    padding_top_y_ticks: int = 0
    padding_bottom_y_ticks: int = 0
    color_y_axis: str = BLACK
    linew_y_axis: int = 1
    direction_y_axis : int = 0
    y_label: str = ''
    rotation_y_label: int = 0
    color_y_label: str = BLACK
    font_y_label: QFont = QFont()
    padding_left_y_label: int = 0
    padding_right_y_label: int = 0
    padding_top_y_label: int = 0
    padding_bottom_y_label: int = 0

    # fig
    width_fig : int = 10
    height_fig : int = 8
    dpi_fig : int = 100
    bgcolor_fig : str = WHITE

    # grid
    show_grid : Qt.CheckState = Qt.CheckState.Checked
    which_grid : int = 0
    color_grid : str = WHITE
    style_grid : int = 0
    linew_grid : int = 1

    # legend
    show_legend : Qt.CheckState = Qt.CheckState.Checked
    font_legend : QFont = QFont()
    location_legend : int = 0
    frameon_legend : Qt.CheckState = Qt.CheckState.Checked

class PlotBar(QScrollArea):
    # 放到类属性中，做统一同步
    defaultPlotSetting = DefaultPlotSetting()

    def __init__(self):
        super().__init__()

        self.models = SelectBox(0, ['原图修改模式', '新图模式'])
        self.draw_new_button = TButton('绘制')

        # 标题
        self.title = LineInput('标题名字，可以空着')
        self.color_title = ColorDataTButton(self.defaultPlotSetting.color_title)
        self.font_title = FontDataTButton(self.defaultPlotSetting.font_title)
        self.padding_left_title = Spin(self.defaultPlotSetting.padding_left_title, 0, 50, 1)
        self.padding_right_title = Spin(self.defaultPlotSetting.padding_right_title, 0, 50, 1)
        self.padding_top_title = Spin(self.defaultPlotSetting.padding_top_title, 0, 50, 1)
        self.padding_bottom_title = Spin(self.defaultPlotSetting.padding_bottom_title, 0, 50, 1)
        self.position_title = SelectBox(0, list(SelectBox_position_title.keys()))

        # x轴系列
        self.ctrl_x_axis = Check(self.defaultPlotSetting.ctrl_x_axis)  # 总控
        self.show_x_ticks = Check(self.defaultPlotSetting.show_x_ticks)
        self.rotation_x_ticks = Spin(self.defaultPlotSetting.rotation_x_ticks)
        self.color_x_ticks = ColorDataTButton(self.defaultPlotSetting.color_x_ticks)
        self.font_x_ticks = FontDataTButton(self.defaultPlotSetting.font_x_ticks)
        self.padding_left_x_ticks = Spin(self.defaultPlotSetting.padding_left_x_ticks, 0, 50, 1)
        self.padding_right_x_ticks = Spin(self.defaultPlotSetting.padding_right_x_ticks, 0, 50, 1)
        self.padding_top_x_ticks = Spin(self.defaultPlotSetting.padding_top_x_ticks, 0, 50, 1)
        self.padding_bottom_x_ticks = Spin(self.defaultPlotSetting.padding_bottom_x_ticks, 0, 50, 1)
        self.color_x_axis = ColorDataTButton(self.defaultPlotSetting.color_x_axis)
        self.linew_x_axis = Spin(self.defaultPlotSetting.linew_x_axis, 0, 10, 1)
        self.direction_x_axis = SelectBox(self.defaultPlotSetting.direction_x_axis, list(SelectBox_tick_direction.keys()))
        self.x_label = LineInput('X轴名字，可以空着')
        self.rotation_x_label = Spin(self.defaultPlotSetting.rotation_x_label)
        self.color_x_label = ColorDataTButton(self.defaultPlotSetting.color_x_label)
        self.font_x_label = FontDataTButton(self.defaultPlotSetting.font_x_label)
        self.padding_left_x_label = Spin(self.defaultPlotSetting.padding_left_x_label, 0, 50, 1)
        self.padding_right_x_label = Spin(self.defaultPlotSetting.padding_right_x_label, 0, 50, 1)
        self.padding_top_x_label = Spin(self.defaultPlotSetting.padding_top_x_label, 0, 50, 1)
        self.padding_bottom_x_label = Spin(self.defaultPlotSetting.padding_bottom_x_label, 0, 50, 1)

        # y轴系列
        self.ctrl_y_axis = Check(self.defaultPlotSetting.ctrl_y_axis)  # 总控
        self.show_y_ticks = Check(self.defaultPlotSetting.show_y_ticks)
        self.rotation_y_ticks = Spin(self.defaultPlotSetting.rotation_y_ticks)
        self.color_y_ticks = ColorDataTButton(self.defaultPlotSetting.color_y_ticks)
        self.font_y_ticks = FontDataTButton(self.defaultPlotSetting.font_y_ticks)
        self.padding_left_y_ticks = Spin(self.defaultPlotSetting.padding_left_y_ticks, 0, 50, 1)
        self.padding_right_y_ticks = Spin(self.defaultPlotSetting.padding_right_y_ticks, 0, 50, 1)
        self.padding_top_y_ticks = Spin(self.defaultPlotSetting.padding_top_y_ticks, 0, 50, 1)
        self.padding_bottom_y_ticks = Spin(self.defaultPlotSetting.padding_bottom_y_ticks, 0, 50, 1)
        self.color_y_axis = ColorDataTButton(self.defaultPlotSetting.color_y_axis)
        self.linew_y_axis = Spin(self.defaultPlotSetting.linew_y_axis, 0, 10, 1)
        self.direction_y_axis = SelectBox(self.defaultPlotSetting.direction_y_axis, list(SelectBox_tick_direction.keys()))
        self.y_label = LineInput('Y轴名字，可以空着')
        self.rotation_y_label = Spin(self.defaultPlotSetting.rotation_y_label)
        self.color_y_label = ColorDataTButton(self.defaultPlotSetting.color_y_label)
        self.font_y_label = FontDataTButton(self.defaultPlotSetting.font_y_label)
        self.padding_left_y_label = Spin(self.defaultPlotSetting.padding_left_y_label, 0, 50, 1)
        self.padding_right_y_label = Spin(self.defaultPlotSetting.padding_right_y_label, 0, 50, 1)
        self.padding_top_y_label = Spin(self.defaultPlotSetting.padding_top_y_label, 0, 50, 1)
        self.padding_bottom_y_label = Spin(self.defaultPlotSetting.padding_bottom_y_label, 0, 50, 1)

        # 画布
        self.width_fig = Spin(self.defaultPlotSetting.width_fig, 2, 100, 1)
        self.height_fig = Spin(self.defaultPlotSetting.height_fig, 2, 100, 1)
        self.dpi_fig = Spin(self.defaultPlotSetting.dpi_fig, 70, 900, 10)
        self.bgcolor_fig = ColorDataTButton(self.defaultPlotSetting.bgcolor_fig)

        # 网格线
        self.show_grid = Check(self.defaultPlotSetting.show_grid)
        self.which_grid = SelectBox(0, list(SelectBox_which_grid.keys()))
        self.color_grid = ColorDataTButton(self.defaultPlotSetting.color_grid)
        self.style_grid = SelectBox(self.defaultPlotSetting.style_grid, list(SelectBox_style_grid.keys()))
        self.linew_grid = Spin(self.defaultPlotSetting.linew_grid, 0, 10, 1)

        # 图例
        self.show_legend = Check(self.defaultPlotSetting.show_legend)
        self.font_legend = FontDataTButton(self.defaultPlotSetting.font_legend)
        self.location_legend = SelectBox(self.defaultPlotSetting.location_legend, list(SelectBox_location_legend.keys()))
        self.frameon_legend = Check(self.defaultPlotSetting.frameon_legend)

        self.__setUI()
    def __setUI(self) -> None:
        lay = QFormLayout()

        lay.addRow(self.models, QLabel('模式选择'))
        lay.addRow(SplitterLine())

        self.addH(lay, QLabel('标题设置'))
        # lay.addWidget()
        lay.addRow(self.title, QLabel('标题控制'))
        lay.addRow(self.color_title, QLabel('颜色'))
        lay.addRow(self.font_title, QLabel('字体'))
        lay.addRow(self.padding_left_title, QLabel('左偏移'))
        lay.addRow(self.padding_right_title, QLabel('右偏移'))
        lay.addRow(self.padding_top_title, QLabel('上偏移'))
        lay.addRow(self.padding_bottom_title, QLabel('下偏移'))
        lay.addRow(self.position_title, QLabel('对齐方式'))
        lay.addRow(SplitterLine())

        self.addH(lay, QLabel('X轴设置'))
        lay.addRow(self.ctrl_x_axis, QLabel('X轴控制'))
        lay.addRow(self.show_x_ticks, QLabel('标签显示'))
        lay.addRow(self.rotation_x_ticks, QLabel('标签角度'))
        lay.addRow(self.font_x_ticks, QLabel('标签字体'))
        lay.addRow(self.padding_left_x_ticks, QLabel('标签左偏移'))
        lay.addRow(self.padding_right_x_ticks, QLabel('标签右偏移'))
        lay.addRow(self.padding_top_x_ticks, QLabel('标签上偏移'))
        lay.addRow(self.padding_bottom_x_ticks, QLabel('标签下偏移'))
        lay.addRow(self.color_x_axis, QLabel('标签颜色'))
        lay.addRow(self.linew_x_axis, QLabel('标签线宽'))
        lay.addRow(self.direction_x_axis, QLabel('标签方向'))
        lay.addRow(self.x_label, QLabel('名称显示'))
        lay.addRow(self.rotation_x_label, QLabel('名称角度'))
        lay.addRow(self.font_x_label, QLabel('名称字体'))
        lay.addRow(self.padding_left_x_label, QLabel('轴标题左偏移'))
        lay.addRow(self.padding_right_x_label, QLabel('轴标题右偏移'))
        lay.addRow(self.padding_top_x_label, QLabel('轴标题上偏移'))
        lay.addRow(self.padding_bottom_x_label, QLabel('轴标题下偏移'))
        lay.addRow(SplitterLine())

        self.addH(lay, QLabel('Y轴设置'))
        lay.addRow(self.ctrl_y_axis, QLabel('Y轴控制'))
        lay.addRow(self.show_y_ticks, QLabel('标签显示'))
        lay.addRow(self.rotation_y_ticks, QLabel('标签角度'))
        lay.addRow(self.font_y_ticks, QLabel('标签字体'))
        lay.addRow(self.padding_left_y_ticks, QLabel('标签左偏移'))
        lay.addRow(self.padding_right_y_ticks, QLabel('标签右偏移'))
        lay.addRow(self.padding_top_y_ticks, QLabel('标签上偏移'))
        lay.addRow(self.padding_bottom_y_ticks, QLabel('标签下偏移'))
        lay.addRow(self.color_y_axis, QLabel('标签颜色'))
        lay.addRow(self.linew_y_axis, QLabel('标签线宽'))
        lay.addRow(self.direction_y_axis, QLabel('标签方向'))
        lay.addRow(self.y_label, QLabel('名称显示'))
        lay.addRow(self.rotation_y_label, QLabel('名称角度'))
        lay.addRow(self.font_y_label, QLabel('名称字体'))
        lay.addRow(self.padding_left_y_label, QLabel('轴标题左偏移'))
        lay.addRow(self.padding_right_y_label, QLabel('轴标题右偏移'))
        lay.addRow(self.padding_top_y_label, QLabel('轴标题上偏移'))
        lay.addRow(self.padding_bottom_y_label, QLabel('轴标题下偏移'))
        lay.addRow(SplitterLine())

        self.addH(lay, QLabel('画布设置'))
        lay.addRow(self.width_fig, QLabel('宽'))
        lay.addRow(self.height_fig, QLabel('高'))
        lay.addRow(self.dpi_fig, QLabel('DPI'))
        lay.addRow(self.bgcolor_fig, QLabel('背景颜色'))
        lay.addRow(SplitterLine())

        self.addH(lay, QLabel('网格设置'))
        lay.addRow(self.show_grid, QLabel('显示'))
        lay.addRow(self.which_grid, QLabel('显示方式'))
        lay.addRow(self.color_grid, QLabel('颜色'))
        lay.addRow(self.style_grid, QLabel('样式'))
        lay.addRow(self.linew_grid, QLabel('线宽'))
        lay.addRow(SplitterLine())

        self.addH(lay, QLabel('图例设置'))
        lay.addRow(self.show_legend, QLabel('显示'))
        lay.addRow(self.font_legend, QLabel('字体'))
        lay.addRow(self.location_legend, QLabel('位置'))
        lay.addRow(self.frameon_legend, QLabel('显示边框'))
        lay.addRow(SplitterLine())

        lay.addRow(self.draw_new_button)
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
        self.setMinimumWidth(300)

        self.draw_new_button.setEnabled(bool(self.models.currentIndex()))

        # connect
        self.models.currentIndexChanged.connect(lambda index : self.draw_new_button.setEnabled(bool(index)))

    @staticmethod
    def addH(l : QFormLayout, w : QWidget):
        h = QHBoxLayout()
        h.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l.addRow(h)
        h.addWidget(w)

    def getState(self) -> dict[str, Any]:
        return {
            #
            'ctrl_title' : self.title.toPlainText(),
            'color_title' : self.color_title.colorData,
            'font_title' : self.font_title.fontData,
            'padding_left_title' : self.padding_left_title.value(),
            'padding_right_title' : self.padding_right_title.value(),
            'padding_top_title' : self.padding_top_title.value(),
            'padding_bottom_title' : self.padding_bottom_title.value(),
            'position_title' : SelectBox_position_title[self.position_title.currentText()],
            #
            'ctrl_x_axis' : self.ctrl_x_axis.isChecked(),
            'show_x_ticks' : self.show_x_ticks.isChecked(),
            'rotation_x_ticks' : self.rotation_x_ticks.value(),
            'font_x_ticks' : self.font_x_ticks.fontData,
            'padding_left_x_ticks' : self.padding_left_x_ticks.value(),
            'padding_right_x_ticks' : self.padding_right_x_ticks.value(),
            'padding_top_x_ticks' : self.padding_top_x_ticks.value(),
            'padding_bottom_x_ticks' : self.padding_bottom_x_ticks.value(),
            'color_x_axis' : self.color_x_axis.colorData,
            'linew_x_axis' : self.linew_x_axis.value(),
            'direction_x_axis' : SelectBox_tick_direction[self.direction_x_axis.currentText()],
            'show_x_label' : self.x_label.toPlainText(),
            'rotation_x_label' : self.rotation_x_label.value(),
            'font_x_label' : self.font_x_label.fontData,
            'padding_left_x_label' : self.padding_left_x_label.value(),
            'padding_right_x_label' : self.padding_right_x_label.value(),
            'padding_top_x_label' : self.padding_top_x_label.value(),
            'padding_bottom_x_label' : self.padding_bottom_x_label.value(),
            #
            'ctrl_y_ayis': self.ctrl_y_axis.isChecked(),
            'show_y_ticks': self.show_y_ticks.isChecked(),
            'rotation_y_ticks': self.rotation_y_ticks.value(),
            'font_y_ticks': self.font_y_ticks.fontData,
            'padding_left_y_ticks': self.padding_left_y_ticks.value(),
            'padding_right_y_ticks': self.padding_right_y_ticks.value(),
            'padding_top_y_ticks': self.padding_top_y_ticks.value(),
            'padding_bottom_y_ticks': self.padding_bottom_y_ticks.value(),
            'color_y_ayis': self.color_y_axis.colorData,
            'linew_y_ayis': self.linew_y_axis.value(),
            'direction_y_ayis': SelectBox_tick_direction[self.direction_y_axis.currentText()],
            'show_y_label': self.y_label.toPlainText(),
            'rotation_y_label': self.rotation_y_label.value(),
            'font_y_label': self.font_y_label.fontData,
            'padding_left_y_label': self.padding_left_y_label.value(),
            'padding_right_y_label': self.padding_right_y_label.value(),
            'padding_top_y_label': self.padding_top_y_label.value(),
            'padding_bottom_y_label': self.padding_bottom_y_label.value(),
            #
            'width_fig' : self.width_fig.value(),
            'height_fig' : self.height_fig.value(),
            'dpi_fig' : self.dpi_fig.value(),
            'bgcolor_fig' : self.bgcolor_fig.colorData,
            #
            'show_grid' : self.show_grid.isChecked(),
            'which_grid' : SelectBox_which_grid[self.which_grid.currentText()],
            'color_grid' : self.color_grid.colorData,
            'style_grid' : SelectBox_style_grid[self.style_grid.currentText()],
            'linew_grid' : self.linew_grid.value(),
            #
            'show_legend' : self.show_legend.isChecked(),
            'font_legend' : self.font_legend.fontData,
            'location_legend' : SelectBox_location_legend[self.location_legend.currentText()],
            'frameon_legend' : self.frameon_legend.isChecked()
        }

if __name__ == '__main__':
    app = QApplication([])
    ui = PlotBar()
    ui.show()
    app.exec()
