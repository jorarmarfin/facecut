
# Proyecto de Recorte Automático de Rostros para Carnés

Este proyecto utiliza la biblioteca `dlib` para detectar rostros en imágenes, recortarlos y guardarlos en una carpeta específica. Está diseñado para recortar fotografías de rostros con márgenes configurables, lo que lo hace ideal para generar fotos de carnés o credenciales.

## Características
- Detección automática de rostros en imágenes.
- Recorte de rostros con márgenes ajustables para incluir frente y mentón.
- Procesamiento de múltiples imágenes en una carpeta.
- Guardado de recortes en una carpeta de salida.

## Requisitos
- Python 3.8 o superior.
- Bibliotecas requeridas:
  - `dlib`
  - `Pillow`

### Instalación de Dependencias
Ejecuta el siguiente comando para instalar las dependencias necesarias:
```bash
pip install dlib pillow
```

## Uso
1. Coloca las imágenes en una carpeta de entrada (por ejemplo, `input`).
2. Configura las rutas de entrada y salida en el script.
3. Ajusta los márgenes de ancho y alto según tus necesidades:
   - `margen_ancho`: Proporción adicional en los bordes laterales (por ejemplo, 0.2 para un 20% del ancho).
   - `margen_alto`: Proporción adicional en los bordes superior e inferior (por ejemplo, 0.3 para un 30% de la altura).
4. Ejecuta el script:
```bash
python recortar_cabezas.py
```

## Estructura del Proyecto
```
Proyecto/
├── input/          # Carpeta con imágenes de entrada
├── output/         # Carpeta donde se guardarán los recortes
├── recortar_cabezas.py # Script principal
└── README.md       # Archivo con información del proyecto
```

## Contribuciones
¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar el proyecto, no dudes en enviar un pull request o abrir un issue.

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Autor
Luis

## Compilar el proyecto
Si deseas compilar el proyecto en un ejecutable, puedes utilizar `PyInstaller`. Ejecuta el siguiente comando en la terminal para compilar el proyecto en un archivo ejecutable:
```bash
pyinstaller --onefile --noconsole --icon=icon.ico --add-data "config.json:." --add-data "assets/*:assets/" app.py
docker run --rm -v "$(pwd):/src/" cdrx/pyinstaller-windows "pyinstaller --onefile --noconsole --icon=icon.ico --add-data config.json:. --add-data assets/*:assets/ app.py"
```

pip freeze > requirements.txt
```