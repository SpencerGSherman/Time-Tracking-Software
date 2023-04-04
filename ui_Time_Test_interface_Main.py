# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Time_Test_interface_MainpbjatF.ui'
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
        Dialog.resize(470, 761)
        self.layoutWidget = QWidget(Dialog)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(32, 22, 431, 531))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_username = QLabel(self.layoutWidget)
        self.label_username.setObjectName(u"label_username")
        font = QFont()
        font.setPointSize(16)
        self.label_username.setFont(font)

        self.horizontalLayout.addWidget(self.label_username)

        self.pushButton_Sort = QPushButton(self.layoutWidget)
        self.pushButton_Sort.setObjectName(u"pushButton_Sort")
        font1 = QFont()
        font1.setPointSize(12)
        self.pushButton_Sort.setFont(font1)

        self.horizontalLayout.addWidget(self.pushButton_Sort)

        self.pushButton_Settings = QPushButton(self.layoutWidget)
        self.pushButton_Settings.setObjectName(u"pushButton_Settings")
        self.pushButton_Settings.setFont(font1)

        self.horizontalLayout.addWidget(self.pushButton_Settings)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.scrollArea = QScrollArea(self.layoutWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 402, 455))
        self.pushButton_CreatNewTask = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_CreatNewTask.setObjectName(u"pushButton_CreatNewTask")
        self.pushButton_CreatNewTask.setGeometry(QRect(0, 0, 401, 71))
        self.pushButton_CreatNewTask.setFont(font)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_3.addWidget(self.scrollArea)

        self.verticalScrollBar = QScrollBar(self.layoutWidget)
        self.verticalScrollBar.setObjectName(u"verticalScrollBar")
        self.verticalScrollBar.setOrientation(Qt.Vertical)

        self.horizontalLayout_3.addWidget(self.verticalScrollBar)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_StopAll = QPushButton(self.layoutWidget)
        self.pushButton_StopAll.setObjectName(u"pushButton_StopAll")
        self.pushButton_StopAll.setFont(font1)

        self.horizontalLayout_2.addWidget(self.pushButton_StopAll)

        self.pushButton_Export = QPushButton(self.layoutWidget)
        self.pushButton_Export.setObjectName(u"pushButton_Export")
        self.pushButton_Export.setFont(font1)

        self.horizontalLayout_2.addWidget(self.pushButton_Export)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_username.setText(QCoreApplication.translate("Dialog", u"Username", None))
        self.pushButton_Sort.setText(QCoreApplication.translate("Dialog", u"Sort", None))
        self.pushButton_Settings.setText(QCoreApplication.translate("Dialog", u"Settings", None))
        self.pushButton_CreatNewTask.setText(QCoreApplication.translate("Dialog", u"+ Create new task", None))
        self.pushButton_StopAll.setText(QCoreApplication.translate("Dialog", u"Stop all tasks", None))
        self.pushButton_Export.setText(QCoreApplication.translate("Dialog", u"Export Project", None))
    # retranslateUi

