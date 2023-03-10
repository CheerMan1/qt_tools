import sys

from PySide6.QtCore import QMetaObject, QCoreApplication
from PySide6.QtWidgets import QDialog, QMessageBox, QLabel, QHBoxLayout, QLineEdit, QVBoxLayout, QFormLayout, QComboBox, \
    QSpacerItem, QSizePolicy, QPushButton


class __Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(291, 95)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.comboBox = QComboBox(Dialog)
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboBox)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.lineedit_password = QLineEdit(Dialog)
        self.lineedit_password.setObjectName(u"lineedit_password")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineedit_password)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.button_ok = QPushButton(Dialog)
        self.button_ok.setObjectName(u"button_ok")
        self.button_ok.setAutoDefault(True)

        self.horizontalLayout.addWidget(self.button_ok)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u8d26\u6237:", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Dialog", u"\u7ba1\u7406\u5458", None))

        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u5bc6\u7801:", None))
        self.button_ok.setText(QCoreApplication.translate("Dialog", u"\u786e\u8ba4", None))
    # retranslateUi


class AdministratorDialog(QDialog, __Ui_Dialog):
    def __init__(self, ps, parent=None):
        super(AdministratorDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("管理员")

        self.default_ps = ps
        self.is_ok = False

        self.lineedit_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.button_ok.clicked.connect(self.on_ok_btn)
        self.lineedit_password.setFocus()

    def on_ok_btn(self):
        text = self.lineedit_password.text()
        self.is_ok = (text == self.default_ps)

        if not self.is_ok:
            QMessageBox.warning(self, "提示", "验证失败, 请检查密码")
        else:
            self.close()


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)

    windwo = AdministratorDialog(ps="123456")
    windwo.show()
    sys.exit(app.exec())

