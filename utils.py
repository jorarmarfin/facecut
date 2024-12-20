import os
import json
import requests


def load_configuration():
    """
    Carga los valores del archivo config.json desde la raíz del proyecto.
    :return: Diccionario con los valores de configuración o valores por defecto.
    """
    config_file_path = get_config_path()
    try:
        with open(config_file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Advertencia: El archivo {config_file_path} no se encontró. Usando valores por defecto.")
    except json.JSONDecodeError:
        print(f"Error: El archivo {config_file_path} está dañado. Usando valores por defecto.")
    return {
        "margen_ancho": 0.2,
        "margen_alto": 0.3,
        "licencia": ""
    }
def get_config_path():
    """
    Devuelve la ruta absoluta al archivo config.json ubicado en la raíz del proyecto.
    """
    # Ruta base del proyecto (directorio del script principal)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Retrocede al directorio raíz desde /screens si es necesario
    if "screens" in base_dir:
        base_dir = os.path.dirname(base_dir)

    # Ruta final al archivo config.json
    return os.path.join(base_dir, "config.json")

def validate_license(licencia):
    """
    Valida la licencia contra el servidor remoto.
    :param licencia: Clave de licencia a validar.
    :return: Diccionario con el resultado de la validación.
    """
    url = "https://facecut.hefesto2js.com/validar_licencia"  # Reemplaza <TU_IP> con la IP de tu servidor
    try:
        response = requests.post(url, json={"licencia": licencia})
        if response.status_code == 200:
            return response.json()
        else:
            return {"valida": False, "error": f"Error del servidor: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"valida": False, "error": f"Error de conexión: {e}"}
