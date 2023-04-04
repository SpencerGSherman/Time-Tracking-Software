# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Time_Test_interface_NewTaskInpEgN.ui'
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
        Dialog.resize(414, 369)
        self.layoutWidget = QWidget(Dialog)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 20, 260, 321))
        self.verticalLayout_4 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_TaskName = QLabel(self.layoutWidget)
        self.label_TaskName.setObjectName(u"label_TaskName")
        font = QFont()
        font.setPointSize(14)
        self.label_TaskName.setFont(font)

        self.verticalLayout.addWidget(self.label_TaskName)

        self.lineEdit_TaskName = QLineEdit(self.layoutWidget)
        self.lineEdit_TaskName.setObjectName(u"lineEdit_TaskName")
        font1 = QFont()
        font1.setPointSize(12)
        self.lineEdit_TaskName.setFont(font1)

        self.verticalLayout.addWidget(self.lineEdit_TaskName)


        self.verticalLayout_4.addLayout(self.verticalLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_Deadline = QLabel(self.layoutWidget)
        self.label_Deadline.setObjectName(u"label_Deadline")
        self.label_Deadline.setFont(font)

        self.horizontalLayout.addWidget(self.label_Deadline)

        self.pushButton_NoDeadline = QPushButton(self.layoutWidget)
        self.pushButton_NoDeadline.setObjectName(u"pushButton_NoDeadline")
        self.pushButton_NoDeadline.setFont(font1)

        self.horizontalLayout.addWidget(self.pushButton_NoDeadline)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.dateTimeEdit_Deadline = QDateTimeEdit(self.layoutWidget)
        self.dateTimeEdit_Deadline.setObjectName(u"dateTimeEdit_Deadline")
        self.dateTimeEdit_Deadline.setFont(font1)

        self.verticalLayout_3.addWidget(self.dateTimeEdit_Deadline)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_Description = QLabel(self.layoutWidget)
        self.label_Description.setObjectName(u"label_Description")
        self.label_Description.setFont(font)

        self.verticalLayout_2.addWidget(self.label_Description)

        self.textEdit_Description = QTextEdit(self.layoutWidget)
        self.textEdit_Description.setObjectName(u"textEdit_Description")
        self.textEdit_Description.setFont(font1)

        self.verticalLayout_2.addWidget(self.textEdit_Description)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_TaskName.setText(QCoreApplication.translate("Dialog", u"Task Name", None))
        self.label_Deadline.setText(QCoreApplication.translate("Dialog", u"Deadline", None))
        self.pushButton_NoDeadline.setText(QCoreApplication.translate("Dialog", u"No Deadline", None))
        self.label_Description.setText(QCoreApplication.translate("Dialog", u"Description", None))
    # retranslateUi

