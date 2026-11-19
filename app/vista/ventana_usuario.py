import tkinter as tk
from tkinter import messagebox, ttk

from controlador.mascota_controlador import MascotaControlador
from vista.estilos import aplicar_estilos, crear_banner


class VentanaUsuario:
    def __init__(self, root, on_return=None):
        self.root = root
        self.on_return = on_return
        self.controlador = MascotaControlador()

        self.root.title("MiMascota - Recepción")
        self.root.geometry("760x620")
        self.root.minsize(680, 560)
        aplicar_estilos(self.root)

        crear_banner(self.root, "Módulo de Recepción y Citas")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=22, pady=10)
        self._crear_formulario_propietario()
        self._crear_formulario_mascota()
        self._crear_formulario_cita()
        self._crear_gestion_citas()
        self.recargar_propietarios()
        self.recargar_mascotas()
        self.recargar_veterinarios()
        self.recargar_servicios()
        self.recargar_citas_gestion()

        ttk.Button(
            self.root,
            text="Cambiar Rol / Volver al Inicio",
            style="Secundario.TButton",
            command=self.volver_inicio
        ).pack(anchor="e", padx=22, pady=(0, 18))
        self.root.protocol("WM_DELETE_WINDOW", self.volver_inicio)

    def _crear_pestana(self, titulo):
        pestaña = ttk.Frame(self.notebook, padding=24)
        self.notebook.add(pestaña, text=titulo)
        pestaña.columnconfigure(0, weight=1)
        return pestaña

    def _agregar_campo(self, parent, etiqueta, fila, valores=None):
        ttk.Label(parent, text=etiqueta).grid(
            row=fila * 2, column=0, sticky="w", pady=(8, 3)
        )
        if valores is None:
            campo = ttk.Entry(parent)
        else:
            campo = ttk.Combobox(parent, values=valores, state="readonly")
        campo.grid(row=fila * 2 + 1, column=0, sticky="ew")
        return campo

    def _crear_formulario_propietario(self):
        form = self._crear_pestana("Propietario")
        self.prop_nombre = self._agregar_campo(form, "Nombre", 0)
        self.prop_telefono = self._agregar_campo(form, "Teléfono", 1)
        self.prop_correo = self._agregar_campo(form, "Correo", 2)
        self.prop_direccion = self._agregar_campo(form, "Dirección", 3)
        ttk.Button(
            form,
            text="Guardar Propietario",
            style="Primario.TButton",
            command=self.guardar_propietario
        ).grid(row=8, column=0, sticky="ew", pady=(20, 0))

    def _crear_formulario_mascota(self):
        form = self._crear_pestana("Mascota")
        self.mascota_nombre = self._agregar_campo(form, "Nombre", 0)
        self.mascota_especie = self._agregar_campo(form, "Especie", 1)
        self.mascota_raza = self._agregar_campo(form, "Raza", 2)
        self.mascota_fecha = self._agregar_campo(
            form, "Fecha de Nacimiento (YYYY-MM-DD)", 3
        )
        self.mascota_sexo = self._agregar_campo(
            form, "Sexo", 4, ("Macho", "Hembra")
        )
        self.mascota_sexo.set("Macho")
        self.mascota_propietario = self._agregar_campo(
            form, "Propietario", 5, ()
        )
        ttk.Button(
            form,
            text="Guardar Mascota",
            style="Primario.TButton",
            command=self.guardar_mascota
        ).grid(row=12, column=0, sticky="ew", pady=(20, 0))

    def _crear_formulario_cita(self):
        form = self._crear_pestana("Programar Cita")
        self.cita_mascota = self._agregar_campo(
            form, "Mascota", 0, ()
        )
        self.cita_veterinario = self._agregar_campo(
            form, "Veterinario", 1, ()
        )
        self.cita_servicio = self._agregar_campo(
            form, "Servicio", 2, ()
        )
        self.cita_fecha = self._agregar_campo(
            form, "Fecha y Hora (YYYY-MM-DD HH:MM:SS)", 3
        )
        ttk.Button(
            form,
            text="Guardar Cita",
            style="Primario.TButton",
            command=self.guardar_cita
        ).grid(row=8, column=0, sticky="ew", pady=(20, 0))

    def _crear_gestion_citas(self):
        form = self._crear_pestana("Gestionar Citas")
        form.columnconfigure(0, weight=1)
        form.rowconfigure(0, weight=1)

        columnas = (
            "ID",
            "Mascota",
            "Especie",
            "Propietario",
            "Teléfono",
            "Veterinario",
            "Servicio",
            "Fecha y Hora",
            "Estado"
        )
        self.tree_citas = ttk.Treeview(
            form,
            columns=columnas,
            show="headings",
            height=8
        )
        for columna, ancho in zip(
            columnas, (55, 125, 85, 140, 95, 140, 120, 140, 85)
        ):
            self.tree_citas.heading(columna, text=columna)
            self.tree_citas.column(columna, width=ancho, anchor="center")
        self.tree_citas.grid(row=0, column=0, sticky="nsew")
        self.tree_citas.bind(
            "<<TreeviewSelect>>", self._al_seleccionar_cita_existente
        )

        scrollbar_vertical = ttk.Scrollbar(
            form, orient="vertical", command=self.tree_citas.yview
        )
        scrollbar_vertical.grid(row=0, column=1, sticky="ns")
        scrollbar_horizontal = ttk.Scrollbar(
            form, orient="horizontal", command=self.tree_citas.xview
        )
        scrollbar_horizontal.grid(row=1, column=0, sticky="ew")
        self.tree_citas.configure(
            yscrollcommand=scrollbar_vertical.set,
            xscrollcommand=scrollbar_horizontal.set
        )

        detalle = ttk.LabelFrame(form, text="Información de la cita", padding=10)
        detalle.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        self.cita_detalle = tk.StringVar(value="—")
        ttk.Label(
            detalle,
            textvariable=self.cita_detalle,
            justify="left",
            wraplength=900
        ).pack(anchor="w", fill="x")

        ttk.Button(
            form,
            text="Cancelar Cita",
            style="Peligro.TButton",
            command=self.cancelar_cita
        ).grid(row=3, column=0, columnspan=2, sticky="e", pady=(10, 0))

    def recargar_citas_gestion(self):
        citas = self.controlador.listar_citas_gestion()
        if self.controlador.ultimo_error:
            messagebox.showerror(
                "Error al cargar citas",
                self.controlador.ultimo_error,
                parent=self.root
            )
            return

        seleccion = self.tree_citas.selection()
        if seleccion:
            self.tree_citas.selection_remove(*seleccion)
        for fila in self.tree_citas.get_children():
            self.tree_citas.delete(fila)
        for cita in citas:
            self.tree_citas.insert("", "end", values=cita)
        self.cita_detalle.set("—")

    def _al_seleccionar_cita_existente(self, _evento):
        seleccion = self.tree_citas.selection()
        if not seleccion:
            self.cita_detalle.set("—")
            return

        cita = self.tree_citas.item(seleccion[0], "values")
        self.cita_detalle.set(
            "ID de cita: {0}\n"
            "Mascota: {1} (especie: {2})\n"
            "Propietario: {3} | Teléfono: {4}\n"
            "Veterinario: {5}\n"
            "Servicio: {6}\n"
            "Fecha y hora: {7}\n"
            "Estado: {8}".format(*cita)
        )

    def cancelar_cita(self):
        seleccion = self.tree_citas.selection()
        if not seleccion:
            messagebox.showwarning(
                "Cita no seleccionada",
                "Seleccione una cita para cancelar.",
                parent=self.root
            )
            return

        cita = self.tree_citas.item(seleccion[0], "values")
        id_cita = int(cita[0])
        estado = str(cita[8]).lower()
        if estado == "atendida":
            messagebox.showerror(
                "Acción no permitida",
                "No se puede cancelar una cita atendida.",
                parent=self.root
            )
            return
        if estado == "cancelada":
            messagebox.showinfo(
                "Cita cancelada",
                "La cita ya está cancelada.",
                parent=self.root
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar cancelación",
            "¿Está seguro de que desea cancelar la cita {}?".format(id_cita),
            parent=self.root
        )
        if not confirmar:
            return

        if not self.controlador.cancelar_cita(id_cita):
            messagebox.showerror(
                "No se pudo cancelar la cita",
                self.controlador.ultimo_error or "Verifique la cita e inténtelo nuevamente.",
                parent=self.root
            )
            return

        self.recargar_citas_gestion()
        messagebox.showinfo(
            "Cita cancelada",
            "La cita se canceló correctamente.",
            parent=self.root
        )

    def recargar_mascotas(self):
        mascotas = self.controlador.listar_mascotas() or []
        opciones = [
            f"{mascota[0]} - {mascota[1]}"
            for mascota in mascotas
            if len(mascota) > 1
        ]
        self.cita_mascota.configure(values=opciones)
        self.cita_mascota.set("")

    def recargar_propietarios(self):
        propietarios = self.controlador.listar_propietarios() or []
        opciones = [
            f"{propietario[0]} - {propietario[1]}"
            for propietario in propietarios
            if len(propietario) > 1
        ]
        self.mascota_propietario.configure(values=opciones)
        self.mascota_propietario.set("")

    def recargar_veterinarios(self):
        veterinarios = self.controlador.listar_veterinarios() or []
        opciones = [
            f"{veterinario[0]} - {veterinario[1]}"
            for veterinario in veterinarios
            if len(veterinario) > 1
        ]
        self.cita_veterinario.configure(values=opciones)
        self.cita_veterinario.set("")

    def recargar_servicios(self):
        servicios = self.controlador.listar_servicios() or []
        opciones = [
            f"{servicio[0]} - {servicio[1]}"
            for servicio in servicios
            if len(servicio) > 1
        ]
        self.cita_servicio.configure(values=opciones)
        self.cita_servicio.set("")

    def guardar_propietario(self):
        valores = (
            self.prop_nombre.get().strip(),
            self.prop_telefono.get().strip(),
            self.prop_correo.get().strip(),
            self.prop_direccion.get().strip()
        )
        if not valores[0] or not valores[1]:
            messagebox.showwarning(
                "Datos incompletos",
                "El nombre y el teléfono del propietario son obligatorios."
            )
            return
        if self.controlador.guardar_propietario(*valores):
            messagebox.showinfo("Éxito", "Propietario guardado.")
            for campo in (self.prop_nombre, self.prop_telefono, self.prop_correo, self.prop_direccion):
                campo.delete(0, tk.END)
            self.recargar_propietarios()
        else:
            messagebox.showerror("Error", "No se pudo guardar el propietario. Verifique la conexión.")

    def guardar_mascota(self):
        seleccion_propietario = self.mascota_propietario.get().strip()
        if not seleccion_propietario:
            messagebox.showwarning(
                "Datos incompletos",
                "Seleccione un propietario para la mascota."
            )
            return

        res = self.controlador.guardar_mascota(
            self.mascota_nombre.get().strip(),
            self.mascota_especie.get().strip(),
            self.mascota_raza.get().strip(),
            self.mascota_fecha.get().strip(),
            self.mascota_sexo.get(),
            int(seleccion_propietario.split(" - ")[0])
        )
        if res:
            messagebox.showinfo("Éxito", "Mascota guardada.")
            for campo in (self.mascota_nombre, self.mascota_especie, self.mascota_raza, self.mascota_fecha):
                campo.delete(0, tk.END)
            self.mascota_sexo.set("Macho")
            self.mascota_propietario.set("")
            self.recargar_mascotas()
        elif self.controlador.ultimo_error != "fecha_nacimiento":
            messagebox.showwarning(
                "No se pudo guardar",
                self.controlador.ultimo_error or "Verifique los campos y vuelva a intentarlo."
            )

    def guardar_cita(self):
        seleccion_mascota = self.cita_mascota.get().strip()
        seleccion_veterinario = self.cita_veterinario.get().strip()
        seleccion_servicio = self.cita_servicio.get().strip()
        if not all((seleccion_mascota, seleccion_veterinario, seleccion_servicio)):
            messagebox.showwarning(
                "Datos incompletos",
                "Seleccione una mascota, un veterinario y un servicio."
            )
            return

        res = self.controlador.guardar_cita(
            int(seleccion_mascota.split(" - ")[0]),
            int(seleccion_veterinario.split(" - ")[0]),
            int(seleccion_servicio.split(" - ")[0]),
            self.cita_fecha.get().strip()
        )
        if res:
            messagebox.showinfo("Éxito", "Cita guardada.")
            for campo in (self.cita_mascota, self.cita_veterinario, self.cita_servicio):
                campo.set("")
            self.cita_fecha.delete(0, tk.END)
            self.recargar_citas_gestion()
        else:
            messagebox.showwarning(
                "No se pudo guardar",
                self.controlador.ultimo_error or "Verifique los campos y vuelva a intentarlo."
            )

    def volver_inicio(self):
        self.root.destroy()
        if self.on_return is not None:
            self.on_return()
