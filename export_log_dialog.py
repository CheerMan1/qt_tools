import os
import shutil
import sys
import time

import py7zr

from PySide6.QtCore import Signal, QThread, QTimer
from PySide6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QLineEdit, QSizePolicy, \
    QFileDialog, QMessageBox

__all__ = ["ExportLogDialog"]


def zip_7z(src_path, dst_path):
    with py7zr.SevenZipFile(dst_path, 'w') as archive:
        folder_name = os.path.split(src_path)[1]  # 为解压后的文件夹名
        archive.writeall(src_path, folder_name)


class ExportThread(QThread):
    isFinishSignal = Signal()
    isErrorSignal = Signal(Exception)

    def __init__(self):
        super(ExportThread, self).__init__()
        self.export_path = ''
        self.dst_path = ''

    def run(self):
        try:
            zip_7z(self.export_path, self.dst_path)
            self.isFinishSignal.emit()
        except Exception as e:
            self.isErrorSignal.emit(e)


class ExportLogDialog(QDialog):
    def __init__(self, log_folder_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle('导出日志')
        self.resize(500, 130)

        self.src_log_path = log_folder_path

        # ui
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        h_layout = QHBoxLayout()
        label = QLabel("导出路径:")
        self.path_lineedit = QLineEdit(self)
        self.path_lineedit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.choose_path_button = QPushButton("选择路径", self)
        self.choose_path_button.clicked.connect(self.on_choose_path)
        h_layout.addWidget(label)
        h_layout.addWidget(self.path_lineedit)
        h_layout.addWidget(self.choose_path_button)

        hh_layout = QHBoxLayout()
        self.export_button = QPushButton("确认", self)
        self.export_button.clicked.connect(self.on_export)
        hh_layout.addStretch()
        hh_layout.addWidget(self.export_button)

        main_layout.addLayout(h_layout)
        main_layout.addLayout(hh_layout)
        self.info_label = QLabel()
        main_layout.addWidget(self.info_label)

        self.path_lineedit.setReadOnly(True)
        self.export_button.setDefault(True)

        self.exporting_text_timer = QTimer()
        self.exporting_text_timer.timeout.connect(self.on_start_set_exporting_text)

        # thread
        self.thread = ExportThread()
        self.thread.isFinishSignal.connect(self.on_export_finish)
        self.thread.isErrorSignal.connect(self.on_export_error)

    def on_choose_path(self):
        file_name = QFileDialog.getSaveFileName(self, '导出路径', "log.7z", "日志文件" + '(*.7z)')
        if file_name[0] != "":
            if file_name[0][-3:] == '.7z':
                file_path = file_name[0]
            else:
                file_path = file_name[0] + '.7z'
                if os.path.exists(file_path):
                    replay = QMessageBox.question(self, "提示", "文件已经存在,是否替代?",
                                                  QMessageBox.Cancel | QMessageBox.Yes, QMessageBox.Yes)
                    if replay == QMessageBox.Cancel:
                        return
            self.path_lineedit.setText(file_path)
            self.path_lineedit.setToolTip(file_path)

    def on_export(self):
        export_path = self.path_lineedit.text()

        export_folder_path = os.path.split(export_path)[0]
        if not export_path:
            QMessageBox.information(self, "信息", '请先选择导出路径')
            return
        if not os.path.exists(export_folder_path):
            QMessageBox.information(self, "信息", f'导出路径不存在: {export_folder_path}')
            return
        if not self.src_log_path:
            QMessageBox.information(self, "信息", '日志文件路径错误')
            return
        if not os.path.exists(self.src_log_path):
            QMessageBox.information(self, "信息", f'日志文件路径不存在: {self.src_log_path}')
            return

        if os.access(export_folder_path, os.W_OK) and os.access(export_folder_path, os.R_OK):
            self.thread.export_path = self.src_log_path
            self.thread.dst_path = export_path
            self.exporting_text_timer.start(1000)
            self.thread.start()
            self.export_button.setEnabled(False)
            self.choose_path_button.setEnabled(False)
        else:
            QMessageBox.warning(self, "信息", '当前选择路径没有读写权限, 请重新选择路径')

    def on_start_set_exporting_text(self):
        text = "导出中"
        point_count = len(self.info_label.text()) % 3 + 1
        self.info_label.setText(text + "." * point_count)

    def on_export_finish(self):
        self.exporting_text_timer.stop()
        self.thread.quit()
        self.thread.wait()
        self.info_label.setText("导出成功")
        self.info_label.setStyleSheet("background:green")
        self.export_button.setEnabled(True)
        self.choose_path_button.setEnabled(True)

    def on_export_error(self, error):
        self.exporting_text_timer.stop()
        self.thread.quit()
        self.thread.wait()
        self.export_button.setEnabled(True)
        self.choose_path_button.setEnabled(True)
        QMessageBox.critical(self, "错误", f"导出失败: {error}")
        self.info_label.setText("导出失败")
        self.info_label.setStyleSheet("background:red")


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)

    path = input("请输入日志存放的文件夹路径: ")
    if path:
        if os.path.exists(path):
            windwo = ExportLogDialog(log_folder_path='C:/Users/86176/Desktop/project/pyTools/python/log')
            windwo.show()
            sys.exit(app.exec())
