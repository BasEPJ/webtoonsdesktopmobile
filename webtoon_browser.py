import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QAction, QWidget, QPushButton, QToolBar, QInputDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, QStandardPaths

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Inicialización de la ventana principal
        self.init_main_window()

        # Configuración del perfil del navegador
        self.init_profile()

        # Inicialización de la interfaz de usuario
        self.init_ui()

    # Método para inicializar la ventana principal
    def init_main_window(self):
        self.setWindowIcon(QIcon(self.resource_path('webtoon.ico')))
        self.setWindowTitle('Webtoons Desktop Mobile')
        self.setGeometry(100, 100, 800, 600)


    # Método para configurar el perfil del navegador
    def init_profile(self):
        self.storage_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation), "webtoon_profile")
        print(f"Almacenando datos en: {self.storage_path}")
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
        
        self.profile = QWebEngineProfile("webtoon_profile", self)
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
        self.profile.setCachePath(self.storage_path)
        self.profile.setPersistentStoragePath(self.storage_path)

        self.page = QWebEnginePage(self.profile, self)
        self.webview = QWebEngineView()
        self.webview.setPage(self.page)

        # Configurar el User-Agent inicial para móvil
        mobile_user_agent = 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36'
        self.profile.setHttpUserAgent(mobile_user_agent)


    # Método para inicializar la interfaz de usuario
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
        self.switch_button.setChecked(True)  # Por defecto está en modo móvil
        self.switch_button.clicked.connect(self.switch_user_agent)
        toolbar.addWidget(self.switch_button)

        change_language_action = QAction(QIcon(self.resource_path('icons/language.png')), "Change Language", self)
        change_language_action.triggered.connect(self.change_language)
        toolbar.addAction(change_language_action)



        # Crear un layout principal
        layout = QVBoxLayout()

        # Crear un widget contenedor
        container = QWidget()
        container.setLayout(layout)

        # Agregar el WebView al layout
        layout.addWidget(self.webview)

        self.setCentralWidget(container)

        # Cargar la URL inicial
        language = self.load_language_preference()
        initial_url = f"https://www.webtoons.com/{language}/"
        self.webview.setUrl(QUrl(initial_url))

    #Función switch_user_agent
    def switch_user_agent(self):
        if self.switch_button.isChecked():
            # Cambiar a User-Agent móvil
            mobile_user_agent = 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36'
            self.profile.setHttpUserAgent(mobile_user_agent)
        else:
            # Cambiar a User-Agent de escritorio
            desktop_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            self.profile.setHttpUserAgent(desktop_user_agent)
        
        # Recargar la página para aplicar el nuevo User-Agent
        self.webview.reload()

    #Método para Crear Botones en la Barra de Herramientas
    def create_toolbar_button(self, icon_path, callback):
        button = QPushButton()
        button.setIcon(QIcon(self.resource_path(icon_path)))
        button.clicked.connect(callback)
        return button

    #Método para Crear el Layout Principal
    def create_layout(self):
        layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(layout)
        layout.addWidget(self.webview)
        self.setCentralWidget(container)


    #Método para Cargar la URL Inicial
    def load_initial_url(self):
        language = self.load_language_preference()
        initial_url = f"https://www.webtoons.com/{language}/"
        self.webview.setUrl(QUrl(initial_url))


    #Método resource_path
    def resource_path(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    

    # Método para cambiar entre User-Agent móvil y de escritorio
    def switch_user_agent(self):
        current_url = self.webview.url().toString()
        print(f"Recargando URL: {current_url}")
        
        if self.switch_button.isChecked():
            # Cambiar a User-Agent móvil
            mobile_user_agent = 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36'
            self.profile.setHttpUserAgent(mobile_user_agent)
        else:
            # Cambiar a User-Agent predeterminado (escritorio)
            default_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            self.profile.setHttpUserAgent(default_user_agent)
        
        # Eliminar la página anterior y crear una nueva instancia de QWebEnginePage
        self.page = QWebEnginePage(self.profile, self)
        self.webview.setPage(self.page)

        # Recargar la página con la URL actual
        self.webview.setUrl(QUrl(current_url))
    #Métodos para Gestión de Idiomas
    def load_language_preference(self):
        config_path = os.path.join(self.storage_path, 'config.txt')
        if os.path.exists(config_path):
            with open(config_path, 'r') as config_file:
                return config_file.read().strip()
        return 'en'  # Idioma predeterminado

    def save_language_preference(self, language):
        config_path = os.path.join(self.storage_path, 'config.txt')
        with open(config_path, 'w') as config_file:
            config_file.write(language)

    #Método para Cambiar el Idioma
    def change_language(self):
        languages = ["en", "es", "fr", "de", "zh-hant", "th", "id"]
        language, ok = QInputDialog.getItem(self, "Select Language", "Language:", languages, 0, False)
        if ok and language:
            self.save_language_preference(language)
            base_url = "https://www.webtoons.com/"
            new_url = f"{base_url}{language}/"
            print(f"Cambiando URL a: {new_url}")
            self.webview.setUrl(QUrl(new_url))


# Bloque principal para ejecutar la aplicación
if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())