"""Pruebas del controlador con un modelo falso: no necesitan MySQL.

Ejecutar desde app/:   python -m unittest discover -s tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("MIMASCOTA_ENV", os.devnull)

from controlador.mascota_controlador import ErrorValidacion, MascotaControlador  # noqa: E402


class ModeloFalso:
    def __init__(self):
        self.datos = {}

    def listar(self):
        return list(self.datos.values())

    def buscar_por_codigo(self, code):
        return self.datos.get(code)

    def guardar(self, m):
        m.id = len(self.datos) + 1
        self.datos[m.code] = m
        return m.id

    def actualizar(self, m):
        if m.code not in self.datos:
            return 0
        self.datos[m.code] = m
        return 1

    def contar_por_estado(self):
        return []


def datos(**cambios):
    d = {"code": "006", "name": "Luna", "born_year": "2021", "color": "Café", "health_status": "Healthy"}
    d.update(cambios)
    return d


class TestControlador(unittest.TestCase):
    def setUp(self):
        self.ctrl = MascotaControlador(ModeloFalso())

    def test_guarda_mascota_valida(self):
        self.assertEqual(self.ctrl.guardar(datos()), 1)
        self.assertEqual(self.ctrl.buscar("006").name, "Luna")

    def test_rechaza_codigo_repetido(self):
        self.ctrl.guardar(datos())
        with self.assertRaises(ErrorValidacion):
            self.ctrl.guardar(datos(name="Otra"))

    def test_rechaza_codigo_largo(self):
        with self.assertRaises(ErrorValidacion):
            self.ctrl.guardar(datos(code="0007"))

    def test_rechaza_anio_no_numerico_y_futuro(self):
        for anio in ("dos mil", "1800", "3000"):
            with self.assertRaises(ErrorValidacion):
                self.ctrl.guardar(datos(born_year=anio))

    def test_rechaza_estado_desconocido(self):
        with self.assertRaises(ErrorValidacion):
            self.ctrl.guardar(datos(health_status="Feliz"))

    def test_actualizar_inexistente(self):
        with self.assertRaises(ErrorValidacion):
            self.ctrl.actualizar(datos(code="999"))

    def test_buscar_sin_codigo(self):
        with self.assertRaises(ErrorValidacion):
            self.ctrl.buscar("  ")


if __name__ == "__main__":
    unittest.main()
