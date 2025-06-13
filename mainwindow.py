# This Python file uses the following encoding: utf-8
import sys
import os
import json
import logging
import resources

from PySide6.QtWidgets import QApplication, QMainWindow, QInputDialog
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QUrl, QSettings, Qt, QTranslator
from PySide6.QtGui import QDesktopServices, QAction, QIcon

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

settings = QSettings("Margarina", "MargarinaWikiDesktop")
wikiAddress = QUrl(settings.value("settings/wikiAddress", type=str, defaultValue="https://www.dokuwiki.org/dokuwiki"))
favorites = []

def load_favorites():
    favorites_json = settings.value("settings/favorites", "[]")
    global favorites
    try:
        favorites = json.loads(favorites_json)
    except json.JSONDecodeError as e:
        logging.error(e)

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)

    def acceptNavigationRequest(self, url: QUrl, isMainFrame: bool, action: QWebEnginePage.NavigationType) -> bool:
        my_domain = "margarina.rf.gd"

        if my_domain not in url.host() and settings.value("settings/externalLinks") == True:
            QDesktopServices.openUrl(url)
            return False
        return True

class CustomWebEngineView(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)

        cookie_storage_path = os.path.join(os.path.expanduser("~"), ".margarinawiki_desktop")

        self.profile = QWebEngineProfile("MargarinaProfile", self)
        self.profile.setPersistentStoragePath(cookie_storage_path)

        self.setPage(CustomWebEnginePage(self.profile, self))

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(":logo.png"))
        self.initialize_settings()
        load_favorites()

        settingsLang = settings.value("settings/language", None)
        self.translator = QTranslator(app)

        self.translator.load(settingsLang)

        app.installTranslator(self.translator)
        self.retranslate_ui()

        self.webEngineView = CustomWebEngineView(self)
        self.setCentralWidget(self.webEngineView)
        self.webEngineView.setStyleSheet("""
        background-color: #000;
        color: #fff;
        """)
        self.webEngineView.setUrl(wikiAddress)

        self.webEngineView.loadFinished.connect(self.inject_scrollbar_styles)

        favCount = 0
        #Loading favorites
        for favorite in favorites:
            favCount += 1
            action = QAction(favorite, self)
            action.setShortcut(f"Ctrl+Shift+{favCount}")
            action.triggered.connect(lambda: self.webEngineView.setUrl(f"{wikiAddress.toString()}/doku.php?id={favorite}"))
            self.ui.menuWiki.addAction(action)


        #actionSair
        self.ui.actionSair.triggered.connect(self.exit_application)
        self.ui.actionSair.setShortcut('Ctrl+Q')

        #actionItalico
        self.ui.actionItalico.triggered.connect(lambda: self.paste_text("//"))
        self.ui.actionItalico.setShortcut('Ctrl+I')

        #actionSublinhado
        self.ui.actionSublinhado.triggered.connect(lambda: self.paste_text("__"))
        self.ui.actionSublinhado.setShortcut('Ctrl+U')

        #actionC_digo
        self.ui.actionC_digo.triggered.connect(lambda: self.paste_text("''"))
        self.ui.actionC_digo.setShortcut('Ctrl+M')

        #actionNegrito
        self.ui.actionNegrito.triggered.connect(lambda: self.paste_text("**"))
        self.ui.actionNegrito.setShortcut('Ctrl+B')

        #actionSobre
        self.ui.actionSobre.triggered.connect(lambda: self.webEngineView.page().runJavaScript("alert('MargarinaWiki Desktop, feito por Adrian Victor.')"))
        self.ui.actionSobre.setShortcut('Alt+A')

        #actionSele_o
        self.ui.actionSele_o.triggered.connect(lambda: self.webEngineView.page().runJavaScript("document.querySelector('body').style.userSelect = 'text'"))
        self.ui.actionSele_o.setShortcut('Ctrl+S')

        #actionNavega_o
        self.ui.actionNavega_o.triggered.connect(lambda: self.webEngineView.page().runJavaScript("document.querySelector('body').style.userSelect = 'none'"))
        self.ui.actionNavega_o.setShortcut('Ctrl+W')

        #actionC_digo_bloco
        self.ui.actionC_digo_bloco.triggered.connect(lambda: self.paste_text("<code>", "</code>"))
        self.ui.actionC_digo_bloco.setShortcut('Ctrl+Shift+M')

        #actionC_digo_bloco
        self.ui.actionC_digo_bloco.triggered.connect(lambda: self.paste_text("<code>", "</code>"))
        self.ui.actionC_digo_bloco.setShortcut('Ctrl+Shift+M')

        #actionMesmo_nivel
        self.ui.actionMesmo_nivel.triggered.connect(lambda: self.click(8))
        self.ui.actionMesmo_nivel.setShortcut('Alt+1')

        #actionNivel_abaixo
        self.ui.actionNivel_abaixo.triggered.connect(lambda: self.click(9))
        self.ui.actionNivel_abaixo.setShortcut('Alt+2')

        #actionNivel_acima
        self.ui.actionNivel_acima.triggered.connect(lambda: self.click(0))
        self.ui.actionNivel_acima.setShortcut('Alt+3')

        #actionInterno_2
        self.ui.actionInterno_2.triggered.connect(lambda: self.click("l"))
        self.ui.actionInterno_2.setShortcut('Ctrl+L')

        #actionExterno
        self.ui.actionExterno.triggered.connect(lambda: self.paste_text("[[http://example.com|", "]]"))
        self.ui.actionExterno.setShortcut('Ctrl+Shift+L')

        #action1
        self.ui.action1.triggered.connect(lambda: self.paste_text("###### ", " ######"))
        self.ui.action1.setShortcut('Alt+Shift+1')

        #action2
        self.ui.action2.triggered.connect(lambda: self.paste_text("##### ", " #####"))
        self.ui.action2.setShortcut('Alt+Shift+2')

        #action3
        self.ui.action3.triggered.connect(lambda: self.paste_text("#### ", " ####"))
        self.ui.action3.setShortcut('Alt+Shift+3')

        #action4
        self.ui.action4.triggered.connect(lambda: self.paste_text("#### ", " ####"))
        self.ui.action4.setShortcut('Alt+Shift+4')

        #action5
        self.ui.action5.triggered.connect(lambda: self.paste_text("### ", " ###"))
        self.ui.action5.setShortcut('Alt+Shift+5')

        #action6
        self.ui.action6.triggered.connect(lambda: self.paste_text("## ", " ##"))
        self.ui.action6.setShortcut('Alt+Shift+6')

        #actionPrefer_ncias
        self.ui.actionPrefer_ncias.triggered.connect(self.open_settings)
        self.ui.actionPrefer_ncias.setShortcut('Alt+P')

        #actionOp_es_de_desesnvolvedor
        self.ui.actionOp_es_de_desenvolvedor.triggered.connect(lambda: self.webEngineView.page().runJavaScript(
            """
            (function () {
                var script = document.createElement('script');
                script.src = '//cdn.jsdelivr.net/npm/eruda';
                document.body.appendChild(script);
                script.onload = function () { eruda.init(); };
            })();
            """
        ))
        self.ui.actionOp_es_de_desenvolvedor.setShortcut('Ctrl+Shift+C')

        # Connect the webEngineView signal to hide the QWebEngineView
        self.webEngineView.loadStarted.connect(lambda: self.webEngineView.setVisible(False))
        self.webEngineView.loadFinished.connect(lambda: self.webEngineView.setVisible(True))

        # Connecting webview to statusbar
        self.webEngineView.loadStarted.connect(self.on_load_started)
        self.webEngineView.loadFinished.connect(self.on_load_finished)

    def retranslate_ui(self):
        self.ui.retranslateUi(self)

    def open_settings(self):
        loader = QUiLoader()
        settings_path = os.path.join(os.path.dirname(__file__), 'settings.ui')
        settings_dialog = loader.load(settings_path)

        settings_dialog.checkExternalLinks.setCheckState(self.get_checkbox_state_config("externalLinks"))
        settings_dialog.checkExternalLinks.stateChanged.connect(lambda state: settings.setValue("settings/externalLinks", state == 2))

        settings_dialog.leWikiAddress.setText(settings.value("settings/wikiAddress", type=str, defaultValue=""))
        settings_dialog.leWikiAddress.editingFinished.connect(lambda: settings.setValue("settings/wikiAddress", settings_dialog.leWikiAddress.text()))

        settings_dialog.pteCustomJS.appendPlainText(settings.value("settings/customJavaScript", type=str, defaultValue=""))
        settings_dialog.pteCustomJS.textChanged.connect(lambda: settings.setValue("settings/customJavaScript", settings_dialog.pteCustomJS.toPlainText()))

        for favorite in favorites:
            settings_dialog.lwFavorites.addItem(favorite)

        settings_dialog.btnFavoritesDelete.clicked.connect(lambda: remove_favorite())
        settings_dialog.btnFavoritesAdd.clicked.connect(lambda: add_favorite())
        settings_dialog.btnFavoritesEdit.clicked.connect(lambda: edit_favorite())

        def remove_favorite():
            settings_dialog.lwFavorites.takeItem(settings_dialog.lwFavorites.row(settings_dialog.lwFavorites.currentItem()))
            save_favorites_to_settings()

        def add_favorite(suggestion = ""):
            input , ok= self.ask_for_input("Adicionar favorito", "Por favor, insira o endereço da página:")
            if input and ok:
                settings_dialog.lwFavorites.addItem(input)
                save_favorites_to_settings()

        def edit_favorite(suggestion = ""):
            input , ok= self.ask_for_input("Editar favorito", "Por favor, insira o novo endereço:")
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
            settings.setValue("settings/favorites", favorites_json)
            load_favorites()

        languages = {
            ":/translations/pt.qm": "Português",
            ":/translations/en.qm": "English",
            ":/translations/jp.qm": "Japanese"
        }

        for path, lang in languages.items():
            settings_dialog.cbLanguage.addItem(lang, path)

        current_language = settings.value("settings/language", None)

        if current_language:
            index = settings_dialog.cbLanguage.findData(current_language)
            if index != -1:
                settings_dialog.cbLanguage.setCurrentIndex(index)

        def change_language(index):
            language_path = settings_dialog.cbLanguage.itemData(index)
            if language_path and self.translator.load(language_path):
                settings.setValue("settings/language", language_path)
                QApplication.instance().installTranslator(self.translator)
                self.retranslate_ui()
            else:
                print(f"Translation file for {language_path} not found.")

        settings_dialog.cbLanguage.currentIndexChanged.connect(change_language)

        settings_dialog.exec()


    def get_checkbox_state_config(self, name):
        setting = settings.value(f"settings/{name}", type=str)
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


    def ask_for_input(self, title, info, suggestion = ""):
        result = QInputDialog.getText(self, title, info)
        return result

    def initialize_settings(self):
        default_settings = {
            "wikiAddress": "https://dokuwiki.org/dokuwiki",
            "language": ":/translations/en.qm",
            "favorites": "[\"main\"]",
            "externalLinks": "true"
        }
        for name, value in default_settings.items():
            if settings.value(f"settings/{name}") is None:
                settings.setValue(f"settings/{name}", value)

    def on_load_started(self):
        self.statusBar().showMessage("Loading...")

    def click(self, id):

        js_code = f'''
            document.querySelector('#tool__bar button[accesskey="{id}"]').click();
        '''
        self.webEngineView.page().runJavaScript(js_code)

    def paste_text(self, wrap_text_start, wrap_text_end = None):
        if wrap_text_end is None:
                wrap_text_end = wrap_text_start
        js_code = f'''
        var activeElement = document.activeElement;
        var wrapTextStart = "{wrap_text_start}";
        var wrapTextEnd = "{wrap_text_end}";

        if (activeElement.tagName === 'TEXTAREA' || (activeElement.tagName === 'INPUT' && activeElement.type === 'text')) {{
            var start = activeElement.selectionStart;
            var end = activeElement.selectionEnd;
            var selectedText = activeElement.value.substring(start, end);

            activeElement.value = activeElement.value.substring(0, start) + wrapTextStart + selectedText + wrapTextEnd + activeElement.value.substring(end);

            if (start === end) {{
                var newCursorPosition = start + wrapTextStart.length;
                activeElement.selectionStart = activeElement.selectionEnd = newCursorPosition;
            }} else {{
                var newCursorPosition = start + wrapTextStart.length + selectedText.length + wrapTextEnd.length;
                activeElement.selectionStart = activeElement.selectionEnd = newCursorPosition;
            }}
        }} else {{
            alert("Please focus on a textarea or input to paste the text.");
        }}
        '''
        self.webEngineView.page().runJavaScript(js_code)

    def inject_scrollbar_styles(self, success):
        if success:
            css = """
            body {
                overflow: auto;
                overflow-x: hidden;
                user-select: none;
            }
            ::-webkit-scrollbar {
                width: 12px; /* Width of the scrollbar */
            }
            ::-webkit-scrollbar-track {
                background: #1f1f1f; /* Background of the scrollbar track */
            }
            ::-webkit-scrollbar-thumb {
                background: #888; /* Color of the scrollbar thumb */
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #000; /* Color of the scrollbar thumb on hover */
            }
            """
            self.webEngineView.page().runJavaScript(f"""
            var style = document.createElement('style');
            style.innerHTML = `{css}`;
            document.head.appendChild(style);
            """)

    def on_load_finished(self, success):
        if success:
            self.statusBar().showMessage(f"Page loaded successfully. ({self.webEngineView.url})")
            self.webEngineView.page().runJavaScript(settings.value("settings/customJavaScript", type=str, defaultValue=""))
        else:
            self.statusBar().showMessage("Failed to load the page.")

    def exit_application(self):
            self.statusBar().showMessage("Exiting the application...")
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
