import json
from pathlib import Path


class ArchivoServicio:
    def __init__(self, carpeta_datos: str | Path) -> None:
        self.carpeta_datos = Path(carpeta_datos)

    def leer_json(self, nombre_archivo: str) -> list:
        # Responsabilidad unica: leer un archivo JSON y devolver una lista.
        ruta = self.carpeta_datos / nombre_archivo

        try:
            with ruta.open("r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except FileNotFoundError:
            print(f"No se encontro el archivo {nombre_archivo}. Se inicia una lista vacia.")
            return []
        except json.JSONDecodeError:
            print(f"El archivo {nombre_archivo} no tiene un formato JSON valido. Se inicia vacio.")
            return []
        except PermissionError:
            print(f"No hay permisos para leer el archivo {nombre_archivo}.")
            return []

        if not isinstance(datos, list):
            print(f"El archivo {nombre_archivo} debe contener una lista. Se inicia vacio.")
            return []

        return datos

    def escribir_json(self, nombre_archivo: str, datos: list) -> bool:
        # Responsabilidad unica: escribir una lista en un archivo JSON (productos, ventas y usuarios).
        ruta = self.carpeta_datos / nombre_archivo

        try:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            with ruta.open("w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except PermissionError:
            print(f"No hay permisos para guardar el archivo {nombre_archivo}.")
            return False
