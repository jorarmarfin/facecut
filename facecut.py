import dlib
from PIL import Image
import os

# Ruta del modelo preentrenado de Dlib (se descarga automáticamente con dlib)
detector = dlib.get_frontal_face_detector()

def recortar_cabezas(input_folder, output_folder):
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
                # Coordenadas del rectángulo de la cara
                x, y, x2, y2 = face.left(), face.top(), face.right(), face.bottom()

                # Recortar la cara
                cropped_face = img.crop((x, y, x2, y2))

                # Guardar la cara recortada
                output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_face{i+1}.jpg")
                cropped_face.save(output_path)

            print(f"Procesada: {filename}, Caras detectadas: {len(faces)}")

# Configurar rutas
carpeta_entrada = "input"
carpeta_salida = "output"

# Ejecutar
recortar_cabezas(carpeta_entrada, carpeta_salida)
