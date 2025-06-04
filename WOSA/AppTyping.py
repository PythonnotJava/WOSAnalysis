from typing import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

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
    def __init__(self, s : Qt.CheckState = Qt.CheckState.Checked, unabled : bool = False, **kwargs):
        super().__init__(**kwargs)
        self.setCheckState(s)

        self.setEnabled(unabled)

class Spin(QSpinBox):
    def __init__(self, value : int = 0, range_from : int = 0, range_to : int = 180, step : int = 1, minW : Optional[int] = 50, **kwargs):
        super().__init__(**kwargs)

        self.setRange(range_from, range_to)
        self.setSingleStep(step)
        self.setValue(value)
        if minW:
            self.setMinimumWidth(minW)

class TButton(QToolButton):
    def __init__(self, text : Optional[str] = None, icon : Optional[QIcon] = None, minW : Optional[int] = 50, **kwargs):
        super().__init__(**kwargs)

        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        if icon:
            self.setIcon(icon)
        if text:
            self.setText(text)
        if minW:
            self.setMinimumWidth(minW)

class FontDataTButton(TButton):
    def __init__(self, font : QFont, **kwargs):
        super().__init__(**kwargs)

        self.fontData = font
        self.setText(font.pointSize().__str__())

class ColorDataTButton(TButton):
    def __init__(self, color : str, **kwargs):
        super().__init__(**kwargs)

        self.colorData = color
        self.setColor(color)

    def setColor(self, c : str):
        self.setStyleSheet(f'background-color:{c}')
class SelectBox(QComboBox):
    def __init__(self, defalutIndex, l : list[str]):
        super().__init__()
        self.addItems(l)
        self.setCurrentIndex(defalutIndex)

    def wheelEvent(self, e, /):
        pass

class LineInput(QTextEdit):
    def __init__(self, p):
        super().__init__()
        self.setFixedWidth(200)
        self.setPlaceholderText(p)

class LineEdit(QLineEdit):
    def __init__(self, minW : Optional[int] = None, p : Optional[str] = None, abled : bool = True):
        super().__init__()

        if minW:
            self.setMinimumWidth(minW)
        if p:
            self.setPlaceholderText(p)

        self.setEnabled(abled)


class RowWidgetByWidget(QHBoxLayout):
    def __init__(self, w1, w2):
        super().__init__()

        self.addWidget(w1)
        self.addWidget(w2)

        self.w1 = w1
        self.w2 = w2