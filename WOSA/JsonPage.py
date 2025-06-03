import json
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt

class JsonPage(QTextEdit):
    def __init__(self, data : dict):
        super().__init__()

        self.data = data

        self.__setUI()
    def __setUI(self) -> None:
        self.setText(json.dumps(self.data, indent=4, ensure_ascii=False))

if __name__ == '__main__':
    app = QApplication([])
    ui = JsonPage(
    {
    "name": "Alice",
    "age": 30,
    "hobbies": ["reading", "gaming", "hiking"],
    "address": {
        "city": "Wonderland",
        "zipcode": "12345"
        }
    }
    )
    ui.show()
    app.exec()