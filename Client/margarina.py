# This Python file uses the following encoding: utf-8
import sys
import os
import json

from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QPushButton
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
# from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QUrl, QTranslator, QFile, QCoreApplication, QTextStream
from PySide6.QtGui import QDesktopServices, QAction, QIcon
from Settings import Settings

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, profile, main_window, parent=None):
        super().__init__(profile, parent)
        self.main_window = main_window

    def acceptNavigationRequest(self, url: QUrl, isMainFrame: bool, action: QWebEnginePage.NavigationType) -> bool:
        if url.scheme() == "qrc" or url.scheme() == "data":
            return True

        if self.main_window.settings.wikiAddress.host() not in url.host():
            QDesktopServices.openUrl(url)
            return False
        return True

class CustomWebEngineView(QWebEngineView):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)

        cookie_storage_path = os.path.join(os.path.expanduser("~"), ".pestowiki")
        self.profile = QWebEngineProfile("PestoProfile", self)
        self.profile.setPersistentStoragePath(cookie_storage_path)

        self.setPage(CustomWebEnginePage(self.profile, main_window, self))


class MainWindow(QMainWindow):
    class InternalWebEnginePage(QWebEnginePage):
        def __init__(self, webEngineView, parent=None):
            super().__init__(parent)
            self.webEngineView = webEngineView

        def acceptNavigationRequest(self, url: QUrl, isMainFrame: bool, action: QWebEnginePage.NavigationType) -> bool:
            if url.scheme() == "data":
                return True
            self.webEngineView.setUrl(url)
            return False

    class InternalWebEngineView(QWebEngineView):
        def __init__(self, webEngineView, parent=None):
            super().__init__(parent)
            self.setPage(MainWindow.InternalWebEnginePage(webEngineView, self))

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
        if self.settings.useLastPage and self.settings.lastPage:
            self.webEngineView.setUrl(QUrl(self.settings.lastPage))
        else:
            self.webEngineView.setUrl(self.settings.wikiAddress)
        self.webEngineView.setZoomFactor(self.settings.zoom)

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
        self.ui.actionSobre.triggered.connect(lambda: self.show_about())
        self.ui.actionSobre.setShortcut('Alt+A')

        self.ui.actionIn_cio_2.triggered.connect(lambda: self.webEngineView.setUrl(self.settings.wikiAddress))
        self.ui.actionIn_cio_2.setShortcut('Alt+Shift+H')

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

        #actionMais
        self.ui.actionMais.triggered.connect(lambda: add_to_zoom(0.1))
        self.ui.actionMais.setShortcut('Alt+Z')

        #actionMenos
        self.ui.actionMenos.triggered.connect(lambda: add_to_zoom(-0.1))
        self.ui.actionMenos.setShortcut('Alt+Shift+Z')

        #actionHist_rico
        self.ui.actionHist_rico.triggered.connect(lambda: self.show_history())
        # self.ui.actionHist_rico.setShortcut('')

        def add_to_zoom(factor):
            finalzoom = self.settings.zoom + factor
            self.webEngineView.setZoomFactor(self.settings.zoom + factor)
            self.settings.change_setting("zoom", finalzoom)

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

        self.webEngineView.loadStarted.connect(lambda: self.webEngineView.setVisible(False))
        self.webEngineView.loadFinished.connect(lambda: self.webEngineView.setVisible(True))
        self.webEngineView.loadStarted.connect(self.on_load_started)
        self.webEngineView.loadFinished.connect(self.on_load_finished)

    def show_about(self):
        content = QCoreApplication.translate(
        "InternalPages",
        "Pesto é feito com carinho pelo grupo Margarina, seu código está disponível na licensa MIT."
        )
        html = self.read(":about.html").format(version=self.settings.version,content=content)
        self.load_internal_page(QCoreApplication.translate("InternalPages", "Sobre"), html)

    def show_history(self):
        body = ""
        for entry in self.settings.history:
            body += f"<a title{entry} href='{entry}'>{entry}</a><br>"
        self.load_internal_page(QCoreApplication.translate("InternalPages", "Histórico"), body)

    def load_internal_page(self, title, body, footer = None):
        if footer is None:
                footer = QCoreApplication.translate('Settings',
                    'Você está vendo uma página interna do Pesto.')
        template = self.read(":internal.html")
        html = template.format(title=title, body_content=body, footer=footer)
        dialog = QDialog(self)
        dialog.setWindowTitle("History")
        dialog.resize(450, 350)
        view = self.InternalWebEngineView(self.webEngineView, dialog)
        view.loadFinished.connect(lambda: view.page().runJavaScript(f"""var style = document.createElement('style'); style.innerHTML = `{self.read(":internal.css")}`; document.head.appendChild(style);"""))
        view.setHtml(html, "")
        layout = QVBoxLayout()
        layout.addWidget(view)
        dialog.setLayout(layout)
        dialog.exec()

    def update_history(self):
        self.settings.add_to_history(self.webEngineView.url())

    def open_custom_url(self, prefix = ""):
        input_url, ok = self.settings.ask_for_input("",
            QCoreApplication.translate("Main_Window", "Acessar endereço"),
            QCoreApplication.translate("Main_Window", "Por favor, digite o endereço:")
        )
        if ok and input_url:
            self.webEngineView.setUrl(QUrl(f"{prefix.toString()}{input_url}"))

    def on_load_started(self):
        self.statusBar().showMessage(QCoreApplication.translate("Main_Window", "Carregando..."))

    def click(self, id):
        js_code = f'''
            document.querySelector('#tool__bar button[accesskey="{id}"]').click();
        '''
        self.webEngineView.page().runJavaScript(js_code)

    def inject_scrollbar_styles(self, success):
        if success:
            if not str(self.settings.selectionMode).lower() in ['true', '1', 'yes']:
                self.inject_css("body {user-select: none;}")
            css = """
            body {
                overflow: auto;
                overflow-x: hidden;
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
            self.inject_css(css)

    def inject_css(self, css):
        self.webEngineView.page().runJavaScript(f"""
        var style = document.createElement('style');
        style.innerHTML = `{css}`;
        document.head.appendChild(style);
        """)

    def on_load_finished(self, success):
        if success:
            status_message = QCoreApplication.translate('Settings',
                'Página carregada com sucesso. ({}).'.format(self.webEngineView.url().toString()))
            self.statusBar().showMessage(status_message)
            self.webEngineView.page().runJavaScript(self.settings.read_from_resources(":default.js"))
            self.webEngineView.page().runJavaScript(self.settings.qsettings.value("settings/customJavaScript", type=str, defaultValue=""))
            self.webEngineView.setZoomFactor(self.settings.zoom)
            self.update_history()
        else:
            status_message = QCoreApplication.translate('Settings',
                'Erro ao carregar a página. ({}).'.format(self.webEngineView.url().toString()))
            self.statusBar().showMessage(status_message)

    def exit_application(self):
            self.close()

    def read(self, path):
        file = QFile(path)
        if file.open(QFile.ReadOnly | QFile.Text):
            text_stream = QTextStream(file)
            return text_stream.readAll()
        return ""

def start_app():
    global app
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    start_app()
