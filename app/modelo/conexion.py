"""Conexión a MySQL con el usuario de la aplicación (BD6: privilegios mínimos)."""
import mysql.connector

from config import DB


def conectar():
    """Abre una conexión nueva. Quien la abre, la cierra."""
    return mysql.connector.connect(**DB)


def probar_conexion():
    """Devuelve (ok, mensaje). Lo usa el botón «Probar conexión».

    Si falla, lo más probable es que el servicio MySQL esté detenido (SO2).
    """
    try:
        cnx = conectar()
        try:
            cur = cnx.cursor()
            cur.execute("SELECT VERSION()")
            version = cur.fetchone()[0]
        finally:
            cnx.close()
        return True, f"Conectado a MySQL {version} en {DB['host']}:{DB['port']} como {DB['user']}"
    except mysql.connector.Error as err:
        return False, f"No hay conexión con MySQL: {err.msg}. ¿Está corriendo el servicio?"
