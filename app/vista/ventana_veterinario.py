import tkinter as tk
from tkinter import messagebox, ttk

from controlador.mascota_controlador import MascotaControlador
from vista.estilos import aplicar_estilos, crear_banner


class VentanaVeterinario:
    def __init__(self, root, on_return=None):
        self.root = root
        self.on_return = on_return
        self.controlador = MascotaControlador()
        self.citas_por_id = {}

        self.root.title("MiMascota - Módulo Veterinario")
        self.root.geometry("1040x820")
        self.root.minsize(900, 700)
        aplicar_estilos(self.root)

        crear_banner(self.root, "Consultorio Médico Veterinario")

        contenido = ttk.Frame(self.root, padding=(22, 8, 22, 12))
        contenido.pack(fill="both", expand=True)
        contenido.columnconfigure(0, weight=1)

        self._crear_bloque_paciente(contenido)
        self._crear_bloque_atencion(contenido)

        barra_inferior = ttk.Frame(self.root, padding=(22, 0, 22, 16))
        barra_inferior.pack(fill="x")
        ttk.Button(
            barra_inferior,
            text="Cambiar Rol / Volver al Inicio",
            style="Secundario.TButton",
            command=self.volver_inicio
        ).pack(side="right")

        self.recargar_catalogos()
        self.recargar_citas_pendientes()
        self.root.protocol("WM_DELETE_WINDOW", self.volver_inicio)

    def _crear_bloque_paciente(self, parent):
        bloque = ttk.LabelFrame(
            parent,
            text="Bloque 1 — Selección y ficha del paciente",
            padding=16
        )
        bloque.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        bloque.columnconfigure(0, weight=1)

        ttk.Label(bloque, text="Cita pendiente").grid(
            row=0, column=0, sticky="w", pady=(0, 4)
        )
        self.cita_combo = ttk.Combobox(bloque, state="readonly")
        self.cita_combo.grid(row=1, column=0, sticky="ew")
        self.cita_combo.bind(
            "<<ComboboxSelected>>", self._al_seleccionar_cita
        )

        ficha = ttk.Frame(bloque, padding=(0, 12, 0, 0))
        ficha.grid(row=2, column=0, sticky="ew")
        for columna in range(3):
            ficha.columnconfigure(columna, weight=1)

        self.ficha_mascota = tk.StringVar(value="—")
        self.ficha_propietario = tk.StringVar(value="—")
        self.ficha_servicio = tk.StringVar(value="—")

        self._crear_dato_ficha(
            ficha, "Mascota", self.ficha_mascota, 0
        )
        self._crear_dato_ficha(
            ficha, "Propietario", self.ficha_propietario, 1
        )
        self._crear_dato_ficha(
            ficha, "Servicio solicitado", self.ficha_servicio, 2
        )

    @staticmethod
    def _crear_dato_ficha(parent, titulo, variable, columna):
        panel = ttk.LabelFrame(parent, text=titulo, padding=10)
        panel.grid(
            row=0,
            column=columna,
            sticky="nsew",
            padx=(0 if columna == 0 else 6, 0 if columna == 2 else 6)
        )
        ttk.Label(
            panel,
            textvariable=variable,
            wraplength=250,
            justify="left"
        ).pack(anchor="w", fill="x")

    def _crear_bloque_atencion(self, parent):
        bloque = ttk.LabelFrame(
            parent,
            text="Bloque 2 — Historial clínico y detalle de atención",
            padding=16
        )
        bloque.grid(row=1, column=0, sticky="nsew")
        bloque.columnconfigure(0, weight=1)
        bloque.columnconfigure(1, weight=1)
        parent.rowconfigure(1, weight=1)

        self.diagnostico = self._agregar_campo(
            bloque, "Diagnóstico", 0, 0
        )
        self.peso_actual = self._agregar_campo(
            bloque, "Peso actual (kg)", 0, 1
        )
        self.observaciones = self._agregar_campo(
            bloque, "Observaciones", 2, 0
        )

        self.medicamento_combo = self._agregar_campo(
            bloque, "Medicamento recetado", 4, 0, readonly=True
        )
        self.dosis = self._agregar_campo(
            bloque, "Dosis / indicaciones (si receta medicamento)", 4, 1
        )
        self.vacuna_combo = self._agregar_campo(
            bloque, "Vacuna aplicada", 6, 0, readonly=True
        )
        self.fecha_aplicacion = self._agregar_campo(
            bloque, "Fecha de aplicación (YYYY-MM-DD)", 6, 1
        )
        self.fecha_proxima_dosis = self._agregar_campo(
            bloque, "Próxima dosis (YYYY-MM-DD)", 8, 0
        )

        self.medicamento_combo.bind(
            "<<ComboboxSelected>>", self._al_cambiar_medicamento
        )
        self.vacuna_combo.bind(
            "<<ComboboxSelected>>", self._al_cambiar_vacuna
        )

        ttk.Button(
            bloque,
            text="Guardar Consulta y Atención",
            style="Primario.TButton",
            command=self.guardar_atencion
        ).grid(
            row=10,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(20, 0)
        )

    @staticmethod
    def _agregar_campo(parent, etiqueta, fila, columna, readonly=False):
        ttk.Label(parent, text=etiqueta).grid(
            row=fila,
            column=columna,
            sticky="w",
            padx=(0 if columna == 0 else 10, 0),
            pady=(8, 3)
        )
        if readonly:
            campo = ttk.Combobox(parent, state="readonly")
        else:
            campo = ttk.Entry(parent)
        campo.grid(
            row=fila + 1,
            column=columna,
            sticky="ew",
            padx=(0 if columna == 0 else 10, 0)
        )
        return campo

    def recargar_catalogos(self):
        errores = []
        medicamentos = self.controlador.listar_medicamentos()
        if self.controlador.ultimo_error:
            errores.append(self.controlador.ultimo_error)
        vacunas = self.controlador.listar_nombres_vacunas_unicos()
        if self.controlador.ultimo_error:
            errores.append(self.controlador.ultimo_error)

        opciones_medicamentos = ["0 - Ninguno"] + [
            "{} - {}".format(item[0], item[1])
            for item in medicamentos
            if len(item) > 1
        ]
        opciones_vacunas = ["Ninguna"] + [
            item[0] for item in vacunas if item and item[0]
        ]
        self.medicamento_combo.configure(values=opciones_medicamentos)
        self.vacuna_combo.configure(values=opciones_vacunas)
        self.medicamento_combo.set(opciones_medicamentos[0])
        self.vacuna_combo.set(opciones_vacunas[0])

        if errores:
            messagebox.showerror(
                "Error al cargar catálogos",
                "\n".join(errores),
                parent=self.root
            )

    def recargar_citas_pendientes(self):
        citas = self.controlador.listar_citas_pendientes_detalle()
        if self.controlador.ultimo_error:
            messagebox.showerror(
                "Error al cargar citas",
                self.controlador.ultimo_error,
                parent=self.root
            )
        self.citas_por_id = {int(cita[0]): cita for cita in citas if len(cita) >= 10}
        opciones = [
            "{} - {} ({})".format(cita[0], cita[3], cita[1])
            for cita in self.citas_por_id.values()
        ]
        self.cita_combo.configure(values=opciones)
        self.cita_combo.set("")
        self._limpiar_ficha_paciente()

    def _al_seleccionar_cita(self, _evento):
        seleccion = self.cita_combo.get().strip()
        if not seleccion:
            self._limpiar_ficha_paciente()
            return
        try:
            id_cita = int(seleccion.split(" - ", 1)[0])
        except ValueError:
            self._limpiar_ficha_paciente()
            return
        cita = self.citas_por_id.get(id_cita)
        if cita is None:
            self._limpiar_ficha_paciente()
            return

        id_mascota, nombre, especie, raza, nacimiento = cita[2:7]
        self.ficha_mascota.set(
            "{} (ID {})\nEspecie: {}\nRaza: {}\nNacimiento: {}".format(
                nombre or "Sin nombre",
                id_mascota,
                especie or "—",
                raza or "—",
                nacimiento or "—"
            )
        )
        self.ficha_propietario.set(
            "{}\nTeléfono: {}".format(
                cita[8] or "Sin propietario asignado",
                cita[9] or "—"
            )
        )
        self.ficha_servicio.set(cita[7] or "—")

    def _limpiar_ficha_paciente(self):
        self.ficha_mascota.set("—")
        self.ficha_propietario.set("—")
        self.ficha_servicio.set("—")

    def _al_cambiar_medicamento(self, _evento):
        if self.medicamento_combo.get().startswith("0 - "):
            self.dosis.delete(0, tk.END)

    def _al_cambiar_vacuna(self, _evento):
        if self.vacuna_combo.get() == "Ninguna":
            self.fecha_aplicacion.delete(0, tk.END)
            self.fecha_proxima_dosis.delete(0, tk.END)

    def guardar_atencion(self):
        seleccion_cita = self.cita_combo.get().strip()
        if not seleccion_cita:
            messagebox.showwarning(
                "Datos incompletos",
                "Seleccione una cita pendiente.",
                parent=self.root
            )
            return

        seleccion_medicamento = self.medicamento_combo.get().strip()
        seleccion_vacuna = self.vacuna_combo.get().strip()
        id_medicamento = (
            None if seleccion_medicamento.startswith("0 - ")
            else int(seleccion_medicamento.split(" - ", 1)[0])
        )
        nombre_vacuna = (
            None if seleccion_vacuna == "Ninguna" else seleccion_vacuna
        )

        exito = self.controlador.registrar_atencion_completa(
            int(seleccion_cita.split(" - ", 1)[0]),
            self.diagnostico.get().strip(),
            self.peso_actual.get().strip(),
            self.observaciones.get().strip(),
            id_medicamento,
            self.dosis.get().strip() or None,
            nombre_vacuna,
            self.fecha_aplicacion.get().strip() or None,
            self.fecha_proxima_dosis.get().strip() or None
        )
        if not exito:
            messagebox.showerror(
                "No se pudo guardar la atención",
                self.controlador.ultimo_error or "Verifique los datos e inténtelo nuevamente.",
                parent=self.root
            )
            return

        messagebox.showinfo(
            "Atención registrada",
            "La consulta y la atención se guardaron correctamente.",
            parent=self.root
        )
        self._limpiar_formulario()
        self.recargar_citas_pendientes()

    def _limpiar_formulario(self):
        for campo in (
            self.diagnostico,
            self.peso_actual,
            self.observaciones,
            self.dosis,
            self.fecha_aplicacion,
            self.fecha_proxima_dosis
        ):
            campo.delete(0, tk.END)
        opciones_medicamento = self.medicamento_combo.cget("values")
        opciones_vacuna = self.vacuna_combo.cget("values")
        self.medicamento_combo.set(opciones_medicamento[0] if opciones_medicamento else "")
        self.vacuna_combo.set(opciones_vacuna[0] if opciones_vacuna else "")

    def volver_inicio(self):
        self.root.destroy()
        if self.on_return is not None:
            self.on_return()
