from datetime import datetime
from decimal import Decimal, InvalidOperation
import os
from tkinter import messagebox

from modelo.mascota import MascotaModelo

class MascotaControlador:
    def __init__(self):
        self.modelo = MascotaModelo()
        self.ultimo_error = None

    def generar_respaldo_bd(self):
        carpeta_respaldos = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "BD",
                "respaldos"
            )
        )
        nombre_archivo = "respaldo_manual_{}.sql".format(
            datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        )
        ruta_completa = os.path.join(carpeta_respaldos, nombre_archivo)

        try:
            os.makedirs(carpeta_respaldos, exist_ok=True)
            self.modelo.exportar_respaldo_sql(ruta_completa)
            return True, ruta_completa
        except Exception as error:
            return False, "No se pudo generar el respaldo: {}".format(error)

    def guardar_mascota(self, nombre, especie, raza, fecha_nac, sexo, id_propietario=None):
        self.ultimo_error = None
        try:
            if not isinstance(fecha_nac, str):
                raise ValueError
            fecha = datetime.strptime(fecha_nac, "%Y-%m-%d").date()
            if fecha.strftime("%Y-%m-%d") != fecha_nac:
                raise ValueError
        except ValueError:
            self.ultimo_error = "fecha_nacimiento"
            messagebox.showwarning(
                "Fecha de nacimiento no válida",
                "Ingrese una fecha válida con formato YYYY-MM-DD. "
                "No se permiten fechas posteriores al 20/11/2026."
            )
            return False

        if fecha > datetime(2026, 11, 20).date():
            self.ultimo_error = "fecha_nacimiento"
            messagebox.showwarning(
                "Fecha de nacimiento no válida",
                "No se permiten fechas posteriores al 20/11/2026."
            )
            return False

        if not nombre or not especie:
            self.ultimo_error = "Complete el nombre y la especie de la mascota."
            return False

        if id_propietario is not None:
            try:
                id_propietario = int(id_propietario)
                if id_propietario <= 0:
                    raise ValueError
            except (TypeError, ValueError):
                self.ultimo_error = "Seleccione un propietario válido."
                return False

        if id_propietario is None:
            resultado = self.modelo.guardar_mascota(
                nombre, especie, raza, fecha_nac, sexo
            )
        else:
            resultado = self.modelo.guardar_mascota(
                nombre, especie, raza, fecha_nac, sexo, id_propietario
            )
        if not resultado:
            self.ultimo_error = "No fue posible guardar la mascota. Verifique la conexión."
        return resultado

    def listar_mascotas(self):
        return self.modelo.obtener_mascotas()

    def eliminar_mascota(self, id_mascota):
        if not id_mascota:
            return False
        return self.modelo.eliminar_mascota(id_mascota)

    def guardar_propietario(self, nombre, telefono, correo, direccion):
        if not nombre:
            return False
        return self.modelo.guardar_propietario(nombre, telefono, correo, direccion)

    def guardar_cita(self, id_mascota, id_veterinario, id_servicio, fecha_hora, estado):
        self.ultimo_error = None
        if not all((id_mascota, id_veterinario, id_servicio, fecha_hora, estado)):
            self.ultimo_error = "Complete todos los campos de la cita."
            return False

        try:
            ids = (int(id_mascota), int(id_veterinario), int(id_servicio))
            if any(id_valor <= 0 for id_valor in ids):
                raise ValueError
        except (TypeError, ValueError):
            self.ultimo_error = "Los ID de mascota, veterinario y servicio deben ser enteros positivos."
            return False

        try:
            fecha = datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M:%S")
            if fecha.strftime("%Y-%m-%d %H:%M:%S") != fecha_hora:
                raise ValueError
        except (TypeError, ValueError):
            self.ultimo_error = "La fecha y hora debe tener formato YYYY-MM-DD HH:MM:SS."
            return False

        if estado not in ("programada", "atendida", "cancelada"):
            self.ultimo_error = "Seleccione un estado válido para la cita."
            return False

        resultado = self.modelo.guardar_cita(*ids, fecha, estado)
        if not resultado:
            self.ultimo_error = "No fue posible guardar la cita. Verifique la conexión."
        return resultado

    def guardar_historial_clinico(self, id_cita, diagnostico, peso_actual, observaciones):
        self.ultimo_error = None
        if not id_cita or not diagnostico or not peso_actual:
            self.ultimo_error = "Complete el ID de cita, diagnóstico y peso actual."
            return False

        try:
            cita_id = int(id_cita)
            peso = Decimal(str(peso_actual))
            if cita_id <= 0 or not peso.is_finite() or peso <= 0:
                raise ValueError
        except (TypeError, ValueError, InvalidOperation):
            self.ultimo_error = "El ID de cita debe ser positivo y el peso debe ser un decimal mayor que cero."
            return False

        resultado = self.modelo.guardar_historial_clinico(
            cita_id, diagnostico, peso, observaciones
        )
        if not resultado:
            self.ultimo_error = "No fue posible guardar el historial clínico. Verifique la conexión."
        return resultado

    def listar_propietarios(self):
        return self.modelo.listar_propietarios()

    def listar_veterinarios(self):
        return self.modelo.obtener_veterinarios()

    def listar_citas(self):
        return self.modelo.obtener_citas()

    def listar_citas_detalle(self):
        return self.modelo.listar_citas_detalle()

    def listar_historial_clinico(self):
        return self.modelo.obtener_historial_clinico()

    def listar_vacunas(self):
        self.ultimo_error = None
        try:
            return self.modelo.listar_vacunas()
        except Exception as error:
            self.ultimo_error = "No fue posible cargar las vacunas: {}".format(error)
            return []

    def listar_nombres_vacunas_unicos(self):
        self.ultimo_error = None
        try:
            return self.modelo.listar_nombres_vacunas_unicos()
        except Exception as error:
            self.ultimo_error = "No fue posible cargar los nombres de vacunas: {}".format(error)
            return []

    def listar_servicios(self):
        return self.modelo.obtener_servicios()

    def listar_medicamentos(self):
        self.ultimo_error = None
        try:
            return self.modelo.listar_medicamentos()
        except Exception as error:
            self.ultimo_error = "No fue posible cargar los medicamentos: {}".format(error)
            return []

    def listar_citas_pendientes_detalle(self):
        self.ultimo_error = None
        try:
            return self.modelo.listar_citas_pendientes_detalle()
        except Exception as error:
            self.ultimo_error = "No fue posible cargar las citas pendientes: {}".format(error)
            return []

    def registrar_atencion_completa(
        self,
        id_cita,
        diagnostico,
        tratamiento,
        peso_actual,
        observaciones,
        id_medicamento=None,
        dosis=None,
        nombre_vacuna=None,
        fecha_aplicacion=None,
        fecha_proxima_dosis=None
    ):
        self.ultimo_error = None
        if not id_cita or not diagnostico or not diagnostico.strip() or not peso_actual:
            self.ultimo_error = "Seleccione una cita e ingrese el diagnóstico y el peso."
            return False

        try:
            cita_id = int(id_cita)
            peso = Decimal(str(peso_actual))
            if cita_id <= 0 or not peso.is_finite() or peso <= 0:
                raise ValueError
        except (TypeError, ValueError, InvalidOperation):
            self.ultimo_error = "La cita debe ser válida y el peso debe ser un número mayor que cero."
            return False

        if id_medicamento is not None:
            try:
                id_medicamento = int(id_medicamento)
                if id_medicamento <= 0 or not dosis or not dosis.strip():
                    raise ValueError
            except (TypeError, ValueError):
                self.ultimo_error = (
                    "El medicamento requiere un ID válido y sus dosis/indicaciones."
                )
                return False

        if nombre_vacuna is not None:
            try:
                nombre_vacuna = nombre_vacuna.strip()
                if not nombre_vacuna:
                    raise ValueError
                fecha_aplicacion_valida = datetime.strptime(
                    fecha_aplicacion, "%Y-%m-%d"
                ).date()
                fecha_proxima_valida = datetime.strptime(
                    fecha_proxima_dosis, "%Y-%m-%d"
                ).date()
                if (
                    fecha_aplicacion_valida.isoformat() != fecha_aplicacion
                    or fecha_proxima_valida.isoformat() != fecha_proxima_dosis
                    or fecha_proxima_valida <= fecha_aplicacion_valida
                ):
                    raise ValueError
            except (TypeError, ValueError):
                self.ultimo_error = (
                    "Ingrese fechas válidas YYYY-MM-DD y una próxima dosis "
                    "posterior a la fecha de aplicación."
                )
                return False

        try:
            return self.modelo.registrar_atencion_completa(
                cita_id,
                diagnostico.strip(),
                (tratamiento or "").strip(),
                peso,
                (observaciones or "").strip(),
                id_medicamento,
                (dosis or "").strip() if id_medicamento is not None else None,
                nombre_vacuna,
                fecha_aplicacion if nombre_vacuna is not None else None,
                fecha_proxima_dosis if nombre_vacuna is not None else None
            )
        except Exception as error:
            self.ultimo_error = "No fue posible guardar la atención: {}".format(error)
            return False

    def listar_detalles_atencion(self):
        return self.modelo.obtener_detalles_atencion()

    def listar_historial_propietario(self):
        return self.modelo.obtener_historial_propietario()