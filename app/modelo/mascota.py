from datetime import date, datetime, time
from decimal import Decimal
import math

from modelo.conexion import ConexionDB

class MascotaModelo:
    def __init__(self):
        self.db = ConexionDB()
        self.conexion = self.db

    @staticmethod
    def _sql_identificador(identificador):
        return "`{}`".format(str(identificador).replace("`", "``"))

    @staticmethod
    def _sql_valor(valor):
        if valor is None:
            return "NULL"
        if isinstance(valor, bool):
            return "1" if valor else "0"
        if isinstance(valor, (int, Decimal)):
            return str(valor)
        if isinstance(valor, float):
            if not math.isfinite(valor):
                raise ValueError("No se puede exportar un valor numérico no finito.")
            return repr(valor)
        if isinstance(valor, (datetime, date, time)):
            valor = valor.isoformat(sep=" ") if isinstance(valor, datetime) else valor.isoformat()
        if isinstance(valor, bytes):
            return "X'{}'".format(valor.hex())
        texto = str(valor)
        texto = (
            texto.replace("\\", "\\\\")
            .replace("\0", "\\0")
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace("\x1a", "\\Z")
            .replace("'", "''")
        )
        return "'{}'".format(texto)

    def exportar_respaldo_sql(self, ruta_archivo):
        conexion = self.conexion.conectar()
        if not conexion:
            raise RuntimeError("No fue posible conectar con la base de datos.")

        cursor = None
        try:
            cursor = conexion.cursor()
            cursor.execute("SHOW TABLES;")
            tablas = [fila[0] for fila in cursor.fetchall()]

            with open(ruta_archivo, "w", encoding="utf-8", newline="\n") as archivo:
                archivo.write("-- Respaldo SQL de la base de datos MiMascota\n")
                archivo.write("SET FOREIGN_KEY_CHECKS=0;\n\n")

                for tabla in tablas:
                    tabla_sql = self._sql_identificador(tabla)
                    cursor.execute("SHOW CREATE TABLE {};".format(tabla_sql))
                    definicion = cursor.fetchone()
                    if not definicion or len(definicion) < 2:
                        raise RuntimeError(
                            "No fue posible obtener la estructura de la tabla {}.".format(tabla)
                        )

                    cursor.execute("SELECT * FROM {};".format(tabla_sql))
                    registros = cursor.fetchall()
                    columnas = [descripcion[0] for descripcion in cursor.description]
                    columnas_sql = ", ".join(
                        self._sql_identificador(columna) for columna in columnas
                    )

                    archivo.write("DROP TABLE IF EXISTS {};\n".format(tabla_sql))
                    archivo.write("{};\n\n".format(definicion[1].rstrip(";")))

                    if columnas:
                        prefijo_insert = "INSERT INTO {} ({}) VALUES ".format(
                            tabla_sql, columnas_sql
                        )
                        for registro in registros:
                            valores_sql = ", ".join(
                                self._sql_valor(valor) for valor in registro
                            )
                            archivo.write("{}({});\n".format(prefijo_insert, valores_sql))
                        if registros:
                            archivo.write("\n")

                archivo.write("SET FOREIGN_KEY_CHECKS=1;\n")
            return True
        finally:
            try:
                if cursor is not None:
                    cursor.close()
            finally:
                self.conexion.desconectar()

    # 1. mascota
    def obtener_mascotas(self):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM mascota")
                resultado = cursor.fetchall()
                cursor.close()
                self.db.desconectar()
                return resultado
            except Exception as e:
                print(f"Error al obtener mascotas: {e}")
                return []
        return []

    def guardar_mascota(self, nombre, especie, raza, fecha_nac, sexo, id_propietario=None):
        conexion = self.db.conectar()
        if conexion:
            cursor = None
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO mascota (nombre, especie, raza, fecha_nacimiento, sexo) VALUES (%s, %s, %s, %s, %s)"
                valores = (nombre, especie, raza, fecha_nac, sexo)
                cursor.execute(sql, valores)
                id_nueva_mascota = cursor.lastrowid
                if id_propietario is not None:
                    cursor.execute(
                        "INSERT INTO historial_propietario "
                        "(id_mascota, id_propietario, fecha_inicio, fecha_fin) "
                        "VALUES (%s, %s, CURDATE(), NULL)",
                        (id_nueva_mascota, id_propietario)
                    )
                conexion.commit()
                return True
            except Exception as e:
                conexion.rollback()
                print(f"Error al guardar mascota: {e}")
                return False
            finally:
                try:
                    if cursor is not None:
                        cursor.close()
                finally:
                    self.db.desconectar()
        return False

    def eliminar_mascota(self, id_mascota):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                # Aquí está la corrección: id_mascota
                sql = "DELETE FROM mascota WHERE id_mascota = %s"
                cursor.execute(sql, (id_mascota,))
                conexion.commit()
                cursor.close()
                self.db.desconectar()
                return True
            except Exception as e:
                print(f"Error al eliminar mascota: {e}")
                return False
        return False

    # 2. propietario
    def obtener_propietarios(self):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM propietario")
                resultado = cursor.fetchall()
                cursor.close()
                self.db.desconectar()
                return resultado
            except Exception as e:
                print(f"Error al obtener propietarios: {e}")
                return []
        return []

    def listar_propietarios(self):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    "SELECT id_propietario, nombre, telefono, correo, direccion "
                    "FROM propietario ORDER BY id_propietario ASC"
                )
                resultado = cursor.fetchall()
                cursor.close()
                self.db.desconectar()
                return resultado
            except Exception as e:
                print(f"Error al listar propietarios: {e}")
                return []
        return []

    def guardar_propietario(self, nombre, telefono, correo, direccion):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO propietario (nombre, telefono, correo, direccion) VALUES (%s, %s, %s, %s)"
                valores = (nombre, telefono, correo, direccion)
                cursor.execute(sql, valores)
                conexion.commit()
                cursor.close()
                self.db.desconectar()
                return True
            except Exception as e:
                print(f"Error al guardar propietario: {e}")
                return False
        return False

    def guardar_cita(self, id_mascota, id_veterinario, id_servicio, fecha_hora, estado):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO cita (id_mascota, id_veterinario, id_servicio, fecha_hora, estado) VALUES (%s, %s, %s, %s, %s)"
                valores = (id_mascota, id_veterinario, id_servicio, fecha_hora, estado)
                cursor.execute(sql, valores)
                conexion.commit()
                cursor.close()
                self.db.desconectar()
                return True
            except Exception as e:
                print(f"Error al guardar cita: {e}")
                return False
        return False

    def guardar_historial_clinico(self, id_cita, diagnostico, peso_actual, observaciones):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO historial_clinico (id_cita, diagnostico, peso_actual, observaciones) VALUES (%s, %s, %s, %s)"
                valores = (id_cita, diagnostico, peso_actual, observaciones)
                cursor.execute(sql, valores)
                conexion.commit()
                cursor.close()
                self.db.desconectar()
                return True
            except Exception as e:
                print(f"Error al guardar historial clinico: {e}")
                return False
        return False

    # 3. veterinario
    def obtener_veterinarios(self):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM veterinario")
                resultado = cursor.fetchall()
                cursor.close()
                self.db.desconectar()
                return resultado
            except Exception as e:
                print(f"Error al obtener veterinarios: {e}")
                return []
        return []

    # 4. cita
    def obtener_citas(self):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM cita")
                resultado = cursor.fetchall()
                cursor.close()
                self.db.desconectar()
                return resultado
            except Exception as e:
                print(f"Error al obtener citas: {e}")
                return []
        return []

    def listar_citas_pendientes_detalle(self):
        conexion = self.db.conectar()
        if not conexion:
            raise RuntimeError("No fue posible conectar con la base de datos.")

        cursor = None
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT c.id_cita, c.fecha_hora, m.id_mascota, m.nombre, "
                "m.especie, m.raza, m.fecha_nacimiento, s.nombre_servicio, "
                "p.nombre, p.telefono "
                "FROM cita c "
                "JOIN mascota m ON c.id_mascota = m.id_mascota "
                "JOIN servicio s ON c.id_servicio = s.id_servicio "
                "LEFT JOIN historial_propietario hp "
                "ON m.id_mascota = hp.id_mascota AND hp.fecha_fin IS NULL "
                "LEFT JOIN propietario p ON hp.id_propietario = p.id_propietario "
                "WHERE c.estado = 'programada' "
                "ORDER BY c.fecha_hora ASC, c.id_cita ASC"
            )
            return cursor.fetchall()
        finally:
            try:
                if cursor is not None:
                    cursor.close()
            finally:
                self.db.desconectar()

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
        conexion = self.db.conectar()
        if not conexion:
            raise RuntimeError("No fue posible conectar con la base de datos.")

        cursor = None
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id_mascota FROM cita "
                "WHERE id_cita = %s AND estado = 'programada' FOR UPDATE",
                (id_cita,)
            )
            cita = cursor.fetchone()
            if not cita:
                raise ValueError("La cita no existe o ya fue atendida.")
            id_mascota = cita[0]

            observaciones_historial = []
            if tratamiento:
                observaciones_historial.append("Tratamiento: {}".format(tratamiento))
            if observaciones:
                observaciones_historial.append(
                    "Observaciones: {}".format(observaciones)
                )
            texto_observaciones = "\n".join(observaciones_historial) or None

            cursor.execute(
                "INSERT INTO historial_clinico "
                "(id_cita, diagnostico, peso_actual, observaciones) "
                "VALUES (%s, %s, %s, %s)",
                (id_cita, diagnostico, peso_actual, texto_observaciones)
            )
            id_historial_clinico = cursor.lastrowid

            if id_medicamento is not None:
                cursor.execute(
                    "INSERT INTO detalle_atencion "
                    "(id_historial_clinico, id_medicamento, dosis) "
                    "VALUES (%s, %s, %s)",
                    (id_historial_clinico, id_medicamento, dosis)
                )

            if nombre_vacuna is not None:
                cursor.execute(
                    "INSERT INTO vacuna "
                    "(id_mascota, nombre_vacuna, fecha_aplicacion, "
                    "fecha_proxima_dosis) VALUES (%s, %s, %s, %s)",
                    (
                        id_mascota,
                        nombre_vacuna,
                        fecha_aplicacion,
                        fecha_proxima_dosis
                    )
                )

            cursor.execute(
                "UPDATE cita SET estado = 'atendida' WHERE id_cita = %s",
                (id_cita,)
            )
            conexion.commit()
            return True
        except Exception:
            conexion.rollback()
            raise
        finally:
            try:
                if cursor is not None:
                    cursor.close()
            finally:
                self.db.desconectar()

    def listar_citas_detalle(self):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    "SELECT c.id_cita, "
                    "c.id_mascota, "
                    "COALESCE(CAST(hp.id_propietario AS CHAR), 'Sin asignar') "
                    "AS id_propietario, "
                    "c.id_servicio, "
                    "c.id_veterinario, "
                    "c.fecha_hora, "
                    "c.estado "
                    "FROM cita c "
                    "LEFT JOIN historial_propietario hp "
                    "ON c.id_mascota = hp.id_mascota "
                    "ORDER BY c.id_cita ASC"
                )
                resultado = cursor.fetchall()
                cursor.close()
                self.db.desconectar()
                return resultado
            except Exception as e:
                print(f"Error al obtener detalle de citas: {e}")
                return []
        return []

    # 5. historial_clinico
    def obtener_historial_clinico(self):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM historial_clinico")
                resultado = cursor.fetchall()
                cursor.close()
                self.db.desconectar()
                return resultado
            except Exception as e:
                print(f"Error al obtener historial clinico: {e}")
                return []
        return []

    # 6. vacuna
    def obtener_vacunas(self):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM vacuna")
                resultado = cursor.fetchall()
                cursor.close()
                self.db.desconectar()
                return resultado
            except Exception as e:
                print(f"Error al obtener vacunas: {e}")
                return []
        return []

    def listar_vacunas(self):
        conexion = self.db.conectar()
        if not conexion:
            raise RuntimeError("No fue posible conectar con la base de datos.")

        cursor = None
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id_vacuna, id_mascota, nombre_vacuna, "
                "fecha_aplicacion, fecha_proxima_dosis "
                "FROM vacuna ORDER BY id_vacuna ASC"
            )
            return cursor.fetchall()
        finally:
            try:
                if cursor is not None:
                    cursor.close()
            finally:
                self.db.desconectar()

    def listar_nombres_vacunas_unicos(self):
        conexion = self.db.conectar()
        if not conexion:
            raise RuntimeError("No fue posible conectar con la base de datos.")

        cursor = None
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT DISTINCT nombre_vacuna FROM vacuna "
                "WHERE nombre_vacuna IS NOT NULL AND nombre_vacuna != '' "
                "ORDER BY nombre_vacuna ASC"
            )
            return cursor.fetchall()
        finally:
            try:
                if cursor is not None:
                    cursor.close()
            finally:
                self.db.desconectar()

    # 7. servicio
    def obtener_servicios(self):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM servicio")
                resultado = cursor.fetchall()
                cursor.close()
                self.db.desconectar()
                return resultado
            except Exception as e:
                print(f"Error al obtener servicios: {e}")
                return []
        return []

    # 8. medicamento
    def obtener_medicamentos(self):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM medicamento")
                resultado = cursor.fetchall()
                cursor.close()
                self.db.desconectar()
                return resultado
            except Exception as e:
                print(f"Error al obtener medicamentos: {e}")
                return []
        return []

    def listar_medicamentos(self):
        conexion = self.db.conectar()
        if not conexion:
            raise RuntimeError("No fue posible conectar con la base de datos.")

        cursor = None
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id_medicamento, nombre_medicamento, stock "
                "FROM medicamento ORDER BY nombre_medicamento ASC, id_medicamento ASC"
            )
            return cursor.fetchall()
        finally:
            try:
                if cursor is not None:
                    cursor.close()
            finally:
                self.db.desconectar()

    # 9. detalle_atencion
    def obtener_detalles_atencion(self):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM detalle_atencion")
                resultado = cursor.fetchall()
                cursor.close()
                self.db.desconectar()
                return resultado
            except Exception as e:
                print(f"Error al obtener detalles de atencion: {e}")
                return []
        return []

    # 10. historial_propietario
    def obtener_historial_propietario(self):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM historial_propietario")
                resultado = cursor.fetchall()
                cursor.close()
                self.db.desconectar()
                return resultado
            except Exception as e:
                print(f"Error al obtener historial propietario: {e}")
                return []
        return []