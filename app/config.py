"""Configuración de la aplicación.

Las credenciales se leen de un archivo app.env fuera del repositorio
(por defecto C:\\mimascota\\config\\app.env). Nunca se escriben en el código.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

RUTA_ENV = Path(os.environ.get("MIMASCOTA_ENV", r"C:\mimascota\config\app.env"))
load_dotenv(RUTA_ENV)

DB = {
    "host": os.environ.get("DB_HOST", "127.0.0.1"),
    "port": int(os.environ.get("DB_PORT", "3306")),
    "user": os.environ.get("DB_USER", "app_mimascota"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": os.environ.get("DB_NAME", "administracionmascotasbd"),
}

# Script de respaldo de Sistemas Operativos (SO3), usado por el botón "Respaldar ahora"
SCRIPT_RESPALDO = Path(os.environ.get("MIMASCOTA_RESPALDO", r"C:\mimascota\so\windows\respaldo.ps1"))

# Valores que usa la base de partida en tb_pet.health_status
ESTADOS_SALUD = ("Healthy", "Sick", "In Surgery")
