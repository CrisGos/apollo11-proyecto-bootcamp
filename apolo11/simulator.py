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


# Crear remoto y relacionarlos


class Apolo11Simulator(logClass):
    def __init__(self, ruta_preferencia: str):
        self.carpeta = 1  # VERIFICAR!!!
        self.logger.info("Initializing...")  # info para el logger
        self.ruta_preferencia = pathlib.Path(ruta_preferencia)
        self.ruta_devices = os.path.join(ruta_preferencia, "devices")
        self.ruta_backups = os.path.join(ruta_preferencia, "backups")

        # Create files if not exist
        if not os.path.exists(self.ruta_devices):
            os.makedirs(self.ruta_devices)
        if not os.path.exists(self.ruta_backups):
            os.makedirs(self.ruta_backups)

    def ejecutar_simulacion(self):
        while True:
            self.simular_datos(
                random.choice(constants.cantidad_archivos)
            )  # Pasar cantidad_archivos como parámetro
            self.generar_reportes()
            self.limpiar_archivos_procesados()
            self.generar_tablero_de_control()
            time.sleep(
                constants.tiempo_iteracion
            )  # Esperar 20 segundos entre simulaciones

    def simular_datos(self, cantidad_archivos: int):
        for _ in range(cantidad_archivos):
            self.logger.info(cantidad_archivos)
            nombre_mision = random.choice(constants.proyectos)
            fecha = datetime.datetime.now().strftime("%d%m%y%H%M%S")
            tipo_dispositivo = random.choice(constants.lista_dispositivos)
            estado_dispositivo = random.choice(constants.lista_estados)
            hash_calculado = self.calcular_hash(
                fecha, nombre_mision, tipo_dispositivo, estado_dispositivo
            )
            i = 1
            # date_directory = str(datetime.datetime.now().strftime("%d%m%y%H%M%S"))
            # ruta_archivo = os.path.join(self.ruta_devices, date_directory)
            while True:
                nombre_archivo = f"APL{nombre_mision}-0000[{i}].log"
                ruta_archivo = os.path.join(self.ruta_devices, nombre_archivo)
                if not os.path.exists(ruta_archivo):
                    break
                i += 1
            """
            while True:
                nombre_archivo = f"APL{nombre_mision}-0000[{i}].log"
                ruta_archivo = os.path.join(self.ruta_devices, nombre_archivo)
                date_directory = str(datetime.datetime.now().strftime("%d%m%y%H%M%S"))
                directory = os.path.join(self.ruta_devices, date_directory)
                path_save = os.path.join(directory, nombre_archivo)
                os.mkdir(path_save)
                if not os.path.exists(path_save):
                    break
                i += 1
                """

            with open(ruta_archivo, "w") as archivo:
                archivo.write(f"fecha:{fecha}\n")
                archivo.write(f"mision:{nombre_mision}\n")
                archivo.write(f"tipo_dispositivo:{tipo_dispositivo}\n")
                archivo.write(f"estado_dispositivo:{estado_dispositivo}\n")
                archivo.write(f"hash:{hash_calculado}\n")

    def calcular_hash(
        self, fecha: str, mision: str, tipo_dispositivo: str, estado_dispositivo: str
    ):
        if mision != "UNKN":
            datos_para_hash = (
                f"{fecha}{mision}{tipo_dispositivo}{estado_dispositivo}".encode("utf-8")
            )
            return hashlib.sha256(datos_para_hash).hexdigest()
        return ""

    def generar_reportes(self):
        reporte_eventos = self.analizar_eventos()
        reporte_desconexiones = self.gestionar_desconexiones()

        # Crear DataFrames a partir de los reportes
        df_eventos = pd.DataFrame(reporte_eventos)
        df_desconexiones = pd.DataFrame(reporte_desconexiones)

        # Imprimir los DataFrames
        print("Reporte de Eventos:")
        print(df_eventos)
        print("\nReporte de Desconexiones:")
        print(df_desconexiones)

        # Guardar reportes en archivos JSON
        with open(
            os.path.join(self.ruta_devices, "reporte_eventos.json"), "w"
        ) as archivo:
            json.dump(reporte_eventos, archivo)

        with open(
            os.path.join(self.ruta_devices, "reporte_desconexiones.json"), "w"
        ) as archivo:
            json.dump(reporte_desconexiones, archivo)

    def analizar_eventos(self):
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

    def limpiar_archivos_procesados(self):
        fecha_archivo = str(datetime.datetime.now().strftime("%d%m%y%H%M%S"))
        self.ruta_destino = os.path.join(self.ruta_backups, fecha_archivo)
        os.makedirs(self.ruta_destino, exist_ok=True)
        """ archivos_procesados = [
            archivo
            for archivo in os.listdir(self.ruta_devices)
            if archivo.endswith(".log")
            ] """
        archivos_procesados = os.listdir(self.ruta_devices)
        for archivo in archivos_procesados:
            ruta_archivo_origen = os.path.join(self.ruta_devices, archivo)
            ruta_archivo_destino = os.path.join(self.ruta_destino, archivo)
            # if os.path.exists(ruta_archivo_destino):
            #   continue
            shutil.move(ruta_archivo_origen, ruta_archivo_destino)

    def generar_tablero_de_control(self):
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
