"""Controlador: valida lo que llega de la vista y llama al modelo. No tiene SQL ni widgets."""
import datetime
import platform
import subprocess

from config import ESTADOS_SALUD, SCRIPT_RESPALDO
from modelo.mascota import Mascota


class ErrorValidacion(ValueError):
    """Dato inválido escrito por el usuario."""


class MascotaControlador:
    def __init__(self, modelo):
        self.modelo = modelo

    def listar(self):
        return self.modelo.listar()

    def buscar(self, code):
        code = (code or "").strip()
        if not code:
            raise ErrorValidacion("Escriba el código de la mascota")
        return self.modelo.buscar_por_codigo(code)

    def guardar(self, datos):
        m = self._validar(datos)
        if self.modelo.buscar_por_codigo(m.code):
            raise ErrorValidacion(f"Ya existe una mascota con el código {m.code}")
        return self.modelo.guardar(m)

    def actualizar(self, datos):
        m = self._validar(datos)
        if self.modelo.actualizar(m) == 0:
            raise ErrorValidacion(f"No existe una mascota con el código {m.code}")

    def reporte_estados(self):
        return self.modelo.contar_por_estado()

    def respaldar_ahora(self):
        """Ejecuta respaldo.ps1 (SO3) como proceso hijo y devuelve (ok, última línea de la salida)."""
        if platform.system() != "Windows":
            return False, "El respaldo manual solo está disponible en Windows"
        if not SCRIPT_RESPALDO.exists():
            return False, f"No se encontró {SCRIPT_RESPALDO}"
        r = subprocess.run(
            ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(SCRIPT_RESPALDO)],
            capture_output=True, text=True, timeout=300)
        lineas = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
        return r.returncode == 0, (lineas[-1] if lineas else f"Código de salida {r.returncode}")

    @staticmethod
    def _validar(d):
        code = (d.get("code") or "").strip()
        name = (d.get("name") or "").strip()
        color = (d.get("color") or "").strip()
        estado = (d.get("health_status") or "").strip()
        if len(code) == 0 or len(code) > 3:
            raise ErrorValidacion("El código debe tener entre 1 y 3 caracteres")
        if not name or len(name) > 50:
            raise ErrorValidacion("El nombre es obligatorio (máximo 50 caracteres)")
        if not color or len(color) > 20:
            raise ErrorValidacion("El color es obligatorio (máximo 20 caracteres)")
        try:
            anio = int(str(d.get("born_year", "")).strip())
        except ValueError:
            raise ErrorValidacion("El año de nacimiento debe ser un número") from None
        if not 1990 <= anio <= datetime.date.today().year:
            raise ErrorValidacion(f"El año de nacimiento debe estar entre 1990 y {datetime.date.today().year}")
        if estado not in ESTADOS_SALUD:
            raise ErrorValidacion("Estado de salud inválido: " + ", ".join(ESTADOS_SALUD))
        return Mascota(code=code, name=name, born_year=anio, color=color, health_status=estado)
