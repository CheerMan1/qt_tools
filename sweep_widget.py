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
    input_valid_signal = Signal(bool, str)

    def __init__(self, reg_ex: Optional[str] = None, parent=None):
        super().__init__(parent)
        self.reg_ex = reg_ex

        if reg_ex:
            validator = QRegularExpressionValidator(self.reg_ex, self)
            self.setValidator(validator)

    def keyPressEvent(self, event) -> None:
        if event.key() in [Qt.Key_Return, Qt.Key_Enter]:
            match = self.check_text_is_valid()
            self.input_valid_signal.emit(match, self.text())

            if not match:
                self.clear()
                self.setFocus()

        super().keyPressEvent(event)

    def check_text_is_valid(self):
        if self.reg_ex is not None:
            match = re.match(self.reg_ex, self.text()) is not None
        else:
            match = True

        return match

# 1. 指定正则

class SweepWidget(QDialog):
    sweep_result_signal = Signal(dict)

    def __init__(self, labels: list, reg_exs: list, parent=None):
        super().__init__(parent)
        self.setWindowTitle("扫码获取字段")
        self.setMinimumWidth(500)
        self.setWindowModality(Qt.ApplicationModal)
        self.is_ok = False

        layout = QFormLayout()
        self.widget_collection = {}

        for tip, reg in zip(labels, reg_exs):
            line_edit = SweepInputWidget(reg)
            label = QLabel(tip + ": ")
            layout.addRow(label, line_edit)
            self.widget_collection[tip] = line_edit

            label.setStyleSheet("font-size: 28px")

            line_edit.setMinimumHeight(40)
            line_edit.setProperty("reg", reg)
            line_edit.setStyleSheet("font-size: 28px")

        widgets = list(self.widget_collection.values())
        for idx, widget in enumerate(widgets):
            widget.input_valid_signal.connect(self.on_check_input_valid)
            if idx == 0:
                widget.setFocus()

            if idx == len(widgets) - 1:
                widget.returnPressed.connect(self.on_ok)
            else:
                widget.returnPressed.connect(lambda idx=idx: widgets[idx + 1].setFocus())

        self.info_label = QLabel()
        self.info_label.setMinimumHeight(40)
        self.info_label.setStyleSheet("font-size: 18px")

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(self.info_label)
        self.setLayout(main_layout)

        self.setVisible(False)

    def on_check_input_valid(self, match, text):
        self.info_label.clear()

        if not match:
            self.info_label.setText(f"'{text}' 输入字段错误, 请重新扫描!!")

    def on_ok(self):
        scan_fields = {}
        for idx, (tip, widget) in enumerate(self.widget_collection.items()):
            if not widget.check_text_is_valid():
                self.on_check_input_valid(False, widget.text())
                return
            scan_fields[tip] = widget.text()

        self.is_ok = True
        self.close()
        self.sweep_result_signal.emit(scan_fields)

    def closeEvent(self, event) -> None:
        if self.is_ok:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    win = SweepWidget(labels=["mac", "sn"], reg_exs=["^BC[0-9A-Z]{15}$", "^BC[0-9A-Z]{15}$"])
    win.show()
    sys.exit(app.exec())
