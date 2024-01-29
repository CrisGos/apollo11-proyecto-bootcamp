import pytest
import pathlib
import os
from apolo11.simulator import Apolo11Simulator
from apolo11.simulator import FileManager
from apolo11.simulator import DeviceFileManager


class TestApolo11Simulator:
    def test_constructor(self):
        simulator = Apolo11Simulator("testsimulation")
        assert str(simulator.ruta_preferencia) == str(pathlib.Path("testsimulation"))
        assert str(simulator.ruta_devices) == str(
            pathlib.Path("testsimulation/devices")
        )
        assert str(simulator.ruta_backups) == str(
            pathlib.Path("testsimulation/backups")
        )


class TestFileManager:
    def test_file_manager(self):
        file_manager = FileManager("testsimulation")
        assert str(file_manager.ruta_preferencia) == str(pathlib.Path("testsimulation"))

    """  assert str(file_manager.cantidad_archivos) == str(
            pathlib.Path("testsimulation")
        ) """


class TestDeviceFileManager:
    def test_device_file_manager(self):
        device_file_manager = DeviceFileManager("testsimulation")
        assert str(device_file_manager.ruta_preferencia) == str(
            pathlib.Path("testsimulation")
        )

    def test_simular_datos(self):
        device_file_manager = DeviceFileManager("testsimulation")
        device_file_manager.simular_datos(5)
        directorios = os.listdir("testsimulation")
        assert directorios

    def test_generar_datos(self):
        device_file_manager = DeviceFileManager("testsimulation")
        device_file_manager.generar_reportes()
        directory = os.listdir("testsimulation")
        assert directory
