"""Modelo: acceso a la tabla tb_pet. Aquí va todo el SQL; ni la vista ni el controlador lo tienen."""
from dataclasses import dataclass
from typing import Optional

from modelo.conexion import conectar


@dataclass
class Mascota:
    code: str
    name: str
    born_year: int
    color: str
    health_status: str
    id: Optional[int] = None


class MascotaModelo:
    """Repositorio de mascotas. Todas las consultas usan parámetros (%s), nunca texto concatenado."""

    def __init__(self, conectar_fn=conectar):
        self._conectar = conectar_fn

    def listar(self):
        return self._consultar(
            "SELECT id, code, name, born_year, color, health_status FROM tb_pet ORDER BY code")

    def buscar_por_codigo(self, code):
        filas = self._consultar(
            "SELECT id, code, name, born_year, color, health_status FROM tb_pet WHERE code = %s", (code,))
        return filas[0] if filas else None

    def contar_por_estado(self):
        """Reporte por estado de salud (como el prototipo Pet Manager)."""
        cnx = self._conectar()
        try:
            cur = cnx.cursor()
            cur.execute("SELECT health_status, COUNT(*) FROM tb_pet GROUP BY health_status ORDER BY health_status")
            return cur.fetchall()
        finally:
            cnx.close()

    def guardar(self, m: Mascota):
        """Inserta y devuelve el id nuevo (tb_pet.id es AUTO_INCREMENT)."""
        cnx = self._conectar()
        try:
            cur = cnx.cursor()
            cur.execute(
                "INSERT INTO tb_pet (code, name, born_year, color, health_status) VALUES (%s, %s, %s, %s, %s)",
                (m.code, m.name, m.born_year, m.color, m.health_status))
            cnx.commit()
            return cur.lastrowid
        except Exception:
            cnx.rollback()
            raise
        finally:
            cnx.close()

    def actualizar(self, m: Mascota):
        cnx = self._conectar()
        try:
            cur = cnx.cursor()
            cur.execute(
                "UPDATE tb_pet SET name = %s, born_year = %s, color = %s, health_status = %s WHERE code = %s",
                (m.name, m.born_year, m.color, m.health_status, m.code))
            cnx.commit()
            return cur.rowcount
        finally:
            cnx.close()

    def _consultar(self, sql, params=()):
        cnx = self._conectar()
        try:
            cur = cnx.cursor()
            cur.execute(sql, params)
            return [Mascota(id=f[0], code=f[1], name=f[2], born_year=f[3], color=f[4], health_status=f[5])
                    for f in cur.fetchall()]
        finally:
            cnx.close()
