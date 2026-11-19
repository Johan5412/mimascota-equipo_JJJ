import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from vista.ventana_principal import VentanaPrincipal
from vista.ventana_usuario import VentanaUsuario
from vista.ventana_veterinario import VentanaVeterinario
from vista.estilos import aplicar_estilos, crear_banner


class SelectorRoles:
    def __init__(self, root):
        self.root = root
        self.ventana_activa = None
        self.root.title("Sistema de Gestión - MiMascota")
        self.root.geometry("760x700")
        self.root.minsize(680, 620)
        aplicar_estilos(self.root)

        crear_banner(root, "Seleccione un módulo para continuar")
        contenedor = ttk.Frame(root, padding=(32, 24))
        contenedor.pack(expand=True, fill="both")
        ttk.Label(
            contenedor,
            text="Acceso al sistema",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", pady=(0, 12))

        roles = (
            (
                "Usuario / Recepción",
                "Registre propietarios, mascotas y citas de atención.",
                VentanaUsuario,
                "Primario.TButton"
            ),
            (
                "Veterinario",
                "Consulte las citas pendientes y registre la atención clínica.",
                VentanaVeterinario,
                "Primario.TButton"
            ),
            (
                "Administrador",
                "Gestione catálogos, registros y respaldos de la base de datos.",
                VentanaPrincipal,
                "Secundario.TButton"
            )
        )
        for titulo, descripcion, ventana, estilo in roles:
            tarjeta = ttk.Frame(
                contenedor,
                style="Card.TFrame",
                padding=(18, 12)
            )
            tarjeta.pack(fill="x", pady=7)
            ttk.Label(
                tarjeta,
                text=titulo,
                style="CardTitle.TLabel"
            ).pack(anchor="w")
            ttk.Label(
                tarjeta,
                text=descripcion,
                style="CardDescription.TLabel",
                wraplength=600
            ).pack(anchor="w", pady=(3, 10))
            if ventana is VentanaPrincipal:
                comando = self.abrir_administrador
            elif ventana is VentanaVeterinario:
                comando = self.abrir_veterinario
            else:
                comando = lambda clase=ventana: self.abrir_modulo(clase)
            ttk.Button(
                tarjeta,
                text="Ingresar",
                style=estilo,
                command=comando
            ).pack(anchor="e")

    def abrir_administrador(self):
        contraseña = simpledialog.askstring(
            "Acceso Administrador",
            "Ingrese la contraseña de administrador:",
            show="*"
        )
        if contraseña is None:
            return
        if contraseña == "12345":
            self.abrir_modulo(VentanaPrincipal)
        else:
            messagebox.showerror(
                "Acceso Denegado",
                "Contraseña incorrecta."
            )

    def abrir_veterinario(self):
        contraseña = simpledialog.askstring(
            "Acceso Veterinario",
            "Ingrese la contraseña del módulo veterinario:",
            show="*",
            parent=self.root
        )
        if contraseña is None:
            return
        if contraseña == "2468":
            self.abrir_modulo(VentanaVeterinario)
        else:
            messagebox.showerror(
                "Acceso denegado",
                "Contraseña incorrecta",
                parent=self.root
            )

    def abrir_modulo(self, clase_ventana):
        self.root.withdraw()
        modulo = tk.Toplevel(self.root)
        self.ventana_activa = clase_ventana(
            modulo, on_return=self.root.deiconify
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = SelectorRoles(root)
    root.mainloop()