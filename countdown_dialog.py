import sys
from PySide6.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QSizePolicy
from PySide6.QtGui import QFont
from PySide6.QtCore import QTimer, QTime, Qt, Signal


class CountdownDialog(QDialog):
    finished_signal = Signal()

    def __init__(self, seconds, text, parent=None):
        super().__init__(parent)
        self.text = text
        self.seconds = seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_text)
        self.timer.start(1000)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('倒计时窗口')

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 2, 0, 2)

        self.label = QLabel(str(self.seconds), self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.resize(400, 150)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Arial', 80))
        self.label.setStyleSheet("color: red;font-size:88px")

        self.info_label = QLabel(self)
        self.info_label.resize(400, 50)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setFont(QFont('Arial', 16))

        self.info_label.setText(self.text)

        layout.addWidget(self.label)
        layout.addWidget(self.info_label)
        self.setLayout(layout)

    def update_text(self):
        self.seconds -= 1
        if self.seconds <= 0:
            self._finish()
            self.close()
        else:
            self.label.setText(str(self.seconds))
            # self.info_label.setText('倒计时还剩 {} 秒'.format(self.seconds))

    def _finish(self):
        self.timer.stop()
        self.finished_signal.emit()

    def close_dialog(self):
        self.timer.stop()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CountdownDialog(10, "倒计时窗口")
    window.show()
    sys.exit(app.exec())
