import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QStackedWidget, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from screens.home_screen import HomeScreen
from screens.crop_screen import CropScreen
from screens.config_screen import ConfigScreen
from utils import validate_license, load_configuration

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar ventana principal
        self.setWindowTitle("FaceCut")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #282a36; color: #f8f8f2;")

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QHBoxLayout()

        # Menu lateral
        side_menu = QFrame()
        side_menu.setFixedWidth(200)
        side_menu.setStyleSheet("background-color: #44475a;")

        menu_layout = QVBoxLayout()
        menu_layout.setAlignment(Qt.AlignTop)

        # Botones del menú
        button1 = QPushButton("Inicio")
        button1.setStyleSheet(
            "QPushButton { background-color: #6272a4; color: #f8f8f2; border: none; padding: 10px; }"
            "QPushButton:hover { background-color: #506294; }"
        )
        button1.clicked.connect(self.show_home)

        button2 = QPushButton("Recortar")
        button2.setStyleSheet(
            "QPushButton { background-color: #6272a4; color: #f8f8f2; border: none; padding: 10px; }"
            "QPushButton:hover { background-color: #506294; }"
        )
        button2.clicked.connect(self.show_crop)

        button3 = QPushButton("Configuración")
        button3.setStyleSheet(
            "QPushButton { background-color: #6272a4; color: #f8f8f2; border: none; padding: 10px; }"
            "QPushButton:hover { background-color: #506294; }"
        )
        button3.clicked.connect(self.show_config)

        button10 = QPushButton("Salir")
        button10.setStyleSheet(
            "QPushButton { background-color: #ff5555; color: #f8f8f2; border: none; padding: 10px; }"
            "QPushButton:hover { background-color: #ff4444; }"
        )
        button10.clicked.connect(self.close)

        # Agregar botones al layout del menú
        menu_layout.addWidget(button1)
        menu_layout.addWidget(button2)
        menu_layout.addWidget(button3)
        menu_layout.addWidget(button10)
        side_menu.setLayout(menu_layout)

        # Stacked widget para cambiar entre pantallas
        self.stack = QStackedWidget()

        # Pantallas
        self.home_screen = HomeScreen()
        self.stack.addWidget(self.home_screen)

        self.crop_screen = CropScreen()
        self.stack.addWidget(self.crop_screen)

        self.config_screen = ConfigScreen(self.licence_validated)
        self.stack.addWidget(self.config_screen)

        # Agregar layouts al layout principal
        main_layout.addWidget(side_menu)
        main_layout.addWidget(self.stack)

        # Configurar el layout del widget central
        central_widget.setLayout(main_layout)

        # Validar licencia al inicio
        self.licencia_valida = self.licence_validate_start()

    def licence_validate_start(self):
        """
        Carga y valida la licencia al inicio del sistema.
        """
        conf = load_configuration()
        licencia = conf.get("licencia")
        if licencia:
            result = validate_license(licencia)
            return result.get("valida", False)
        return False

    def licence_validated(self):
        """
        Marca la licencia como válida tras la validación en ConfigScreen.
        """
        self.licencia_valida = True
        QMessageBox.information(self, "Éxito", "Licencia validada correctamente. Ahora puede usar la funcionalidad de recorte.")
        self.show_home()

    def show_home(self):
        """
        Muestra la pantalla de inicio.
        """
        self.stack.setCurrentWidget(self.home_screen)

    def show_crop(self):
        """
        Muestra la pantalla de recorte si la licencia es válida.
        """
        if self.licencia_valida:
            self.stack.setCurrentWidget(self.crop_screen)
        else:
            QMessageBox.warning(self, "Acceso Denegado", "Debe validar una licencia válida en Configuración antes de usar esta funcionalidad.")
            self.show_config()

    def show_config(self):
        """
        Muestra la pantalla de configuración.
        """
        self.stack.setCurrentWidget(self.config_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
