from PySide6.QtWidgets import (
    QApplication, QWidget, QComboBox, QVBoxLayout,
    QLineEdit, QLabel
)

class DynamicUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("根据 ComboBox 显示控件")

        self.combo = QComboBox()
        self.combo.addItems(["0", "1", "2", "3", "4", "5"])  # 显示 0~5 个控件

        self.input_area = QWidget()
        self.input_layout = QVBoxLayout(self.input_area)
        self.input_layout.setSpacing(5)
        self.input_layout.setContentsMargins(0, 0, 0, 0)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(QLabel("选择显示多少个输入框:"))
        main_layout.addWidget(self.combo)
        main_layout.addWidget(self.input_area)

        self.combo.currentIndexChanged.connect(self.update_inputs)

        self.line_edits = []  # 保存所有已添加的输入框
        self.update_inputs(0)  # 初始化

    def update_inputs(self, index):
        count = int(self.combo.currentText())

        # 清除旧控件
        for widget in self.line_edits:
            self.input_layout.removeWidget(widget)
            widget.deleteLater()
        self.line_edits.clear()

        # 添加新控件
        for i in range(count):
            edit = QLineEdit()
            edit.setPlaceholderText(f"输入框 {i + 1}")
            self.input_layout.addWidget(edit)
            self.line_edits.append(edit)

        self.adjustSize()

app = QApplication([])
win = DynamicUI()
win.show()
app.exec()
