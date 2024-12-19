from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Logo
        logo = QLabel()
        pixmap = QPixmap("assets/logo.png")  # Cambia "logo.png" por la ruta de tu imagen
        pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)

        # Texto debajo del logo
        title = QLabel("FaceCut")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #bd93f9;")
        title.setAlignment(Qt.AlignCenter)

        layout.addWidget(logo)
        layout.addWidget(title)
        self.setLayout(layout)
