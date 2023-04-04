# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Time_Test_interface_loginYLdGBA.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(545, 236)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_Username = QLabel(Dialog)
        self.label_Username.setObjectName(u"label_Username")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_Username.setFont(font)

        self.verticalLayout.addWidget(self.label_Username)

        self.lineEdit_Username = QLineEdit(Dialog)
        self.lineEdit_Username.setObjectName(u"lineEdit_Username")
        font1 = QFont()
        font1.setPointSize(12)
        self.lineEdit_Username.setFont(font1)

        self.verticalLayout.addWidget(self.lineEdit_Username)

        self.label_Password = QLabel(Dialog)
        self.label_Password.setObjectName(u"label_Password")
        self.label_Password.setFont(font)

        self.verticalLayout.addWidget(self.label_Password)

        self.lineEdit_Password = QLineEdit(Dialog)
        self.lineEdit_Password.setObjectName(u"lineEdit_Password")
        self.lineEdit_Password.setFont(font1)

        self.verticalLayout.addWidget(self.lineEdit_Password)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_ForgotPassword = QPushButton(Dialog)
        self.pushButton_ForgotPassword.setObjectName(u"pushButton_ForgotPassword")
        font2 = QFont()
        font2.setPointSize(10)
        self.pushButton_ForgotPassword.setFont(font2)

        self.horizontalLayout.addWidget(self.pushButton_ForgotPassword)

        self.pushButton_Login = QPushButton(Dialog)
        self.pushButton_Login.setObjectName(u"pushButton_Login")
        self.pushButton_Login.setFont(font2)

        self.horizontalLayout.addWidget(self.pushButton_Login)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_Username.setText(QCoreApplication.translate("Dialog", u"Username", None))
        self.label_Password.setText(QCoreApplication.translate("Dialog", u"Password", None))
        self.pushButton_ForgotPassword.setText(QCoreApplication.translate("Dialog", u"Forgot password?", None))
        self.pushButton_Login.setText(QCoreApplication.translate("Dialog", u"Login", None))
    # retranslateUi

