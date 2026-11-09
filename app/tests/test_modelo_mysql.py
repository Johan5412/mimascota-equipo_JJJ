"""Prueba de integración del modelo contra MySQL real.

Solo corre si existe la variable MIMASCOTA_TEST_DB=1 y app.env apunta a una base de PRUEBA
(nunca a la base de producción: la prueba inserta y actualiza una mascota con código 'T01').
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@unittest.skipUnless(os.environ.get("MIMASCOTA_TEST_DB") == "1", "Defina MIMASCOTA_TEST_DB=1 para probar contra MySQL")
class TestModeloMySQL(unittest.TestCase):
    def setUp(self):
        from modelo.mascota import Mascota, MascotaModelo
        self.Mascota = Mascota
        self.modelo = MascotaModelo()

    def test_ciclo_guardar_buscar_actualizar(self):
        if self.modelo.buscar_por_codigo("T01") is None:
            self.modelo.guardar(self.Mascota(code="T01", name="Prueba", born_year=2020, color="Gris",
                                             health_status="Healthy"))
        self.assertEqual(self.modelo.buscar_por_codigo("T01").name, "Prueba")
        self.modelo.actualizar(self.Mascota(code="T01", name="Prueba", born_year=2020, color="Gris",
                                            health_status="Sick"))
        self.assertEqual(self.modelo.buscar_por_codigo("T01").health_status, "Sick")
        estados = dict(self.modelo.contar_por_estado())
        self.assertGreaterEqual(estados.get("Sick", 0), 1)


if __name__ == "__main__":
    unittest.main()
