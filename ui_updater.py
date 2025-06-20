# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'updater.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QPushButton,
    QSizePolicy, QSpacerItem, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        self.horizontalLayout_2 = QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.teUpdater = QTextEdit(Dialog)
        self.teUpdater.setObjectName(u"teUpdater")

        self.horizontalLayout_2.addWidget(self.teUpdater)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.btnUpdate = QPushButton(Dialog)
        self.btnUpdate.setObjectName(u"btnUpdate")
        self.btnUpdate.setEnabled(False)

        self.verticalLayout.addWidget(self.btnUpdate)

        self.btnSearch = QPushButton(Dialog)
        self.btnSearch.setObjectName(u"btnSearch")

        self.verticalLayout.addWidget(self.btnSearch)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.btnUpdate.setText(QCoreApplication.translate("Dialog", u"Atualizar", None))
        self.btnSearch.setText(QCoreApplication.translate("Dialog", u"Buscar", None))
    # retranslateUi

