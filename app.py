import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QStackedWidget, QPushButton
from PyQt5.QtCore import Qt
from screens.home_screen import HomeScreen
from screens.crop_screen import CropScreen

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

        button3 = QPushButton("Salir")
        button3.setStyleSheet(
            "QPushButton { background-color: #ff5555; color: #f8f8f2; border: none; padding: 10px; }"
            "QPushButton:hover { background-color: #ff4444; }"
        )
        button3.clicked.connect(self.close)

        # Agregar botones al layout del menú
        menu_layout.addWidget(button1)
        menu_layout.addWidget(button2)
        menu_layout.addWidget(button3)
        side_menu.setLayout(menu_layout)

        # Stacked widget para cambiar entre pantallas
        self.stack = QStackedWidget()

        # Pantallas
        self.home_screen = HomeScreen()
        self.stack.addWidget(self.home_screen)

        self.crop_screen = CropScreen()
        self.stack.addWidget(self.crop_screen)

        # Agregar layouts al layout principal
        main_layout.addWidget(side_menu)
        main_layout.addWidget(self.stack)

        # Configurar el layout del widget central
        central_widget.setLayout(main_layout)

    def show_home(self):
        self.stack.setCurrentWidget(self.home_screen)

    def show_crop(self):
        self.stack.setCurrentWidget(self.crop_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
