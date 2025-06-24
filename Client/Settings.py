# This Python file uses the following encoding: utf-8
import os
import json
import resources
import requests

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QInputDialog, QTableWidgetItem
from PySide6.QtCore import QFile, QIODevice, Qt, QSettings, QUrl, QTranslator, QCoreApplication
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QDesktopServices

class Settings:
    def __init__(self, app, window):
        self.window = window
        self.qsettings = QSettings("Margarina", "MargarinaWikiDesktop")
        self.qshistory = QSettings("Margarina", "MargarinaWikiDesktopHistory")
        self.initialize_settings()
        self.reload_settings()
        self.selectionMode = self.defToSelectionMode
        self.translator = QTranslator(app)
        self.translator.load(self.language)
        app.installTranslator(self.translator)
        self.window.retranslate_ui()
        self.constants = self.get_constants()
        self.version = self.constants.get("version")
        pass

    def reload_settings(self):
        self.favorites = self.load_favorites()
        self.wikiAddress = QUrl(self.qsettings.value("settings/wikiAddress", type=str))
        self.searchAddress = QUrl(self.qsettings.value("settings/searchAddress", type=str))
        self.language = self.qsettings.value("settings/language", None)
        self.zoom = float(self.qsettings.value("settings/zoom", None))
        self.externalLinks = self.qsettings.value("settings/externalLinks", None)
        self.customJavaScript = self.qsettings.value("settings/customJavaScript", None)
        self.keyCombos = self.qsettings.value("settings/keyCombos", None)
        self.defToSelectionMode = self.qsettings.value("settings/defToSelectionMode", None)
        self.saveHistory = self.get_boolean_from_config(self.qsettings.value("settings/saveHistory", None))
        self.history = self.qshistory.value("history", [], type=list)
        self.historyMaxEntries = self.qsettings.value("settings/historyMaxEntries", 0, int)

    def load_favorites(self):
        favorites_json = self.qsettings.value("settings/favorites", "[]")
        return json.loads(favorites_json)

    def initialize_settings(self):
        default_settings = {
            "wikiAddress": "http://margarina.rf.gd/mediawiki/index.php/",
            "searchAddress": "http://margarina.rf.gd/mediawiki/index.php?search=",
            "key_combos": "[\n    {\n        \"title\": \"Bold\",\n        \"key_combination\": \"Ctrl+B\",\n        \"js_code\": \"_around(\\\"\\\\'\\\\'\\\\'\\\", \\\"\\\\'\\\\'\\\\'\\\");\"\n    },\n    {\n        \"title\": \"Italic\",\n        \"key_combination\": \"Ctrl+I\",\n        \"js_code\": \"_around(\\\"\\\\'\\\\'\\\", \\\"\\\\'\\\\'\\\");\"\n    },\n    {\n        \"title\": \"Heading\",\n        \"key_combination\": \"Ctrl+H\",\n        \"js_code\": \"i = prompt(\\\"Heading level\\\"); if (_isNumeric(i)) { _mwHeading(i); }\"\n    },\n    {\n        \"title\": \"List\",\n        \"key_combination\": \"Ctrl+L\",\n        \"js_code\": \"_around(\\\"* \\\",\\\"\\\");\"\n    },\n    {\n        \"title\": \"Numbered List\",\n        \"key_combination\": \"Ctrl+Alt+L\",\n        \"js_code\": \"_around(\\\"# \\\", \\\"\\\");\"\n    },\n    {\n        \"title\": \"Preformatted text block\",\n        \"key_combination\": \"Ctrl+P\",\n        \"js_code\": \"_around(\\\"<nowiki>\\\", \\\"</nowiki>\\\");\"\n    },\n    {\n        \"title\": \"Code\",\n        \"key_combination\": \"Ctrl+U\",\n        \"js_code\": \"_around(\\\"<code>\\\", \\\"</code>\\\");\"\n    },\n    {\n        \"title\": \"Quote\",\n        \"key_combination\": \"Ctrl+J\",\n        \"js_code\": \"_around(\\\"<q>\\\", \\\"</q>\\\");\"\n    },\n    {\n        \"title\": \"Blockquote\",\n        \"key_combination\": \"Ctrl+Shift+J\",\n        \"js_code\": \"_around(\\\"<blockquote>\\\", \\\"</blockquote>\\\");\"\n    },\n    {\n        \"title\": \"Comment\",\n        \"key_combination\": \"Ctrl+/\",\n        \"js_code\": \"_around(\\\"<!-- \\\", \\\" -->\\\");\"\n    }\n]",
            "language": ":/translations/en.qm",
            "customJavaScript" : "let i;",
            "favorites": "[]",
            "externalLinks": "true",
            "defToSelectionMode" : "false",
            "zoom": "1.00",
            "saveHistory" : "false",
            "historyMaxEntries" : "50"
        }
        for name, value in default_settings.items():
            if self.qsettings.value(f"settings/{name}") is None:
                self.qsettings.setValue(f"settings/{name}", value)

    def change_setting(self, setting, value):
        self.qsettings.setValue(f"settings/{setting}", value)
        self.reload_settings()

    def add_to_history(self, address):
        if not self.history or self.history[-1] != address:
            if len(self.history) >= self.historyMaxEntries:
                self.history.pop(0)
            self.history.append(address)

    def save_settings(self):
        self.qsettings.setValue("settings/wikiAddress", self.wikiAddress)
        self.qsettings.setValue("settings/searchAddress", self.searchAddress)
        self.qsettings.setValue("settings/zoom", self.zoom)
        self.qsettings.setValue("settings/language", self.language)
        self.qsettings.setValue("settings/externalLinks", self.externalLinks)
        self.qsettings.setValue("settings/wiki", self.wikiAddress)
        self.qsettings.setValue("settings/customJavaScript", self.customJavaScript)
        self.qsettings.setValue("settings/key_combos", self.keyCombos)
        self.qsettings.setValue("settings/defToSelectionMode", self.defToSelectionMode)
        self.qsettings.setValue("settings/saveHistory", self.saveHistory)
        self.qsettings.setValue("settings/historyMaxEntries", self.historyMaxEntries)

    def get_constants(self):
        file = QFile(":constants.json")
        file.open(QIODevice.ReadOnly)
        json_data = file.readAll()
        json_string = str(json_data, encoding='utf-8')
        const = json.loads(json_string)
        file.close()
        return const

    def open_settings(self):
        loader = QUiLoader()
        settings_path = os.path.join(os.path.dirname(__file__), 'settings.ui')
        settings_dialog = loader.load(settings_path)

        versiontxt = QCoreApplication.translate("Settings", "Versão: ")
        settings_dialog.lbVersion.setText(f"{versiontxt}{self.version}")

        # External links
        settings_dialog.checkExternalLinks.setCheckState(self.get_checkbox_state(self.externalLinks))
        settings_dialog.checkExternalLinks.stateChanged.connect(lambda state: self.change_setting("externalLinks", state == 2))

        # Selection mode
        settings_dialog.checkSelectionMode.setCheckState(self.get_checkbox_state(self.defToSelectionMode))
        settings_dialog.checkSelectionMode.stateChanged.connect(lambda state: self.change_setting("defToSelectionMode", state == 2))

        # saveHistory
        settings_dialog.checkHistory.setChecked(self.saveHistory)
        settings_dialog.checkHistory.stateChanged.connect(lambda state: self.change_setting("saveHistory", state == 2))

        # wikiAddress
        settings_dialog.leWikiAddress.setText(self.wikiAddress.toString())
        settings_dialog.leWikiAddress.editingFinished.connect(lambda: self.change_setting("wikiAddress", settings_dialog.leWikiAddress.text()))

        # searchAddress
        settings_dialog.leSearchAddress.setText(self.searchAddress.toString())
        settings_dialog.leSearchAddress.editingFinished.connect(lambda: self.change_setting("searchAddress", settings_dialog.leSearchAddress.text()))

        # customJavaScript
        settings_dialog.pteCustomJS.appendPlainText(self.customJavaScript)
        settings_dialog.pteCustomJS.textChanged.connect(lambda: self.change_setting("customJavaScript", settings_dialog.pteCustomJS.toPlainText()))

        # Favorites
        for favorite in self.favorites:
            settings_dialog.lwFavorites.addItem(favorite)

        settings_dialog.btnFavoritesDelete.clicked.connect(lambda: remove_favorite())
        settings_dialog.btnFavoritesAdd.clicked.connect(lambda: add_favorite())
        settings_dialog.btnFavoritesEdit.clicked.connect(lambda: edit_favorite())
        settings_dialog.btnUpdater.clicked.connect(lambda: search_for_updates())

        # zoom
        settings_dialog.dsZoomFactor.setValue(self.zoom)
        settings_dialog.dsZoomFactor.valueChanged.connect(lambda: self.change_setting("zoom", settings_dialog.dsZoomFactor.value()))

        # functions

        def remove_favorite():
            settings_dialog.lwFavorites.takeItem(settings_dialog.lwFavorites.row(settings_dialog.lwFavorites.currentItem()))
            save_favorites_to_settings()

        def add_favorite(suggestion = ""):
            input , ok= self.ask_for_input(self,
            QCoreApplication.translate("Settings", "Adicionar favorito"),
            QCoreApplication.translate("Settings", "Por favor, digite endereço da página:"))
            if input and ok:
                settings_dialog.lwFavorites.addItem(input)
                save_favorites_to_settings()

        def edit_favorite(suggestion = ""):
            input , ok= self.ask_for_input(self,
            QCoreApplication.translate("Settings", "Editar favorito"),
            QCoreApplication.translate("Settings", "Por favor, digite o novo endereço da página:"))
            if input and ok:
                settings_dialog.lwFavorites.currentItem().setText(input)
                save_favorites_to_settings()


        def save_favorites_to_settings():
            favorites = []
            for index in range(settings_dialog.lwFavorites.count()):
                item = settings_dialog.lwFavorites.item(index)
                if item is not None:
                    favorites.append(item.text())

            favorites_json = json.dumps(favorites)
            self.qsettings.setValue("settings/favorites", favorites_json)
            self.load_favorites()

        languages = {
            ":/translations/portuguese.qm": "Português",
            ":/translations/english.qm": "English",
            ":/translations/japanese.qm": "Japanese"
        }

        for path, lang in languages.items():
            settings_dialog.cbLanguage.addItem(lang, path)

        current_language = self.qsettings.value("settings/language", None)

        if current_language:
            index = settings_dialog.cbLanguage.findData(current_language)
            if index != -1:
                settings_dialog.cbLanguage.setCurrentIndex(index)

        def change_language(index):
            language_path = settings_dialog.cbLanguage.itemData(index)
            if language_path and self.translator.load(language_path):
                self.change_setting("language", language_path)
                QApplication.instance().installTranslator(self.translator)
                self.window.retranslate_ui()
            else:
                print(f"Translation file for {language_path} not found.")

        settings_dialog.cbLanguage.currentIndexChanged.connect(change_language)

        settings_dialog.pbKeyCombosDelete.clicked.connect(lambda: remove_key_combo())
        settings_dialog.pbKeyCombosAdd.clicked.connect(lambda: add_key_combo())
        settings_dialog.pbKeyCombosEdit.clicked.connect(lambda: edit_key_combo())

        def remove_key_combo():
            current_row = settings_dialog.twKeyCombos.currentRow()
            if current_row >= 0:  # Check if a row is selected
                settings_dialog.twKeyCombos.removeRow(current_row)
                save_key_combos_to_settings()

        def add_key_combo():
            title, ok1 = self.ask_for_input(
                "Settings",  # Use a string for context
                QCoreApplication.translate("Settings", "Adicionar combinação de teclas"),
                QCoreApplication.translate("Settings", "Por favor, digite o título:")
            )

            key_combination, ok2 = self.ask_for_input(
                "Settings",  # Use a string for context
                QCoreApplication.translate("Settings", "Adicionar combinação de teclas"),
                QCoreApplication.translate("Settings", "Por favor, digite a combinação:")
            )

            js_code, ok3 = self.ask_for_input(
                "Settings",  # Use a string for context
                QCoreApplication.translate("Settings", "Adicionar combinação de teclas"),
                QCoreApplication.translate("Settings", "Por favor, digite o código JavaScript:")
            )

            if ok1 and ok2 and ok3:
                row_position = settings_dialog.twKeyCombos.rowCount()
                settings_dialog.twKeyCombos.insertRow(row_position)
                settings_dialog.twKeyCombos.setItem(row_position, 0, QTableWidgetItem(title))
                settings_dialog.twKeyCombos.setItem(row_position, 1, QTableWidgetItem(key_combination))
                settings_dialog.twKeyCombos.setItem(row_position, 2, QTableWidgetItem(js_code))
                save_key_combos_to_settings()

        def edit_key_combo():
            current_row = settings_dialog.twKeyCombos.currentRow()
            if current_row >= 0:  # Check if a row is selected
                title, ok1 = self.ask_for_input(self,
                                            QCoreApplication.translate("Settings", "Editar combinação de teclas"),
                                            QCoreApplication.translate("Settings", "Por favor, digite o novo título:"),
                                            settings_dialog.twKeyCombos.item(current_row, 0).text())
                key_combination, ok2 = self.ask_for_input(self,
                                            QCoreApplication.translate("Settings", "Editar combinação de teclas"),
                                            QCoreApplication.translate("Settings", "Por favor, digite a nova combinação:"),
                                                      settings_dialog.twKeyCombos.item(current_row, 1).text())
                js_code, ok3 = self.ask_for_input(self,
                                            QCoreApplication.translate("Settings", "Editar combinação de teclas"),
                                            QCoreApplication.translate("Settings", "Por favor, digite o novo código JavaScript:"),
                                              settings_dialog.twKeyCombos.item(current_row, 2).text())

                if ok1 and ok2 and ok3:
                    settings_dialog.twKeyCombos.item(current_row, 0).setText(title)
                    settings_dialog.twKeyCombos.item(current_row, 1).setText(key_combination)
                    settings_dialog.twKeyCombos.item(current_row, 2).setText(js_code)
                    save_key_combos_to_settings()

        def save_key_combos_to_settings():
            key_combos = []
            for row in range(settings_dialog.twKeyCombos.rowCount()):
                title = settings_dialog.twKeyCombos.item(row, 0).text() if settings_dialog.twKeyCombos.item(row, 0) else ""
                key_combination = settings_dialog.twKeyCombos.item(row, 1).text() if settings_dialog.twKeyCombos.item(row, 1) else ""
                js_code = settings_dialog.twKeyCombos.item(row, 2).text() if settings_dialog.twKeyCombos.item(row, 2) else ""
                key_combos.append({"title": title, "key_combination": key_combination, "js_code": js_code})

            key_combos_json = json.dumps(key_combos, indent=4)
            self.change_setting("key_combos", key_combos_json)
            load_key_combos()

        def load_key_combos():
            key_combos_json = self.qsettings.value("settings/key_combos", "[]")
            key_combos = json.loads(key_combos_json)

            settings_dialog.twKeyCombos.setRowCount(0)

            for combo in key_combos:
                row_position = settings_dialog.twKeyCombos.rowCount()
                settings_dialog.twKeyCombos.insertRow(row_position)
                settings_dialog.twKeyCombos.setItem(row_position, 0, QTableWidgetItem(combo.get("title", "")))
                settings_dialog.twKeyCombos.setItem(row_position, 1, QTableWidgetItem(combo.get("key_combination", "")))
                settings_dialog.twKeyCombos.setItem(row_position, 2, QTableWidgetItem(combo.get("js_code", "")))

        def search_for_updates():
            latest_version, download_url = get_latest_release()
            if latest_version and download_url:
                if latest_version != self.version:
                    if show_alert(
                        QCoreApplication.translate("Settings", "Deseja atualizar?"),
                        f"{QCoreApplication.translate('Settings', 'Uma nova versão desta aplicação foi encontrada:')} {latest_version}",
                        QMessageBox.Ok | QMessageBox.Cancel,
                        QMessageBox.Information
                    ):
                        QDesktopServices.openUrl(self.constants.get("update_link"))
                else:
                    show_alert(
                        QCoreApplication.translate("Settings", "Atualizações"),
                        QCoreApplication.translate("Settings", "Nenhuma atualização foi encontrada."),
                        QMessageBox.Ok,
                        QMessageBox.Information
                    )

        def get_latest_release():
            url = self.constants.get("update_repo")
            response = requests.get(url)
            if response.status_code == 200:
                release_data = response.json()
                latest_version = release_data['tag_name']
                download_url = release_data['assets'][0]['browser_download_url']
                return latest_version, download_url
            else:
                return None, None

        def show_alert(title, text, buttons = QMessageBox.Ok, icon = QMessageBox.Information):
            msg_box = QMessageBox()
            msg_box.setWindowTitle(title)
            msg_box.setText(text)
            msg_box.setIcon(icon)
            msg_box.setStandardButtons(buttons)
            return msg_box.exec()

        load_key_combos()
        settings_dialog.exec()

    def ask_for_input(self, context, title, info, suggestion=""):
        result = QInputDialog.getText(self.window, title, info, text=suggestion)
        return result

    def read_from_resources(self, path):
        file = QFile(path)
        if file.open(QIODevice.ReadOnly | QIODevice.Text):
            text = file.readAll().data().decode('utf-8')
            file.close()
            return text
        else:
            print("Failed to open the file.")
            return None


    def get_boolean_from_config(self, string):
        if str(string).lower() == 'true':
            return True
        else:
            return False

    def get_checkbox_state(self, string):
        if string is None:
            return Qt.Unchecked
        if string.lower() == 'true':
            return Qt.Checked
        elif string.lower() == 'false':
            return Qt.Unchecked
        else:
            try:
                return int(string)
            except ValueError:
                return Qt.Unchecked

    def settings_to_json(settings):
        settings_dict = {}
        for key in settings.allKeys():
            settings_dict[key] = settings.value(key)
        return json.dumps(settings_dict, indent=4)
