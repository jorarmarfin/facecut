import json
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from utils import validate_license,load_configuration,get_config_path

class ConfigScreen(QWidget):
    def __init__(self, licencia_validada_callback):
        self.licencia_validada_callback = licencia_validada_callback
        super().__init__()

        # Ruta del archivo de configuración
        # self.config_file_path = os.path.join("screens", "config.json")
        conf = load_configuration()
        self.config_file_path = get_config_path()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Título
        title = QLabel("Pantalla de configuración")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #bd93f9;")
        title.setAlignment(Qt.AlignLeft)
        layout.addWidget(title)

        # Configuración de ancho y alto de recorte
        dimensions_layout = QHBoxLayout()

        # Ancho de recorte
        self.width_label = QLabel("Ancho de recorte")
        self.width_label.setStyleSheet("font-size: 14px; color: #f8f8f2;")
        dimensions_layout.addWidget(self.width_label)

        self.width_input = QLineEdit()
        self.width_input.setPlaceholderText("Ingrese el ancho...")
        self.width_input.setStyleSheet(
            "background-color: #f8f8f2; color: #000; border: 1px solid #44475a; padding: 5px;"
        )
        dimensions_layout.addWidget(self.width_input)

        # Alto de recorte
        self.height_label = QLabel("Alto de recorte")
        self.height_label.setStyleSheet("font-size: 14px; color: #f8f8f2;")
        dimensions_layout.addWidget(self.height_label)

        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Ingrese el alto...")
        self.height_input.setStyleSheet(
            "background-color: #f8f8f2; color: #000; border: 1px solid #44475a; padding: 5px;"
        )
        dimensions_layout.addWidget(self.height_input)

        layout.addLayout(dimensions_layout)

        # Configuración de licencia
        self.license_label = QLabel("Licencia")
        self.license_label.setStyleSheet("font-size: 14px; color: #f8f8f2;")
        layout.addWidget(self.license_label)

        self.license_input = QLineEdit()
        self.license_input.setPlaceholderText("Ingrese la clave de licencia...")
        self.license_input.setStyleSheet(
            "background-color: #f8f8f2; color: #000; border: 1px solid #44475a; padding: 5px;"
        )
        layout.addWidget(self.license_input)

        # Botón Guardar
        self.save_button = QPushButton("Guardar")
        self.save_button.setStyleSheet(
            "background-color: #6272a4; color: #f8f8f2; font-size: 14px; border: none; padding: 10px;"
            "QPushButton:hover { background-color: #506294; }"
        )
        self.save_button.clicked.connect(self.guardar_configuracion)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        # Cargar configuración al iniciar
        self.cargar_configuracion()

    def cargar_configuracion(self):
        """
        Lee el archivo config.json y llena los campos de la pantalla con los valores.
        """
        try:
            with open(self.config_file_path, "r") as file:
                config = json.load(file)
                self.width_input.setText(str(config.get("margen_ancho", "")))
                self.height_input.setText(str(config.get("margen_alto", "")))
                self.license_input.setText(config.get("licencia", ""))
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "El archivo de configuración no existe. Se usarán valores por defecto.")
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Error", "El archivo de configuración está dañado. Corrígelo o elimínalo.")

    def guardar_configuracion(self):
        """
        Guarda los valores ingresados en el archivo config.json.
        """
        try:
            # Leer valores de los campos
            ancho = self.width_input.text()
            alto = self.height_input.text()
            licencia = self.license_input.text()

            # Validar campos
            if not ancho or not alto or not licencia:
                QMessageBox.warning(self, "Error", "Por favor, llena todos los campos.")
                return

            # Crear el diccionario de configuración
            config = {
                "margen_ancho": float(ancho),
                "margen_alto": float(alto),
                "licencia": licencia
            }

            resultado = validate_license(licencia)
            if resultado.get("valida", False):
                self.licencia_validada_callback()  # Notificar que la licencia es válida
            else:
                error = resultado.get("error", "Licencia no válida.")
                QMessageBox.critical(self, "Error", f"No se pudo validar la licencia:\n{error}")

            # Guardar en config.json
            with open(self.config_file_path, "w") as file:
                json.dump(config, file, indent=4)
            QMessageBox.information(self, "Éxito", "¡Configuración guardada correctamente!")
        except ValueError:
            QMessageBox.warning(self, "Error", "Los valores de ancho y alto deben ser números válidos.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar la configuración: {e}")
