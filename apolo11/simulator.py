import json
import datetime
import hashlib
import os
import random
import shutil
import time
import pandas as pd
import pathlib
from apolo11.base.log import logClass
from apolo11.configs import constants


# Event Logger Decorator
def log_event(func):
    """Decorator to log events.

    :param func: The function to be decorated.
    :type func: function
    """

    def wrapper(*args, **kwargs):
        """Wrapper function to log events.

        :return: The result of the decorated function.
        :rtype: Any
        """
        result = func(*args, **kwargs)
        args[0].logger.info(f"Event: {func.__name__}")
        return result

    return wrapper


# Class for file management
class FileManager(logClass):
    """Manages file operations.

    :param logClass: Class providing logging functionality.
    :type logClass: class
    """

    def __init__(self, ruta_preferencia: str):
        """Initializes FileManager with the preferred path

        :param ruta_preferencia: The preferred path.
        :type ruta_preferencia: str
        """
        self.ruta_preferencia = pathlib.Path(ruta_preferencia)
        self.ruta_devices = os.path.join(ruta_preferencia, "devices")
        self.ruta_backups = os.path.join(ruta_preferencia, "backups")

        if not os.path.exists(self.ruta_devices):
            os.makedirs(self.ruta_devices)
        if not os.path.exists(self.ruta_backups):
            os.makedirs(self.ruta_backups)

    @log_event
    def limpiar_archivos_procesados(self):
        """Moves processed files to the backup directory.

        Clears out processed files from the devices directory and moves them to a backup directory with a timestamped folder name.
        """
        fecha_archivo = str(datetime.datetime.now().strftime("%d%m%y%H%M%S"))
        self.ruta_destino = os.path.join(self.ruta_backups, fecha_archivo)
        os.makedirs(self.ruta_destino, exist_ok=True)
        archivos_procesados = os.listdir(self.ruta_devices)
        for archivo in archivos_procesados:
            ruta_archivo_origen = os.path.join(self.ruta_devices, archivo)
            ruta_archivo_destino = os.path.join(self.ruta_destino, archivo)
            shutil.move(ruta_archivo_origen, ruta_archivo_destino)


# Specific subclass for managing device file handling
class DeviceFileManager(FileManager):
    """Manages device-specific file operations.

    :param FileManager: Class providing file management functionality.
    :type FileManager: class

    This class extends FileManager to handle device-specific file operations such as simulating data, generating reports,
    and managing disconnections.
    """

    def __init__(self, ruta_preferencia: str):
        super().__init__(ruta_preferencia)

    @log_event
    def simular_datos(self, cantidad_archivos: int):
        """Simulates data for a specified number of files.

        :param cantidad_archivos: The number of files to simulate data for (random number)
        :type cantidad_archivos: int

        This function simulates data for the specified number of files by generating random mission names, dates, device types,
        and states. It calculates a hash value for each simulated file and saves them in the devices directory.
        """
        for _ in range(cantidad_archivos):
            nombre_mision = random.choice(constants.proyectos)
            fecha = datetime.datetime.now().strftime("%d%m%y%H%M%S")
            tipo_dispositivo = random.choice(constants.lista_dispositivos)
            estado_dispositivo = random.choice(constants.lista_estados)
            hash_calculado = self.calcular_hash(
                fecha, nombre_mision, tipo_dispositivo, estado_dispositivo
            )
            i = 1
            while True:
                nombre_archivo = f"APL{nombre_mision}-0000[{i}].log"
                ruta_archivo = os.path.join(self.ruta_devices, nombre_archivo)
                if not os.path.exists(ruta_archivo):
                    break
                i += 1

            with open(ruta_archivo, "w") as archivo:
                archivo.write(f"fecha:{fecha}\n")
                archivo.write(f"mision:{nombre_mision}\n")
                archivo.write(f"tipo_dispositivo:{tipo_dispositivo}\n")
                archivo.write(f"estado_dispositivo:{estado_dispositivo}\n")
                archivo.write(f"hash:{hash_calculado}\n")

    @staticmethod
    def calcular_hash(
        fecha: str, mision: str, tipo_dispositivo: str, estado_dispositivo: str
    ):
        """Calculates the hash value for given parameters.

        :param fecha: The date.
        :type fecha: str
        :param mision: The mission name.
        :type mision: str
        :param tipo_dispositivo: The device type.
        :type tipo_dispositivo: str
        :param estado_dispositivo: The device state.
        :type estado_dispositivo: str
        :return: The calculated hash value.
        :rtype: str
        """
        if mision != "UNKN":
            datos_para_hash = (
                f"{fecha}{mision}{tipo_dispositivo}{estado_dispositivo}".encode("utf-8")
            )
            return hashlib.sha256(datos_para_hash).hexdigest()
        return ""

    @log_event
    def generar_reportes(self):
        """Generates reports based on device events and disconnections.

        This function generates reports based on device events and disconnections by analyzing events and managing disconnections.
        It prints the reports to the console and saves them as JSON files.
        """
        reporte_eventos = self.analizar_eventos()
        reporte_desconexiones = self.gestionar_desconexiones()

        df_eventos = pd.DataFrame(reporte_eventos)
        df_desconexiones = pd.DataFrame(reporte_desconexiones)

        print("Reporte de Eventos:")
        print(df_eventos)
        print("\nReporte de Desconexiones:")
        print(df_desconexiones)

        with open(
            os.path.join(self.ruta_devices, "reporte_eventos.json"), "w"
        ) as archivo:
            json.dump(reporte_eventos, archivo)

        with open(
            os.path.join(self.ruta_devices, "reporte_desconexiones.json"), "w"
        ) as archivo:
            json.dump(reporte_desconexiones, archivo)

    @log_event
    def generar_tablero_de_control(self):
        """Generates a control dashboard based on device events and disconnections.

        This function generates a control dashboard based on device events and disconnections by analyzing events and managing disconnections.
        It saves the generated control dashboard as a JSON file in the backups directory.
        """
        reporte_eventos = self.analizar_eventos()
        reporte_desconexiones = self.gestionar_desconexiones()

        tablero_de_control = {
            "reporte_eventos": reporte_eventos,
            "reporte_desconexiones": reporte_desconexiones,
        }

        ruta_tablero_control = os.path.join(
            self.ruta_backups, "tablero_de_control.json"
        )
        with open(ruta_tablero_control, "w") as archivo:
            json.dump(tablero_de_control, archivo)

    def analizar_eventos(self):
        """Analyzes device events and counts occurrences of different states.

        :return: A dictionary containing the count of each state.
        :rtype: dict

        This function analyzes device events by reading device files from the devices directory.
        It counts the occurrences of different states ('excellent', 'good', 'warning', 'faulty', 'killed', 'unknown')
        and returns a dictionary containing the count of each state.
        """
        archivos_dispositivos = os.listdir(self.ruta_devices)
        eventos = {
            "excellent": 0,
            "good": 0,
            "warning": 0,
            "faulty": 0,
            "killed": 0,
            "unknown": 0,
        }

        for archivo in archivos_dispositivos:
            ruta_archivo = os.path.join(self.ruta_devices, archivo)
            with open(ruta_archivo, "r") as f:
                contenido = f.readlines()
                for linea in contenido:
                    key, value = linea.strip().split(":")
                    if key == "estado_dispositivo":
                        estado_dispositivo = value.strip()
                        if estado_dispositivo in eventos:
                            eventos[estado_dispositivo] += 1

        return {"eventos": eventos}

    def gestionar_desconexiones(self):
        """Manages disconnections and counts occurrences of unknown state.

        :return: A dictionary containing the count of unknown state disconnections for each device.
        :rtype: dict

        This function manages disconnections by reading device files from the devices directory.
        It counts the occurrences of the unknown state in each device file and returns a dictionary
        containing the count of unknown state disconnections for each device.
        """
        archivos_dispositivos = os.listdir(self.ruta_devices)
        desconexiones = {"desconexiones": {}}

        for archivo in archivos_dispositivos:
            ruta_archivo = os.path.join(self.ruta_devices, archivo)
            with open(ruta_archivo, "r") as f:
                contenido = f.readlines()
                for linea in contenido:
                    key, value = linea.strip().split(":")
                    if key == "estado_dispositivo" and value.strip() == "unknown":
                        desconexiones["desconexiones"][archivo] = (
                            desconexiones["desconexiones"].get(archivo, 0) + 1
                        )

        return desconexiones


# Main Class
class Apolo11Simulator(DeviceFileManager, logClass):
    """Simulates the operation of the Apollo 11 devices.

    :param DeviceFileManager: Class providing device file management functionality.
    :type DeviceFileManager: class
    :param logClass: Class providing logging functionality.
    :type logClass: class
    """

    def __init__(self, ruta_preferencia: str):
        """Initializes the class.

        :param ruta_preferencia: The preferred path for file operations.
        :type ruta_preferencia: str
        """
        super().__init__(ruta_preferencia)
        self.logger.info("Initializing...")

    def ejecutar_simulacion(self):
        """Executes the simulation loop.

        This method runs the simulation loop indefinitely. In each iteration, it simulates device data,
        generates reports, cleans processed files, and generates a control dashboard. It then waits for
        a predefined iteration time before starting the next iteration.
        """
        while True:
            self.simular_datos(random.choice(constants.cantidad_archivos))
            self.generar_reportes()
            self.limpiar_archivos_procesados()
            self.generar_tablero_de_control()
            time.sleep(constants.tiempo_iteracion)
