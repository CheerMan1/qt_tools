import re

from typing import Optional

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QLineEdit, QLabel, QDialog, QFormLayout, QMessageBox, QVBoxLayout


"""
通过正则限制扫码输入文本的格式
1. 可自定义需要扫码输入的文本
2. 自动跳转光标
3. 结果验证
"""


class SweepInputWidget(QLineEdit):
    def __init__(self, reg_ex: Optional[str] = None, parent=None):
        super().__init__(parent)
        self.reg_ex = reg_ex

        if reg_ex:
            validator = QRegularExpressionValidator(self.reg_ex, self)
            self.setValidator(validator)


class SweepWidget(QDialog):
    sweep_result_signal = Signal(dict)

    def __init__(self, labels: list, reg_exs: list, parent=None):
        super().__init__(parent)
        self.setWindowTitle("扫码获取字段")
        self.setMinimumWidth(500)
        self.setWindowModality(Qt.ApplicationModal)
        self.is_ok = False
        self.setStyleSheet("font-size: 28px")

        layout = QFormLayout()
        self.widget_collection = {}
        self.scan_fields = {}

        for tip, reg in zip(labels, reg_exs):
            line_edit = SweepInputWidget(reg)
            line_edit.setMinimumHeight(40)
            layout.addRow(tip + ": ", line_edit)
            self.widget_collection[tip] = line_edit
            line_edit.setProperty("reg", reg)

        widgets = list(self.widget_collection.values())
        for idx, widget in enumerate(widgets):
            if idx == len(widgets) - 1:
                widget.returnPressed.connect(self.on_ok)
            else:
                widget.returnPressed.connect(lambda idx=idx: widgets[idx + 1].setFocus())

        self.info_label = QLabel()
        self.info_label.setMinimumHeight(40)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(self.info_label)
        self.setLayout(main_layout)

        self.close()

    def on_ok(self):
        self.scan_fields.clear()
        for idx, (tip, widget) in enumerate(self.widget_collection.items()):
            reg = widget.property("reg")
            if reg is not None:
                match = re.match(reg, widget.text())
            else:
                match = True
            if not match:
                self.info_label.setStyleSheet("color: red;")
                self.info_label.setText("输入字段错误, 请重新扫描!!")
                widget.clear()
                widget.setFocus()
                return

            self.scan_fields[tip] = widget.text()
            widget.clear()

            if idx == 0:
                widget.setFocus()

        self.info_label.clear()
        self.is_ok = True
        self.sweep_result_signal.emit(self.scan_fields)
        self.close()

    def show(self) -> None:
        self.is_ok = False
        self.scan_fields.clear()
        super().show()

    def exec_(self) -> int:
        self.is_ok = False
        self.scan_fields.clear()
        super().exec_()


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    win = SweepWidget(labels=["mac", "sn"], reg_exs=["^BC[0-9A-Z]{15}$", "^BC[0-9A-Z]{15}$"])
    win.show()
    sys.exit(app.exec_())
