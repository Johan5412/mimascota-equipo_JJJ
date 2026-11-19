import os
import sys
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modelo.mascota import MascotaModelo  # noqa: E402


class CursorFalso:
    def __init__(
        self, fail_on=None, filas=None, columnas=None, resultado_uno=(42,)
    ):
        self.fail_on = fail_on
        self.filas = filas or []
        self.columnas = columnas or []
        self.resultado_uno = resultado_uno
        self.consultas = []
        self.procedimientos = []
        self.lastrowid = 17
        self.rowcount = 1
        self.cerrado = False
        self.ultima_consulta = ""

    def execute(self, sql, valores=None):
        self.consultas.append((sql, valores))
        self.ultima_consulta = sql
        if self.fail_on and self.fail_on in sql:
            raise RuntimeError("error simulado")

    def fetchone(self):
        return self.resultado_uno

    def callproc(self, procedimiento, valores):
        self.procedimientos.append((procedimiento, valores))

    def fetchall(self):
        if self.ultima_consulta.startswith("SHOW COLUMNS"):
            return [(columna,) for columna in self.columnas]
        return self.filas

    def close(self):
        self.cerrado = True


class ConexionFalsa:
    def __init__(self, cursor):
        self.cursor_falso = cursor
        self.confirmada = False
        self.revertida = False

    def cursor(self):
        return self.cursor_falso

    def commit(self):
        self.confirmada = True

    def rollback(self):
        self.revertida = True


class BaseDatosFalsa:
    def __init__(self, conexion):
        self.conexion_falsa = conexion
        self.desconectada = False

    def conectar(self):
        return self.conexion_falsa

    def desconectar(self):
        self.desconectada = True


class TestAtencionVeterinaria(unittest.TestCase):
    def crear_modelo_falso(self, cursor):
        conexion = ConexionFalsa(cursor)
        modelo = MascotaModelo()
        modelo.db = BaseDatosFalsa(conexion)
        return modelo, conexion

    def test_actualiza_cita_antes_de_insertar_historial(self):
        cursor = CursorFalso()
        modelo, conexion = self.crear_modelo_falso(cursor)

        resultado = modelo.registrar_atencion_completa(
            3, "Diagnóstico", 12.5, ""
        )

        sentencias = [consulta[0] for consulta in cursor.consultas]
        posicion_actualizacion = next(
            i for i, sql in enumerate(sentencias) if sql.startswith("UPDATE cita")
        )
        posicion_historial = next(
            i for i, sql in enumerate(sentencias)
            if sql.startswith("INSERT INTO historial_clinico")
        )
        self.assertTrue(resultado)
        self.assertLess(posicion_actualizacion, posicion_historial)
        self.assertTrue(conexion.confirmada)
        self.assertFalse(conexion.revertida)

    def test_revierte_estado_si_falla_el_historial(self):
        cursor = CursorFalso(fail_on="INSERT INTO historial_clinico")
        modelo, conexion = self.crear_modelo_falso(cursor)

        with self.assertRaisesRegex(RuntimeError, "error simulado"):
            modelo.registrar_atencion_completa(3, "Diagnóstico", 12.5, "")

        self.assertTrue(conexion.revertida)
        self.assertFalse(conexion.confirmada)

    def test_programa_cita_con_procedimiento_almacenado(self):
        cursor = CursorFalso()
        modelo, conexion = self.crear_modelo_falso(cursor)

        resultado = modelo.guardar_cita(3, 4, 2, "2026-11-20 09:00:00")

        self.assertTrue(resultado)
        self.assertEqual(
            cursor.procedimientos,
            [("sp_agendar_cita", (3, 4, 2, "2026-11-20 09:00:00"))]
        )
        self.assertTrue(conexion.confirmada)

    def test_cancelar_cita_actualiza_estado_y_confirma(self):
        cursor = CursorFalso(resultado_uno=("programada",))
        modelo, conexion = self.crear_modelo_falso(cursor)

        self.assertTrue(modelo.cancelar_cita(14))

        self.assertEqual(
            cursor.consultas[1],
            (
                "UPDATE cita SET estado = 'cancelada' "
                "WHERE id_cita = %s AND estado = 'programada'",
                (14,)
            )
        )
        self.assertTrue(conexion.confirmada)
        self.assertFalse(conexion.revertida)

    def test_no_cancela_cita_atendida(self):
        cursor = CursorFalso(resultado_uno=("atendida",))
        modelo, conexion = self.crear_modelo_falso(cursor)

        with self.assertRaisesRegex(ValueError, "cita atendida"):
            modelo.cancelar_cita(14)

        self.assertEqual(len(cursor.consultas), 1)
        self.assertTrue(conexion.revertida)
        self.assertFalse(conexion.confirmada)

    def test_guarda_observaciones_sin_prefijo_y_sin_concatenar(self):
        cursor = CursorFalso()
        modelo, _ = self.crear_modelo_falso(cursor)

        modelo.registrar_atencion_completa(
            3, "Diagnóstico", 12.5, "  buen tamaño  "
        )

        insercion = next(
            valores for sql, valores in cursor.consultas
            if sql.startswith("INSERT INTO historial_clinico")
        )
        self.assertEqual(insercion[3], "buen tamaño")

    def test_normaliza_saltos_de_linea_de_historial_antes_de_mostrar(self):
        from vista.ventana_principal import VentanaPrincipal

        fila = (1, 2, "Diagnóstico", 12.5, "Tratamiento\r\nreposo\nObservación\rextra")

        self.assertEqual(
            VentanaPrincipal._normalizar_saltos_linea(fila),
            (1, 2, "Diagnóstico", 12.5, "Tratamiento | reposo | Observación | extra")
        )

    def test_pin_correcto_abre_modulo_veterinario(self):
        from main import SelectorRoles, VentanaVeterinario

        selector = SelectorRoles.__new__(SelectorRoles)
        selector.root = object()
        selector.abrir_modulo = Mock()

        with patch("main.simpledialog.askstring", return_value="2468") as pedir_pin:
            selector.abrir_veterinario()

        pedir_pin.assert_called_once_with(
            "Acceso Veterinario",
            "Ingrese la contraseña del módulo veterinario:",
            show="*",
            parent=selector.root
        )
        selector.abrir_modulo.assert_called_once_with(VentanaVeterinario)

    def test_pin_incorrecto_bloquea_modulo_veterinario(self):
        from main import SelectorRoles

        selector = SelectorRoles.__new__(SelectorRoles)
        selector.root = object()
        selector.abrir_modulo = Mock()

        with patch("main.simpledialog.askstring", return_value="incorrecto"):
            with patch("main.messagebox.showerror") as mostrar_error:
                selector.abrir_veterinario()

        selector.abrir_modulo.assert_not_called()
        mostrar_error.assert_called_once_with(
            "Acceso denegado",
            "Contraseña incorrecta",
            parent=selector.root
        )

    def test_recargar_citas_limpia_seleccion_y_detalle(self):
        from vista.ventana_usuario import VentanaUsuario

        class TreeFalso:
            def __init__(self):
                self.seleccion = ("cita-anterior",)
                self.filas = {"cita-anterior": ()}

            def selection(self):
                return self.seleccion

            def selection_remove(self, *_items):
                self.seleccion = ()

            def get_children(self):
                return tuple(self.filas)

            def delete(self, fila):
                del self.filas[fila]

            def insert(self, _parent, _posicion, values):
                identificador = str(values[0])
                self.filas[identificador] = values

        class ControladorFalso:
            ultimo_error = None

            def listar_citas_gestion(self):
                return [(15, "7 - Mailo", "Perro", "Ana", "300", "Vet", "Consulta", "fecha", "programada")]

        class VariableFalsa:
            valor = ""

            def set(self, valor):
                self.valor = valor

        ventana = VentanaUsuario.__new__(VentanaUsuario)
        ventana.controlador = ControladorFalso()
        ventana.tree_citas = TreeFalso()
        ventana.cita_detalle = VariableFalsa()

        ventana.recargar_citas_gestion()

        self.assertEqual(ventana.tree_citas.seleccion, ())
        self.assertEqual(tuple(ventana.tree_citas.filas), ("15",))
        self.assertEqual(ventana.cita_detalle.valor, "—")

    def test_veterinarios_usa_columnas_reales_del_esquema_legacy(self):
        fila = (1, "Dra. Ejemplo", "TP-12345", "3001234567")
        cursor = CursorFalso(
            filas=[fila],
            columnas=[
                "id_veterinario", "nombre", "tarjeta_profesional", "telefono"
            ]
        )
        modelo, _ = self.crear_modelo_falso(cursor)

        resultado = modelo.obtener_veterinarios()

        self.assertEqual(resultado, [fila])
        self.assertEqual(
            modelo.columnas_veterinarios,
            ("ID", "Nombre", "Tarjeta profesional", "Teléfono")
        )
        self.assertIn(
            "SELECT `id_veterinario`, `nombre`, `tarjeta_profesional`, `telefono` "
            "FROM veterinario",
            cursor.consultas[1][0]
        )

    def test_veterinarios_usa_especialidad_y_email_si_existen(self):
        fila = (1, "Dra. Ejemplo", "Medicina general", "3001234567", "vet@example.com")
        cursor = CursorFalso(
            filas=[fila],
            columnas=[
                "id_veterinario", "nombre", "especialidad", "telefono", "email"
            ]
        )
        modelo, _ = self.crear_modelo_falso(cursor)

        resultado = modelo.obtener_veterinarios()

        self.assertEqual(resultado, [fila])
        self.assertEqual(
            modelo.columnas_veterinarios,
            ("ID", "Nombre", "Especialidad", "Teléfono", "Email")
        )

    def test_selects_de_listados_administrador_corresponden_al_esquema(self):
        casos = (
            (
                "obtener_mascotas",
                "SELECT id_mascota, nombre, especie, raza, fecha_nacimiento, "
                "sexo, estado FROM mascota ORDER BY id_mascota ASC"
            ),
            (
                "listar_propietarios",
                "SELECT id_propietario, nombre, telefono, correo, direccion "
                "FROM propietario ORDER BY id_propietario ASC"
            ),
            (
                "listar_medicamentos",
                "SELECT id_medicamento, nombre_medicamento, stock "
                "FROM medicamento ORDER BY nombre_medicamento ASC, id_medicamento ASC"
            ),
            (
                "obtener_servicios",
                "SELECT id_servicio, nombre_servicio, precio "
                "FROM servicio ORDER BY id_servicio ASC"
            ),
            (
                "obtener_historial_clinico",
                "SELECT hc.id_historial_clinico, hc.id_cita, "
                "CONCAT(m.id_mascota, ' - ', m.nombre) AS mascota, "
                "hc.diagnostico, hc.peso_actual, hc.observaciones "
                "FROM historial_clinico hc "
                "JOIN cita c ON hc.id_cita = c.id_cita "
                "JOIN mascota m ON c.id_mascota = m.id_mascota "
                "ORDER BY hc.id_historial_clinico ASC"
            ),
            (
                "listar_vacunas",
                "SELECT v.id_vacuna, "
                "CONCAT(m.id_mascota, ' - ', m.nombre) AS mascota, "
                "v.nombre_vacuna, v.fecha_aplicacion, v.fecha_proxima_dosis "
                "FROM vacuna v "
                "JOIN mascota m ON v.id_mascota = m.id_mascota "
                "ORDER BY v.id_vacuna ASC"
            ),
            (
                "listar_citas_gestion",
                "SELECT c.id_cita, "
                "CONCAT(m.id_mascota, ' - ', m.nombre) AS mascota, "
                "m.especie, "
                "COALESCE(p.nombre, 'Sin propietario asignado') AS propietario, "
                "COALESCE(p.telefono, '—') AS telefono, "
                "v.nombre AS veterinario, s.nombre_servicio, "
                "c.fecha_hora, c.estado "
                "FROM cita c "
                "JOIN mascota m ON c.id_mascota = m.id_mascota "
                "LEFT JOIN historial_propietario hp "
                "ON m.id_mascota = hp.id_mascota AND hp.fecha_fin IS NULL "
                "LEFT JOIN propietario p ON hp.id_propietario = p.id_propietario "
                "JOIN veterinario v ON c.id_veterinario = v.id_veterinario "
                "JOIN servicio s ON c.id_servicio = s.id_servicio "
                "WHERE c.estado = 'programada' "
                "ORDER BY c.fecha_hora DESC, c.id_cita DESC"
            ),
            (
                "obtener_detalles_atencion",
                "SELECT id_detalle, id_historial_clinico, id_medicamento, dosis "
                "FROM detalle_atencion ORDER BY id_detalle ASC"
            ),
            (
                "obtener_historial_propietario",
                "SELECT hp.id_historial, "
                "CONCAT(m.id_mascota, ' - ', m.nombre) AS mascota, "
                "hp.id_propietario, hp.fecha_inicio, hp.fecha_fin "
                "FROM historial_propietario hp "
                "JOIN mascota m ON hp.id_mascota = m.id_mascota "
                "ORDER BY hp.id_historial ASC"
            ),
            (
                "listar_citas_detalle",
                "SELECT c.id_cita, "
                "CONCAT(m.id_mascota, ' - ', m.nombre) AS mascota, "
                "COALESCE(CAST(hp.id_propietario AS CHAR), 'Sin asignar') "
                "AS id_propietario, c.id_servicio, c.id_veterinario, "
                "c.fecha_hora, c.estado "
                "FROM cita c "
                "JOIN mascota m ON c.id_mascota = m.id_mascota "
                "LEFT JOIN historial_propietario hp "
                "ON c.id_mascota = hp.id_mascota AND hp.fecha_fin IS NULL "
                "ORDER BY c.id_cita ASC"
            )
        )

        for metodo, consulta_esperada in casos:
            with self.subTest(metodo=metodo):
                cursor = CursorFalso(columnas=[])
                modelo, _ = self.crear_modelo_falso(cursor)
                getattr(modelo, metodo)()
                consultas_select = [
                    sql for sql, _ in cursor.consultas
                    if sql.lstrip().upper().startswith("SELECT")
                ]
                self.assertEqual(consultas_select, [consulta_esperada])


if __name__ == "__main__":
    unittest.main()
