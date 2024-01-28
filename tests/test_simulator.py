import pytest
import pathlib
from apolo11.simulator import Apolo11Simulator


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
