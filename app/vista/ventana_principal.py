"""Vista: ventana principal en Tkinter. Solo muestra datos y avisa al controlador; no tiene SQL."""
import threading
import tkinter as tk
from tkinter import messagebox, ttk

from config import ESTADOS_SALUD
from controlador.mascota_controlador import ErrorValidacion
from modelo.conexion import probar_conexion

CAMPOS = (("code", "Código"), ("name", "Nombre"), ("born_year", "Año de nacimiento"), ("color", "Color"))


class VentanaPrincipal(tk.Tk):
    def __init__(self, controlador):
        super().__init__()
        self.ctrl = controlador
        self.title("MiMascota · Administración de mascotas")
        self.geometry("980x560")
        self.minsize(900, 540)
        self.vars = {clave: tk.StringVar() for clave, _ in CAMPOS}
        self.vars["health_status"] = tk.StringVar(value=ESTADOS_SALUD[0])
        self.estado = tk.StringVar(value="Listo")
        self._construir()
        self.refrescar()

    # ---------- construcción ----------
    def _construir(self):
        form = ttk.LabelFrame(self, text="Mascota", padding=12)
        form.grid(row=0, column=0, sticky="nsw", padx=12, pady=12)
        for i, (clave, texto) in enumerate(CAMPOS):
            ttk.Label(form, text=texto).grid(row=i, column=0, sticky="w", pady=4)
            ttk.Entry(form, textvariable=self.vars[clave], width=24).grid(row=i, column=1, pady=4)
        ttk.Label(form, text="Estado de salud").grid(row=len(CAMPOS), column=0, sticky="w", pady=4)
        ttk.Combobox(form, textvariable=self.vars["health_status"], values=ESTADOS_SALUD,
                     state="readonly", width=21).grid(row=len(CAMPOS), column=1, pady=4)

        botones = ttk.Frame(form)
        botones.grid(row=len(CAMPOS) + 1, column=0, columnspan=2, pady=(12, 0), sticky="ew")
        for texto, accion in (("Guardar", self.guardar), ("Actualizar", self.actualizar),
                              ("Buscar", self.buscar), ("Limpiar", self.limpiar)):
            ttk.Button(botones, text=texto, command=accion).pack(fill="x", pady=2)

        sistema = ttk.LabelFrame(self, text="Sistema", padding=12)
        sistema.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        ttk.Button(sistema, text="Probar conexión", command=self.probar).pack(fill="x", pady=2)
        ttk.Button(sistema, text="Reporte por estado", command=self.reporte).pack(fill="x", pady=2)
        ttk.Button(sistema, text="Respaldar ahora", command=self.respaldar).pack(fill="x", pady=2)

        columnas = ("code", "name", "born_year", "color", "health_status")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings")
        anchos = {"code": 70, "name": 180, "born_year": 70, "color": 120, "health_status": 120}
        for c, t in zip(columnas, ("Código", "Nombre", "Año", "Color", "Estado de salud")):
            self.tabla.heading(c, text=t)
            self.tabla.column(c, width=anchos[c], minwidth=60)
        self.tabla.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(0, 12), pady=12)
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar)

        ttk.Label(self, textvariable=self.estado, relief="sunken", anchor="w").grid(
            row=2, column=0, columnspan=2, sticky="ew")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

    # ---------- acciones ----------
    def _datos(self):
        return {clave: var.get() for clave, var in self.vars.items()}

    def _ejecutar(self, accion, exito):
        try:
            accion()
            self.estado.set(exito)
            self.refrescar()
        except ErrorValidacion as e:
            messagebox.showwarning("Revise los datos", str(e))
        except Exception as e:  # errores de base de datos: se muestran, no se esconden
            messagebox.showerror("Error", str(e))

    def guardar(self):
        self._ejecutar(lambda: self.ctrl.guardar(self._datos()), "Mascota guardada")

    def actualizar(self):
        self._ejecutar(lambda: self.ctrl.actualizar(self._datos()), "Mascota actualizada")

    def buscar(self):
        try:
            m = self.ctrl.buscar(self.vars["code"].get())
        except ErrorValidacion as e:
            messagebox.showwarning("Buscar", str(e))
            return
        if not m:
            self.estado.set("No se encontró esa mascota")
            return
        self._cargar(m)
        self.estado.set(f"Encontrada: {m.name}")

    def limpiar(self):
        for clave, _ in CAMPOS:
            self.vars[clave].set("")
        self.vars["health_status"].set(ESTADOS_SALUD[0])

    def refrescar(self):
        self.tabla.delete(*self.tabla.get_children())
        try:
            for m in self.ctrl.listar():
                self.tabla.insert("", "end", values=(m.code, m.name, m.born_year, m.color, m.health_status))
        except Exception as e:
            self.estado.set(f"No se pudo leer la base: {e}")

    def probar(self):
        ok, msg = probar_conexion()
        self.estado.set(msg)
        (messagebox.showinfo if ok else messagebox.showerror)("Probar conexión", msg)

    def reporte(self):
        try:
            filas = self.ctrl.reporte_estados()
        except Exception as e:
            messagebox.showerror("Reporte", str(e))
            return
        messagebox.showinfo("Mascotas por estado de salud", "\n".join(f"{e}: {n}" for e, n in filas))

    def respaldar(self):
        """El respaldo corre en un hilo para que la ventana no se congele mientras dura."""
        self.estado.set("Respaldando…")

        def trabajo():
            ok, msg = self.ctrl.respaldar_ahora()
            self.after(0, lambda: (self.estado.set(msg),
                                   (messagebox.showinfo if ok else messagebox.showerror)("Respaldo", msg)))

        threading.Thread(target=trabajo, daemon=True).start()

    def _seleccionar(self, _evento):
        sel = self.tabla.selection()
        if sel:
            v = self.tabla.item(sel[0], "values")
            for clave, valor in zip(("code", "name", "born_year", "color", "health_status"), v):
                self.vars[clave].set(valor)

    def _cargar(self, m):
        for clave in ("code", "name", "born_year", "color", "health_status"):
            self.vars[clave].set(getattr(m, clave))
