import dlib
from PIL import Image
import os

# Ruta del modelo preentrenado de Dlib
detector = dlib.get_frontal_face_detector()

def recortar_cabezas(input_folder, output_folder, margen_ancho=0.2, margen_alto=0.3):
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
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            # Leer la imagen
            image_path = os.path.join(input_folder, filename)
            img = Image.open(image_path).convert('RGB')

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

# Configurar rutas y márgenes
carpeta_entrada = "input"
carpeta_salida = "output"
margen_ancho = 0.2  # 20% del ancho detectado
margen_alto = 0.5   # 30% del alto detectado

# Ejecutar
recortar_cabezas(carpeta_entrada, carpeta_salida, margen_ancho, margen_alto)
