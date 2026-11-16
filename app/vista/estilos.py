from tkinter import ttk


FONDO_VENTANA = "#F4F7F6"
FONDO_TARJETA = "#FFFFFF"
PRIMARIO = "#0D7377"
PRIMARIO_HOVER = "#14919B"
PELIGRO = "#C0392B"
PELIGRO_HOVER = "#A93226"
SECUNDARIO = "#546E7A"
SECUNDARIO_HOVER = "#455A64"
RESPALDO = "#2C3E50"
RESPALDO_HOVER = "#1A252F"
TEXTO_OSCURO = "#1E293B"


def aplicar_estilos(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure(
        ".",
        font=("Segoe UI", 10),
        foreground=TEXTO_OSCURO
    )
    style.configure("TFrame", background=FONDO_VENTANA)
    style.configure("TLabel", background=FONDO_VENTANA, foreground=TEXTO_OSCURO)
    style.configure(
        "TLabelFrame",
        background=FONDO_TARJETA,
        bordercolor="#D7E3E0",
        borderwidth=1,
        relief="solid",
        padding=12
    )
    style.configure(
        "TLabelFrame.Label",
        background=FONDO_TARJETA,
        foreground=PRIMARIO,
        font=("Segoe UI", 11, "bold")
    )
    style.configure(
        "Card.TFrame",
        background=FONDO_TARJETA,
        bordercolor="#D7E3E0",
        borderwidth=1,
        relief="solid"
    )
    style.configure("Card.TLabel", background=FONDO_TARJETA, foreground=TEXTO_OSCURO)
    style.configure(
        "CardTitle.TLabel",
        background=FONDO_TARJETA,
        foreground=TEXTO_OSCURO,
        font=("Segoe UI", 12, "bold")
    )
    style.configure(
        "CardDescription.TLabel",
        background=FONDO_TARJETA,
        foreground="#52616B",
        font=("Segoe UI", 10)
    )
    style.configure("TNotebook", background=FONDO_VENTANA, borderwidth=0)
    style.configure(
        "TNotebook.Tab",
        background="#E7EFED",
        foreground=TEXTO_OSCURO,
        padding=(14, 8),
        font=("Segoe UI", 10, "bold")
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", PRIMARIO), ("active", "#D7E9E5")],
        foreground=[("selected", "#FFFFFF")]
    )
    style.configure("TEntry", padding=7, fieldbackground=FONDO_TARJETA)
    style.configure("TCombobox", padding=7, fieldbackground=FONDO_TARJETA)
    style.configure("TButton", padding=(12, 8), font=("Segoe UI", 10, "bold"))

    for nombre, color, hover in (
        ("Primario", PRIMARIO, PRIMARIO_HOVER),
        ("Peligro", PELIGRO, PELIGRO_HOVER),
        ("Secundario", SECUNDARIO, SECUNDARIO_HOVER),
        ("Respaldo", RESPALDO, RESPALDO_HOVER)
    ):
        style.configure(
            "{}.TButton".format(nombre),
            background=color,
            foreground="#FFFFFF",
            padding=(13, 9),
            font=("Segoe UI", 10, "bold"),
            borderwidth=0
        )
        style.map(
            "{}.TButton".format(nombre),
            background=[("disabled", "#B0BEC5"), ("pressed", hover), ("active", hover)],
            foreground=[("disabled", "#ECEFF1"), ("!disabled", "#FFFFFF")]
        )

    style.configure(
        "Accent.TButton",
        background=PRIMARIO,
        foreground="#FFFFFF",
        padding=(16, 11),
        font=("Segoe UI", 11, "bold")
    )
    style.map(
        "Accent.TButton",
        background=[("active", PRIMARIO_HOVER), ("pressed", PRIMARIO_HOVER)],
        foreground=[("active", "#FFFFFF"), ("pressed", "#FFFFFF")]
    )
    style.configure(
        "Treeview",
        background=FONDO_TARJETA,
        fieldbackground=FONDO_TARJETA,
        foreground=TEXTO_OSCURO,
        rowheight=28,
        relief="solid",
        borderwidth=1
    )
    style.configure(
        "Treeview.Heading",
        background=PRIMARIO,
        foreground="#FFFFFF",
        font=("Segoe UI", 10, "bold"),
        relief="solid",
        borderwidth=1,
        padding=(8, 7)
    )
    style.map(
        "Treeview",
        background=[("selected", "#CBE5DF")],
        foreground=[("selected", "#0F172A")]
    )
    style.configure("Banner.TFrame", background=PRIMARIO)
    style.configure(
        "BannerTitle.TLabel",
        background=PRIMARIO,
        foreground="#FFFFFF",
        font=("Segoe UI", 17, "bold")
    )
    style.configure(
        "BannerSubtitle.TLabel",
        background=PRIMARIO,
        foreground="#E4F3F1",
        font=("Segoe UI", 10)
    )
    style.configure(
        "BannerBadge.TLabel",
        background=PRIMARIO,
        foreground="#D9EEEA",
        font=("Segoe UI", 9, "bold")
    )
    style.configure(
        "BannerCard.TFrame",
        background=PRIMARIO,
        borderwidth=0
    )

    root.configure(background=FONDO_VENTANA)


def crear_banner(parent, subtitulo):
    banner = ttk.Frame(parent, style="Banner.TFrame", padding=(22, 14))
    banner.pack(fill="x")

    texto = ttk.Frame(banner, style="Banner.TFrame")
    texto.pack(side="left", fill="x", expand=True)
    ttk.Label(
        texto,
        text="Clínica Veterinaria MiMascota",
        style="BannerTitle.TLabel"
    ).pack(anchor="w")
    ttk.Label(
        texto,
        text=subtitulo,
        style="BannerSubtitle.TLabel"
    ).pack(anchor="w", pady=(2, 0))
    ttk.Label(
        banner,
        text="● MySQL Azure Activo",
        style="BannerBadge.TLabel"
    ).pack(side="right", padx=(16, 0))
    return banner


def aplicar_zebra_treeview(tree):
    tree.tag_configure("par", background="#FFFFFF")
    tree.tag_configure("impar", background="#EDF5F3")


def insertar_filas_zebra(tree, filas):
    aplicar_zebra_treeview(tree)
    for indice, fila in enumerate(filas):
        etiqueta = "par" if indice % 2 == 0 else "impar"
        tree.insert("", "end", values=fila, tags=(etiqueta,))
