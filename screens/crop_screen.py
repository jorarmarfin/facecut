import dlib
from PIL import Image
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from utils import load_configuration

# Ruta del modelo preentrenado de Dlib
detector = dlib.get_frontal_face_detector()

class CropScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Título
        title = QLabel("Pantalla de Recorte")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #bd93f9;")
        title.setAlignment(Qt.AlignLeft)
        layout.addWidget(title)

        # Selector de carpeta de fotos
        self.photo_folder_label = QLabel("Escoger carpeta de fotos")
        self.photo_folder_label.setStyleSheet("font-size: 14px; color: #f8f8f2;")
        layout.addWidget(self.photo_folder_label)

        self.photo_folder_input = QLineEdit()
        self.photo_folder_input.setPlaceholderText("Ruta de la carpeta de fotos...")
        self.photo_folder_input.setStyleSheet(
            "background-color: #f8f8f2; color: #000; border: 1px solid #44475a; padding: 5px;"
        )
        layout.addWidget(self.photo_folder_input)

        self.photo_folder_button = QPushButton("Seleccionar carpeta")
        self.photo_folder_button.setStyleSheet(
            "background-color: #6272a4; color: #f8f8f2; border: none; padding: 5px;"
            "QPushButton:hover { background-color: #506294; }"
        )
        self.photo_folder_button.clicked.connect(self.select_photo_folder)
        layout.addWidget(self.photo_folder_button)

        # Selector de carpeta de salida
        self.output_folder_label = QLabel("Escoger carpeta de salida")
        self.output_folder_label.setStyleSheet("font-size: 14px; color: #f8f8f2;")
        layout.addWidget(self.output_folder_label)

        self.output_folder_input = QLineEdit()
        self.output_folder_input.setPlaceholderText("Ruta de la carpeta de salida...")
        self.output_folder_input.setStyleSheet(
            "background-color: #f8f8f2; color: #000; border: 1px solid #44475a; padding: 5px;"
        )
        layout.addWidget(self.output_folder_input)

        self.output_folder_button = QPushButton("Seleccionar carpeta")
        self.output_folder_button.setStyleSheet(
            "background-color: #6272a4; color: #f8f8f2; border: none; padding: 5px;"
            "QPushButton:hover { background-color: #506294; }"
        )
        self.output_folder_button.clicked.connect(self.select_output_folder)
        layout.addWidget(self.output_folder_button)

        # Botón de recortar
        self.crop_button = QPushButton("Recortar")
        self.crop_button.setStyleSheet(
            "background-color: #6272a4; color: #f8f8f2; font-size: 14px; border: none; padding: 10px;"
            "QPushButton:hover { background-color: #506294; }"
        )
        self.crop_button.clicked.connect(self.start_crop)
        layout.addWidget(self.crop_button)

        # Etiqueta para mostrar el estado de la imagen actual
        self.status_label = QLabel("Estado: Esperando acción")
        self.status_label.setStyleSheet("font-size: 14px; color: #f8f8f2;")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def select_photo_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de fotos")
        if folder:
            self.photo_folder_input.setText(folder)

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de salida")
        if folder:
            self.output_folder_input.setText(folder)

    def start_crop(self):
        input_folder = self.photo_folder_input.text()
        output_folder = self.output_folder_input.text()

        if not input_folder or not output_folder:
            self.status_label.setText("Estado: Seleccione ambas carpetas.")
            return
        config = load_configuration()
        print(config)
        self.recortar_cabezas(input_folder, output_folder, config["margen_ancho"], config["margen_alto"])

    def recortar_cabezas(self, input_folder, output_folder, margen_ancho, margen_alto):
        """
        Recorta cabezas con un margen configurable.
        :param input_folder: Carpeta de entrada con imágenes.
        :param output_folder: Carpeta donde se guardarán las caras recortadas.
        :param margen_ancho: Margen adicional en proporción al ancho detectado (ejemplo: 0.2 = 20%).
        :param margen_alto: Margen adicional en proporción a la altura detectada (ejemplo: 0.3 = 30%).
        """
        # Crear la carpeta de salida si no existe
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Procesar cada imagen en la carpeta de entrada
        for filename in os.listdir(input_folder):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                # Actualizar estado
                self.status_label.setText(f"Procesando: {filename}")

                # Leer la imagen
                image_path = os.path.join(input_folder, filename)
                img = Image.open(image_path).convert("RGB")

                # Convertir la imagen a formato compatible con dlib
                img_array = dlib.load_rgb_image(image_path)

                # Detectar caras
                faces = detector(img_array)

                # Recortar cada cara detectada
                for i, face in enumerate(faces):
                    # Coordenadas del rectángulo de la cara detectada
                    x, y, x2, y2 = face.left(), face.top(), face.right(), face.bottom()

                    # Calcular el ancho y alto del rostro detectado
                    ancho = x2 - x
                    alto = y2 - y

                    # Aplicar márgenes
                    x -= int(ancho * margen_ancho)
                    x2 += int(ancho * margen_ancho)
                    y -= int(alto * margen_alto)
                    y2 += int(alto * margen_alto)

                    # Asegurarse de que las coordenadas estén dentro de los límites de la imagen
                    x, y = max(0, x), max(0, y)
                    x2, y2 = min(img.width, x2), min(img.height, y2)

                    # Recortar la cara con márgenes
                    cropped_face = img.crop((x, y, x2, y2))

                    # Guardar la cara recortada
                    output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_face{i+1}.jpg")
                    cropped_face.save(output_path)

                print(f"Procesada: {filename}, Caras detectadas: {len(faces)}")

        # Actualizar estado final
        self.status_label.setText("Estado: Procesamiento completado.")
