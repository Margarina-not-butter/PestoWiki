# This Python file uses the following encoding: utf-8
import sys
import os
import json
import logging

from PySide6.QtWidgets import QApplication, QMainWindow, QInputDialog, QTableWidgetItem
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QUrl, QSettings, Qt, QTranslator, QFile, QIODevice, QCoreApplication
from PySide6.QtGui import QDesktopServices, QAction, QIcon
from Settings import Settings

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)

    def acceptNavigationRequest(self, url: QUrl, isMainFrame: bool, action: QWebEnginePage.NavigationType) -> bool:
        my_domain = "margarina.rf.gd"

        if my_domain not in url.host() and settings.qsettings.value("settings/externalLinks") == True:
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

    def retranslate_ui(self):
        self.ui.retranslateUi(self)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.settings = Settings(app, self)

        self.setWindowIcon(QIcon(":logo.png"))

        self.webEngineView = CustomWebEngineView(self)
        self.setCentralWidget(self.webEngineView)
        self.webEngineView.setStyleSheet("""
        background-color: #000;
        color: #fff;
        """)
        self.webEngineView.setUrl(self.settings.wikiAddress)

        self.webEngineView.loadFinished.connect(self.inject_scrollbar_styles)

        favCount = 0

        #Loading favorites
        for favorite in self.settings.favorites:
            favCount += 1
            action = QAction(favorite, self)
            action.setShortcut(f"Ctrl+Shift+{favCount}")
            action.triggered.connect(lambda: self.webEngineView.setUrl(f"{self.settings.wikiAddress.toString()}{favorite}"))
            self.ui.menuWiki.addAction(action)

        key_combos_json = self.settings.qsettings.value("settings/key_combos", "[]")
        key_combos = json.loads(key_combos_json)
        for combo in key_combos:
            action = QAction(combo.get("title", ""), self)
            action.setShortcut(combo.get("key_combination", ""))
            action.triggered.connect(lambda checked, js_code=combo.get("js_code"): runCustomJS(js_code))
            self.ui.menuInserir.addAction(action)


        def runCustomJS(code):
            self.webEngineView.page().runJavaScript(code)

        #actionSair
        self.ui.actionSair.triggered.connect(self.exit_application)
        self.ui.actionSair.setShortcut('Ctrl+Q')

        #actionSobre
        self.ui.actionSobre.triggered.connect(lambda: self.webEngineView.page().runJavaScript("alert('MargarinaWiki Desktop, feito por Adrian Victor.')"))
        self.ui.actionSobre.setShortcut('Alt+A')

        #actionSele_o
        self.ui.actionSele_o.triggered.connect(lambda: self.webEngineView.page().runJavaScript("document.querySelector('body').style.userSelect = 'text'"))
        self.ui.actionSele_o.setShortcut('Ctrl+S')

        #actionNavega_o
        self.ui.actionNavega_o.triggered.connect(lambda: self.webEngineView.page().runJavaScript("document.querySelector('body').style.userSelect = 'none'"))
        self.ui.actionNavega_o.setShortcut('Ctrl+W')

        #actionPrefer_ncias
        self.ui.actionPrefer_ncias.triggered.connect(lambda: self.settings.open_settings())
        self.ui.actionPrefer_ncias.setShortcut('Alt+P')

        #actionCustomizado
        self.ui.actionCustomizado.triggered.connect(lambda: self.open_custom_url(self.settings.wikiAddress))
        self.ui.actionCustomizado.setShortcut('Ctrl+Shift+L')

        #actionAnterior
        self.ui.actionVoltar.triggered.connect(lambda: self.webEngineView.back())
        self.ui.actionVoltar.setShortcut('Alt+Left')

        #actionPosterior
        self.ui.actionPosterior.triggered.connect(lambda: self.webEngineView.forward())
        self.ui.actionPosterior.setShortcut('Alt+Right')

        #actionRecarregar
        self.ui.actionRecarregar.triggered.connect(lambda: self.webEngineView.reload())
        self.ui.actionRecarregar.setShortcut('F5')

        #actionPesquisar
        self.ui.actionPesquisar.triggered.connect(lambda: self.open_custom_url(self.settings.searchAddress))
        self.ui.actionPesquisar.setShortcut('Ctrl+Shift+K')

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

    def open_custom_url(self, prefix = ""):
        input_url, ok = self.settings.ask_for_input("",
            QCoreApplication.translate("Main_Window", "Acessar endereço"),
            QCoreApplication.translate("Main_Window", "Por favor, digite o endereço:")
        )
        if ok and input_url:
            self.webEngineView.setUrl(QUrl(f"{prefix.toString()}{input_url}"))

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
            self.webEngineView.page().runJavaScript(self.settings.read_from_resources(":default.js"))
            self.webEngineView.page().runJavaScript(self.settings.qsettings.value("settings/customJavaScript", type=str, defaultValue=""))
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
