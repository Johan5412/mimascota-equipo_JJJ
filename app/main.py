"""Punto de entrada de MiMascota (app de escritorio, patrón MVC).

Ejecutar desde la carpeta app/:   python main.py
"""
from controlador.mascota_controlador import MascotaControlador
from modelo.mascota import MascotaModelo
from vista.ventana_principal import VentanaPrincipal


def main():
    controlador = MascotaControlador(MascotaModelo())
    VentanaPrincipal(controlador).mainloop()


if __name__ == "__main__":
    main()
