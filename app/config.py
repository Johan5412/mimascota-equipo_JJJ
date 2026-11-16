import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo app.env
ruta_env = os.path.join(os.path.dirname(__file__), 'app.env')
load_dotenv(ruta_env)

class Config:
    DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
    DB_PORT = os.environ.get("DB_PORT", "3306")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_NAME = os.environ.get("DB_NAME", "administracionmascotasbd")