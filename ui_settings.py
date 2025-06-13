# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPlainTextEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(364, 377)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen))
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelLanguage = QLabel(Dialog)
        self.labelLanguage.setObjectName(u"labelLanguage")
        self.labelLanguage.setLocale(QLocale(QLocale.Portuguese, QLocale.Brazil))

        self.verticalLayout.addWidget(self.labelLanguage)

        self.cbLanguage = QComboBox(Dialog)
        self.cbLanguage.setObjectName(u"cbLanguage")
        self.cbLanguage.setLocale(QLocale(QLocale.Portuguese, QLocale.Brazil))

        self.verticalLayout.addWidget(self.cbLanguage)

        self.checkExternalLinks = QCheckBox(Dialog)
        self.checkExternalLinks.setObjectName(u"checkExternalLinks")
        self.checkExternalLinks.setLocale(QLocale(QLocale.Portuguese, QLocale.Brazil))

        self.verticalLayout.addWidget(self.checkExternalLinks)

        self.labelWikiAddress = QLabel(Dialog)
        self.labelWikiAddress.setObjectName(u"labelWikiAddress")
        self.labelWikiAddress.setLocale(QLocale(QLocale.Portuguese, QLocale.Brazil))

        self.verticalLayout.addWidget(self.labelWikiAddress)

        self.leWikiAddress = QLineEdit(Dialog)
        self.leWikiAddress.setObjectName(u"leWikiAddress")
        self.leWikiAddress.setLocale(QLocale(QLocale.Portuguese, QLocale.Brazil))

        self.verticalLayout.addWidget(self.leWikiAddress)

        self.labelBookmarks = QLabel(Dialog)
        self.labelBookmarks.setObjectName(u"labelBookmarks")
        self.labelBookmarks.setLocale(QLocale(QLocale.Portuguese, QLocale.Brazil))

        self.verticalLayout.addWidget(self.labelBookmarks)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lwFavorites = QListWidget(Dialog)
        self.lwFavorites.setObjectName(u"lwFavorites")
        self.lwFavorites.setLocale(QLocale(QLocale.Portuguese, QLocale.Brazil))

        self.horizontalLayout.addWidget(self.lwFavorites)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.btnFavoritesDelete = QPushButton(Dialog)
        self.btnFavoritesDelete.setObjectName(u"btnFavoritesDelete")
        self.btnFavoritesDelete.setLocale(QLocale(QLocale.Portuguese, QLocale.Brazil))

        self.verticalLayout_2.addWidget(self.btnFavoritesDelete)

        self.btnFavoritesAdd = QPushButton(Dialog)
        self.btnFavoritesAdd.setObjectName(u"btnFavoritesAdd")
        self.btnFavoritesAdd.setLocale(QLocale(QLocale.Portuguese, QLocale.Brazil))

        self.verticalLayout_2.addWidget(self.btnFavoritesAdd)

        self.btnFavoritesEdit = QPushButton(Dialog)
        self.btnFavoritesEdit.setObjectName(u"btnFavoritesEdit")
        self.btnFavoritesEdit.setLocale(QLocale(QLocale.Portuguese, QLocale.Brazil))

        self.verticalLayout_2.addWidget(self.btnFavoritesEdit)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.labelCustomJS = QLabel(Dialog)
        self.labelCustomJS.setObjectName(u"labelCustomJS")

        self.verticalLayout.addWidget(self.labelCustomJS)

        self.pteCustomJS = QPlainTextEdit(Dialog)
        self.pteCustomJS.setObjectName(u"pteCustomJS")

        self.verticalLayout.addWidget(self.pteCustomJS)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Configura\u00e7\u00f5es", None))
        self.labelLanguage.setText(QCoreApplication.translate("Dialog", u"Idioma", None))
        self.checkExternalLinks.setText(QCoreApplication.translate("Dialog", u"Abrir links externos no seu navegador.", None))
        self.labelWikiAddress.setText(QCoreApplication.translate("Dialog", u"Endere\u00e7o da wiki", None))
        self.labelBookmarks.setText(QCoreApplication.translate("Dialog", u"Favoritos", None))
        self.btnFavoritesDelete.setText(QCoreApplication.translate("Dialog", u"Deletar", None))
        self.btnFavoritesAdd.setText(QCoreApplication.translate("Dialog", u"Adicionar", None))
        self.btnFavoritesEdit.setText(QCoreApplication.translate("Dialog", u"Editar", None))
        self.labelCustomJS.setText(QCoreApplication.translate("Dialog", u"JavaScript customizado", None))
    # retranslateUi

