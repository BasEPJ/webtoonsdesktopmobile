import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QAction, QWidget, QPushButton, QToolBar, QInputDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, QStandardPaths

# Variables globales
MOBILE_USER_AGENT = 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36'
DESKTOP_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
BASE_URL = "https://www.webtoons.com/"
LANGUAGE_PROMPT = "Select Language"
STORAGE_DIR_NAME = "webtoon_profile"

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_main_window()
        self.init_profile()
        self.init_ui()

    def init_main_window(self):
        self.setWindowIcon(QIcon(self.resource_path('webtoon.ico')))
        self.setWindowTitle('Webtoons Desktop Mobile')
        self.setGeometry(100, 100, 800, 600)

    def init_profile(self):
        self.storage_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation), STORAGE_DIR_NAME)
        print(f"Almacenando datos en: {self.storage_path}")
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
        
        self.profile = QWebEngineProfile(STORAGE_DIR_NAME, self)
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
        self.profile.setCachePath(self.storage_path)
        self.profile.setPersistentStoragePath(self.storage_path)

        self.page = QWebEnginePage(self.profile, self)
        self.webview = QWebEngineView()
        self.webview.setPage(self.page)

        self.profile.setHttpUserAgent(MOBILE_USER_AGENT)

    def init_ui(self):
        self.create_toolbar()
        self.create_layout()
        self.load_initial_url()

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        back_button = self.create_toolbar_button('icons/back.png', self.webview.back)
        toolbar.addWidget(back_button)

        reload_button = self.create_toolbar_button('icons/reload.png', self.webview.reload)
        toolbar.addWidget(reload_button)

        forward_button = self.create_toolbar_button('icons/forward.png', self.webview.forward)
        toolbar.addWidget(forward_button)

        self.switch_button = QPushButton()
        self.switch_button.setIcon(QIcon(self.resource_path('icons/switch.png')))
        self.switch_button.setCheckable(True)
        self.switch_button.clicked.connect(self.switch_user_agent)
        toolbar.addWidget(self.switch_button)

        change_language_action = QAction(QIcon(self.resource_path('icons/language.png')), LANGUAGE_PROMPT, self)
        change_language_action.triggered.connect(self.change_language)
        toolbar.addAction(change_language_action)

    def create_toolbar_button(self, icon_path, callback):
        button = QPushButton()
        button.setIcon(QIcon(self.resource_path(icon_path)))
        button.clicked.connect(callback)
        return button

    def create_layout(self):
        layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(layout)
        layout.addWidget(self.webview)
        self.setCentralWidget(container)

    def load_initial_url(self):
        language = self.load_language_preference()
        initial_url = f"{BASE_URL}{language}/"
        self.webview.setUrl(QUrl(initial_url))

    def resource_path(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    
    def switch_user_agent(self):
        if self.switch_button.isChecked():
            self.profile.setHttpUserAgent(MOBILE_USER_AGENT)
        else:
            self.profile.setHttpUserAgent(DESKTOP_USER_AGENT)
        
        current_url = self.webview.url().toString()
        print(f"Recargando URL: {current_url}")
        self.webview.setUrl(QUrl(current_url))

    def load_language_preference(self):
        config_path = os.path.join(self.storage_path, 'config.txt')
        if os.path.exists(config_path):
            with open(config_path, 'r') as config_file:
                return config_file.read().strip()
        return 'en'

    def save_language_preference(self, language):
        config_path = os.path.join(self.storage_path, 'config.txt')
        with open(config_path, 'w') as config_file:
            config_file.write(language)

    def change_language(self):
        languages = ["en", "es", "fr", "de", "zh-hant", "th", "id"]
        language, ok = QInputDialog.getItem(self, LANGUAGE_PROMPT, "Language:", languages, 0, False)
        if ok and language:
            self.save_language_preference(language)
            new_url = f"{BASE_URL}{language}/"
            print(f"Cambiando URL a: {new_url}")
            self.webview.setUrl(QUrl(new_url))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())
