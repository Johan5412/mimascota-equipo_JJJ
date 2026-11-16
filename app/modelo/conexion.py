import mysql.connector
from mysql.connector import Error
from config import Config

class ConexionDB:
    def __init__(self):
        self.conexion = None

    def conectar(self):
        """Establece y retorna la conexión a la base de datos MySQL."""
        try:
            self.conexion = mysql.connector.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME
            )
            if self.conexion.is_connected():
                return self.conexion
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            return None

    def desconectar(self):
        """Cierra la conexión a la base de datos."""
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()