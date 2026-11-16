from tkinter import ttk, messagebox
from controlador.mascota_controlador import MascotaControlador
from vista.estilos import aplicar_estilos, aplicar_zebra_treeview, crear_banner, insertar_filas_zebra

class VentanaPrincipal:
    def __init__(self, root, on_return=None):
        self.root = root
        self.on_return = on_return
        self.root.title("Sistema de Gestión - MiMascota")
        self.root.geometry("1000x650")
        aplicar_estilos(self.root)
        self.controlador = MascotaControlador()

        crear_banner(self.root, "Módulo Administrador")
        barra_superior = ttk.Frame(self.root, padding=(10, 8))
        barra_superior.pack(fill="x")
        ttk.Button(
            barra_superior,
            text="Cambiar Rol / Volver al Inicio",
            style="Secundario.TButton",
            command=self.volver_inicio
        ).pack(side="right")
        ttk.Button(
            barra_superior,
            text="Respaldar BD (.sql)",
            style="Respaldo.TButton",
            command=self.generar_respaldo_bd_ui
        ).pack(side="right", padx=(0, 8))

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.setup_tab_mascotas()
        self.setup_tab_propietarios()
        self.setup_tab_veterinarios()
        self.setup_tab_citas()
        self.setup_tab_historial_clinico()
        self.setup_tab_vacunas()
        self.setup_tab_servicios()
        self.setup_tab_medicamentos()
        self.setup_tab_detalle_atencion()
        self.setup_tab_historial_propietario()

        self.recargar_propietarios_mascota()
        self.actualizar_todas_las_tablas()
        self.root.protocol("WM_DELETE_WINDOW", self.volver_inicio)

    def volver_inicio(self):
        self.root.destroy()
        if self.on_return is not None:
            self.on_return()

    def generar_respaldo_bd_ui(self):
        exito, resultado = self.controlador.generar_respaldo_bd()
        if exito:
            messagebox.showinfo(
                "Respaldo creado",
                "El respaldo de la base de datos se creó correctamente:\n{}".format(
                    resultado
                ),
                parent=self.root
            )
        else:
            messagebox.showerror(
                "Error al crear respaldo",
                resultado,
                parent=self.root
            )

    def crear_tabla_generica(self, parent, columnas):
        tree = ttk.Treeview(parent, columns=columnas, show="headings")
        aplicar_zebra_treeview(tree)
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor="center")

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)
        return tree

    # 1. MASCOTAS
    def setup_tab_mascotas(self):
        self.tab_mascotas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_mascotas, text="Mascotas")

        frame_form = ttk.LabelFrame(self.tab_mascotas, text="Gestión de Mascota")
        frame_form.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(frame_form, text="Nombre:").pack(anchor="w", padx=5, pady=2)
        self.txt_nombre = ttk.Entry(frame_form)
        self.txt_nombre.pack(fill="x", padx=5, pady=2)

        ttk.Label(frame_form, text="Especie:").pack(anchor="w", padx=5, pady=2)
        self.txt_especie = ttk.Entry(frame_form)
        self.txt_especie.pack(fill="x", padx=5, pady=2)

        ttk.Label(frame_form, text="Raza:").pack(anchor="w", padx=5, pady=2)
        self.txt_raza = ttk.Entry(frame_form)
        self.txt_raza.pack(fill="x", padx=5, pady=2)

        ttk.Label(frame_form, text="Fecha Nacimiento:").pack(anchor="w", padx=5, pady=2)
        self.txt_fecha_nac = ttk.Entry(frame_form)
        self.txt_fecha_nac.pack(fill="x", padx=5, pady=2)

        ttk.Label(frame_form, text="Sexo:").pack(anchor="w", padx=5, pady=2)
        self.txt_sexo = ttk.Combobox(frame_form, values=["Macho", "Hembra"])
        self.txt_sexo.pack(fill="x", padx=5, pady=2)
        self.txt_sexo.set("Macho")

        ttk.Label(frame_form, text="Propietario:").pack(anchor="w", padx=5, pady=2)
        self.txt_propietario_mascota = ttk.Combobox(
            frame_form, state="readonly"
        )
        self.txt_propietario_mascota.pack(fill="x", padx=5, pady=2)

        btn_guardar = ttk.Button(
            frame_form,
            text="Guardar",
            style="Primario.TButton",
            command=self.guardar_mascota_ui
        )
        btn_guardar.pack(fill="x", padx=5, pady=10)

        btn_eliminar = ttk.Button(
            frame_form,
            text="Eliminar Seleccionada",
            style="Peligro.TButton",
            command=self.eliminar_mascota_ui
        )
        btn_eliminar.pack(fill="x", padx=5, pady=5)

        frame_tabla = ttk.Frame(self.tab_mascotas)
        frame_tabla.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        self.tree_mascotas = self.crear_tabla_generica(frame_tabla, ("ID", "Nombre", "Especie", "Raza", "Fecha Nacimiento", "Sexo"))

    def guardar_mascota_ui(self):
        seleccion_propietario = self.txt_propietario_mascota.get().strip()
        if not seleccion_propietario:
            messagebox.showwarning(
                "Datos incompletos",
                "Seleccione un propietario para la mascota.",
                parent=self.root
            )
            return

        res = self.controlador.guardar_mascota(
            self.txt_nombre.get(), self.txt_especie.get(),
            self.txt_raza.get(), self.txt_fecha_nac.get(), self.txt_sexo.get(),
            int(seleccion_propietario.split(" - ")[0])
        )
        if res:
            messagebox.showinfo("Éxito", "Mascota guardada.")
            self.txt_nombre.delete(0, 'end')
            self.txt_especie.delete(0, 'end')
            self.txt_raza.delete(0, 'end')
            self.txt_fecha_nac.delete(0, 'end')
            self.txt_propietario_mascota.set("")
            self.actualizar_todas_las_tablas()
        else:
            if self.controlador.ultimo_error != "fecha_nacimiento":
                messagebox.showerror(
                    "Error",
                    self.controlador.ultimo_error or "Error al guardar. Revise la consola."
                )

    def eliminar_mascota_ui(self):
        seleccion = self.tree_mascotas.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una mascota de la tabla para eliminar.")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar esta mascota?"):
            item = self.tree_mascotas.item(seleccion)
            id_mascota = item['values'][0]

            if self.controlador.eliminar_mascota(id_mascota):
                messagebox.showinfo("Éxito", "Mascota eliminada correctamente.")
                self.actualizar_tabla_mascotas()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la mascota. Verifique si tiene citas o historial asociado.")

    def actualizar_tabla_mascotas(self):
        for row in self.tree_mascotas.get_children(): self.tree_mascotas.delete(row)
        insertar_filas_zebra(self.tree_mascotas, self.controlador.listar_mascotas())

    # 2. PROPIETARIOS
    def setup_tab_propietarios(self):
        self.tab_propietarios = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_propietarios, text="Propietarios")

        frame_form = ttk.LabelFrame(self.tab_propietarios, text="Gestión de Propietario")
        frame_form.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(frame_form, text="Nombre:").pack(anchor="w", padx=5, pady=2)
        self.txt_prop_nombre = ttk.Entry(frame_form)
        self.txt_prop_nombre.pack(fill="x", padx=5, pady=2)

        ttk.Label(frame_form, text="Teléfono:").pack(anchor="w", padx=5, pady=2)
        self.txt_prop_telefono = ttk.Entry(frame_form)
        self.txt_prop_telefono.pack(fill="x", padx=5, pady=2)

        ttk.Label(frame_form, text="Correo:").pack(anchor="w", padx=5, pady=2)
        self.txt_prop_correo = ttk.Entry(frame_form)
        self.txt_prop_correo.pack(fill="x", padx=5, pady=2)

        ttk.Label(frame_form, text="Dirección:").pack(anchor="w", padx=5, pady=2)
        self.txt_prop_direccion = ttk.Entry(frame_form)
        self.txt_prop_direccion.pack(fill="x", padx=5, pady=2)

        btn_guardar = ttk.Button(
            frame_form,
            text="Guardar",
            style="Primario.TButton",
            command=self.guardar_propietario_ui
        )
        btn_guardar.pack(fill="x", padx=5, pady=10)

        frame_tabla = ttk.Frame(self.tab_propietarios)
        frame_tabla.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        self.tree_propietarios = self.crear_tabla_generica(frame_tabla, ("ID", "Nombre", "Teléfono", "Correo", "Dirección"))

    def guardar_propietario_ui(self):
        res = self.controlador.guardar_propietario(
            self.txt_prop_nombre.get(), self.txt_prop_telefono.get(),
            self.txt_prop_correo.get(), self.txt_prop_direccion.get()
        )
        if res:
            messagebox.showinfo("Éxito", "Propietario guardado.")
            self.txt_prop_nombre.delete(0, 'end')
            self.txt_prop_telefono.delete(0, 'end')
            self.txt_prop_correo.delete(0, 'end')
            self.txt_prop_direccion.delete(0, 'end')
            self.actualizar_tabla_propietarios()
            self.recargar_propietarios_mascota()
        else:
            messagebox.showerror("Error", "Revise los campos o la conexión.")

    def actualizar_tabla_propietarios(self):
        for row in self.tree_propietarios.get_children(): self.tree_propietarios.delete(row)
        insertar_filas_zebra(self.tree_propietarios, self.controlador.listar_propietarios())

    def recargar_propietarios_mascota(self):
        propietarios = self.controlador.listar_propietarios() or []
        opciones = [
            f"{propietario[0]} - {propietario[1]}"
            for propietario in propietarios
            if len(propietario) > 1
        ]
        self.txt_propietario_mascota.configure(values=opciones)
        self.txt_propietario_mascota.set("")

    # 3. VETERINARIOS
    def setup_tab_veterinarios(self):
        self.tab_veterinarios = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_veterinarios, text="Veterinarios")
        self.tree_veterinarios = self.crear_tabla_generica(self.tab_veterinarios, ("ID", "Nombre", "Especialidad", "Teléfono", "Correo"))

    def actualizar_tabla_veterinarios(self):
        for row in self.tree_veterinarios.get_children(): self.tree_veterinarios.delete(row)
        insertar_filas_zebra(self.tree_veterinarios, self.controlador.listar_veterinarios())

    # 4. CITAS
    def setup_tab_citas(self):
        self.tab_citas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_citas, text="Citas")
        self.tree_citas = self.crear_tabla_generica(
            self.tab_citas,
            (
                "ID",
                "Mascota ID",
                "Propietario ID",
                "Servicio ID",
                "Veterinario ID",
                "Fecha y Hora",
                "Estado"
            )
        )

    def actualizar_tabla_citas(self):
        for row in self.tree_citas.get_children(): self.tree_citas.delete(row)
        insertar_filas_zebra(
            self.tree_citas, self.controlador.listar_citas_detalle()
        )

    # 5. HISTORIAL CLÍNICO
    def setup_tab_historial_clinico(self):
        self.tab_historial_clinico = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_historial_clinico, text="Historial Clínico")
        self.tree_historial_clinico = self.crear_tabla_generica(self.tab_historial_clinico, ("ID", "Mascota ID", "Diagnóstico", "Peso (kg)", "Tratamiento / Observación"))

    def actualizar_tabla_historial_clinico(self):
        for row in self.tree_historial_clinico.get_children(): self.tree_historial_clinico.delete(row)
        insertar_filas_zebra(
            self.tree_historial_clinico,
            self.controlador.listar_historial_clinico()
        )

    # 6. VACUNAS
    def setup_tab_vacunas(self):
        self.tab_vacunas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_vacunas, text="Vacunas")
        self.tree_vacunas = self.crear_tabla_generica(self.tab_vacunas, ("ID", "Mascota ID", "Nombre Vacuna", "Fecha Aplicación", "Próxima Dosis"))

    def actualizar_tabla_vacunas(self):
        for row in self.tree_vacunas.get_children(): self.tree_vacunas.delete(row)
        insertar_filas_zebra(self.tree_vacunas, self.controlador.listar_vacunas())

    # 7. SERVICIOS
    def setup_tab_servicios(self):
        self.tab_servicios = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_servicios, text="Servicios")
        self.tree_servicios = self.crear_tabla_generica(self.tab_servicios, ("ID", "Nombre Servicio", "Costo"))

    def actualizar_tabla_servicios(self):
        for row in self.tree_servicios.get_children(): self.tree_servicios.delete(row)
        insertar_filas_zebra(self.tree_servicios, self.controlador.listar_servicios())

    # 8. MEDICAMENTOS
    def setup_tab_medicamentos(self):
        self.tab_medicamentos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_medicamentos, text="Medicamentos")
        self.tree_medicamentos = self.crear_tabla_generica(self.tab_medicamentos, ("ID", "Nombre", "Principio Activo", "Presentación", "Stock"))

    def actualizar_tabla_medicamentos(self):
        for row in self.tree_medicamentos.get_children(): self.tree_medicamentos.delete(row)
        insertar_filas_zebra(
            self.tree_medicamentos, self.controlador.listar_medicamentos()
        )

    # 9. DETALLES ATENCIÓN
    def setup_tab_detalle_atencion(self):
        self.tab_detalle_atencion = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_detalle_atencion, text="Detalles Atención")
        self.tree_detalle_atencion = self.crear_tabla_generica(self.tab_detalle_atencion, ("ID", "Cita ID", "Medicamento ID", "Dosis / Instrucción"))

    def actualizar_tabla_detalle_atencion(self):
        for row in self.tree_detalle_atencion.get_children(): self.tree_detalle_atencion.delete(row)
        insertar_filas_zebra(
            self.tree_detalle_atencion,
            self.controlador.listar_detalles_atencion()
        )

    # 10. HISTORIAL PROPIETARIO
    def setup_tab_historial_propietario(self):
        self.tab_historial_propietario = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_historial_propietario, text="Historial Propietario")
        self.tree_historial_propietario = self.crear_tabla_generica(self.tab_historial_propietario, ("ID", "Propietario ID", "Mascota ID", "Fecha Registro", "Observaciones"))

    def actualizar_tabla_historial_propietario(self):
        for row in self.tree_historial_propietario.get_children(): self.tree_historial_propietario.delete(row)
        insertar_filas_zebra(
            self.tree_historial_propietario,
            self.controlador.listar_historial_propietario()
        )

    # ACTUALIZADOR GLOBAL
    def actualizar_todas_las_tablas(self):
        self.actualizar_tabla_mascotas()
        self.actualizar_tabla_propietarios()
        self.actualizar_tabla_veterinarios()
        self.actualizar_tabla_citas()
        self.actualizar_tabla_historial_clinico()
        self.actualizar_tabla_vacunas()
        self.actualizar_tabla_servicios()
        self.actualizar_tabla_medicamentos()
        self.actualizar_tabla_detalle_atencion()
        self.actualizar_tabla_historial_propietario()