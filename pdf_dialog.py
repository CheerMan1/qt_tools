import fitz

from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QImage, QPixmap, QTransform
from PySide6.QtWidgets import QDialog, QLabel

"""
需要安装
pip install fitz
pip install pymupdf
"""


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(680, 992)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 660, 972))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_label = QtWidgets.QVBoxLayout()
        self.verticalLayout_label.setObjectName("verticalLayout_label")
        self.verticalLayout_3.addLayout(self.verticalLayout_label)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


class PDFDialog(QDialog, Ui_Dialog):
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("帮助")

        self.all_pages = 0
        self.pages = 0
        self.file_path = path

        self.show_image()

    def show_image(self):
        doc = fitz.open(self.file_path)
        all_pages = int(doc.page_count)
        for index in range(all_pages):
            page = doc.load_page(index)
            page_pixmap = page.get_pixmap()
            # 将Pixmap转换为QImage
            image_format = QImage.Format_RGBA8888 if page_pixmap.alpha else QImage.Format_RGB888
            page_image = QImage(page_pixmap.samples, page_pixmap.width,
                                page_pixmap.height, page_pixmap.stride, image_format)
            width = page_image.width()
            height = page_image.height()
            pix = QPixmap.fromImage(page_image)
            trans = QTransform()
            trans.rotate(0)
            new = pix.transformed(trans)

            label = QLabel(str(index))
            label.setScaledContents(True)
            label.setPixmap(new)
            label.setStyleSheet("background-color: red")
            self.verticalLayout_label.addWidget(label)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)

    windwo = PDFDialog(path="test.pdf")
    windwo.show()
    sys.exit(app.exec())
