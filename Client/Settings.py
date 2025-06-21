# This Python file uses the following encoding: utf-8
import os
import json
import resources
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QInputDialog, QTableWidgetItem
from PySide6.QtCore import QFile, QIODevice, Qt, QSettings, QUrl, QTranslator, QCoreApplication

class Settings:
    def __init__(self, app, window):
        self.window = window
        self.qsettings = QSettings("Margarina", "MargarinaWikiDesktop")
        self.initialize_settings()
        self.reload_settings()
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
            "externalLinks": "true"
        }
        for name, value in default_settings.items():
            if self.qsettings.value(f"settings/{name}") is None:
                self.qsettings.setValue(f"settings/{name}", value)

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

        if(self.constants.get("disable_updater")):
            settings_dialog.btnUpdater.setVisible(False)
            settings_dialog.btnUpdater.deleteLater()

        versiontxt = QCoreApplication.translate("Settings", "Versão: ")
        settings_dialog.lbVersion.setText(f"{versiontxt}{self.version}")

        settings_dialog.checkExternalLinks.setCheckState(self.get_checkbox_state_config("externalLinks"))
        settings_dialog.checkExternalLinks.stateChanged.connect(lambda state: self.qsettings.setValue("settings/externalLinks", state == 2))

        settings_dialog.leWikiAddress.setText(self.qsettings.value("settings/wikiAddress", type=str, defaultValue=""))
        settings_dialog.leWikiAddress.editingFinished.connect(lambda: self.qsettings.setValue("settings/wikiAddress", settings_dialog.leWikiAddress.text()))

        settings_dialog.leSearchAddress.setText(self.qsettings.value("settings/searchAddress", type=str, defaultValue=""))
        settings_dialog.leSearchAddress.editingFinished.connect(lambda: self.qsettings.setValue("settings/searchAddress", settings_dialog.leSearchAddress.text()))

        settings_dialog.pteCustomJS.appendPlainText(self.qsettings.value("settings/customJavaScript", type=str, defaultValue=""))
        settings_dialog.pteCustomJS.textChanged.connect(lambda: self.qsettings.setValue("settings/customJavaScript", settings_dialog.pteCustomJS.toPlainText()))

        for favorite in self.favorites:
            settings_dialog.lwFavorites.addItem(favorite)

        settings_dialog.btnFavoritesDelete.clicked.connect(lambda: remove_favorite())
        settings_dialog.btnFavoritesAdd.clicked.connect(lambda: add_favorite())
        settings_dialog.btnFavoritesEdit.clicked.connect(lambda: edit_favorite())
        # updater = Updater(self.version)
        # settings_dialog.btnUpdater.clicked.connect(lambda: updater.open_updater())

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
                self.qsettings.setValue("settings/language", language_path)
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
            self.qsettings.setValue("settings/key_combos", key_combos_json)
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


    def get_checkbox_state_config(self, name):
        setting = self.qsettings.value(f"settings/{name}", type=str)
        if setting is None:
            return Qt.Unchecked
        if setting.lower() == 'true':
            return Qt.Checked
        elif setting.lower() == 'false':
            return Qt.Unchecked
        else:
            try:
                return int(setting)
            except ValueError:
                return Qt.Unchecked
