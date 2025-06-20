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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QDialog, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(370, 857)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen))
        Dialog.setWindowIcon(icon)
        Dialog.setWindowOpacity(0.900000000000000)
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

        self.lbSearchAddress = QLabel(Dialog)
        self.lbSearchAddress.setObjectName(u"lbSearchAddress")

        self.verticalLayout.addWidget(self.lbSearchAddress)

        self.leSearchAddress = QLineEdit(Dialog)
        self.leSearchAddress.setObjectName(u"leSearchAddress")

        self.verticalLayout.addWidget(self.leSearchAddress)

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

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.labelCustomJS = QLabel(Dialog)
        self.labelCustomJS.setObjectName(u"labelCustomJS")

        self.verticalLayout.addWidget(self.labelCustomJS)

        self.pteCustomJS = QPlainTextEdit(Dialog)
        self.pteCustomJS.setObjectName(u"pteCustomJS")

        self.verticalLayout.addWidget(self.pteCustomJS)

        self.lbKeyCombos = QLabel(Dialog)
        self.lbKeyCombos.setObjectName(u"lbKeyCombos")

        self.verticalLayout.addWidget(self.lbKeyCombos)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.twKeyCombos = QTableWidget(Dialog)
        if (self.twKeyCombos.columnCount() < 3):
            self.twKeyCombos.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.twKeyCombos.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.twKeyCombos.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.twKeyCombos.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.twKeyCombos.setObjectName(u"twKeyCombos")
        self.twKeyCombos.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.twKeyCombos.sizePolicy().hasHeightForWidth())
        self.twKeyCombos.setSizePolicy(sizePolicy1)
        self.twKeyCombos.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.twKeyCombos.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.twKeyCombos.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.horizontalLayout_3.addWidget(self.twKeyCombos)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.pbKeyCombosDelete = QPushButton(Dialog)
        self.pbKeyCombosDelete.setObjectName(u"pbKeyCombosDelete")

        self.verticalLayout_4.addWidget(self.pbKeyCombosDelete)

        self.pbKeyCombosAdd = QPushButton(Dialog)
        self.pbKeyCombosAdd.setObjectName(u"pbKeyCombosAdd")

        self.verticalLayout_4.addWidget(self.pbKeyCombosAdd)

        self.pbKeyCombosEdit = QPushButton(Dialog)
        self.pbKeyCombosEdit.setObjectName(u"pbKeyCombosEdit")

        self.verticalLayout_4.addWidget(self.pbKeyCombosEdit)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_4)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lbVersion = QLabel(Dialog)
        self.lbVersion.setObjectName(u"lbVersion")

        self.horizontalLayout_2.addWidget(self.lbVersion)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.btnUpdater = QPushButton(Dialog)
        self.btnUpdater.setObjectName(u"btnUpdater")

        self.horizontalLayout_2.addWidget(self.btnUpdater)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Configura\u00e7\u00f5es", None))
        self.labelLanguage.setText(QCoreApplication.translate("Dialog", u"Idioma", None))
        self.checkExternalLinks.setText(QCoreApplication.translate("Dialog", u"Abrir links externos no seu navegador.", None))
        self.labelWikiAddress.setText(QCoreApplication.translate("Dialog", u"Endere\u00e7o da wiki", None))
        self.lbSearchAddress.setText(QCoreApplication.translate("Dialog", u"Endere\u00e7o de pesquisa", None))
        self.labelBookmarks.setText(QCoreApplication.translate("Dialog", u"Favoritos", None))
        self.btnFavoritesDelete.setText(QCoreApplication.translate("Dialog", u"Deletar", None))
        self.btnFavoritesAdd.setText(QCoreApplication.translate("Dialog", u"Adicionar", None))
        self.btnFavoritesEdit.setText(QCoreApplication.translate("Dialog", u"Editar", None))
        self.labelCustomJS.setText(QCoreApplication.translate("Dialog", u"JavaScript customizado", None))
        self.lbKeyCombos.setText(QCoreApplication.translate("Dialog", u"Atalhos do teclado", None))
        ___qtablewidgetitem = self.twKeyCombos.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Nome", None));
        ___qtablewidgetitem1 = self.twKeyCombos.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Combina\u00e7\u00e3o", None));
        ___qtablewidgetitem2 = self.twKeyCombos.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"C\u00f3digo", None));
        self.pbKeyCombosDelete.setText(QCoreApplication.translate("Dialog", u"Deletar", None))
        self.pbKeyCombosAdd.setText(QCoreApplication.translate("Dialog", u"Adicionar", None))
        self.pbKeyCombosEdit.setText(QCoreApplication.translate("Dialog", u"Editar", None))
        self.lbVersion.setText("")
        self.btnUpdater.setText(QCoreApplication.translate("Dialog", u"Atualiza\u00e7\u00f5es", None))
    # retranslateUi

