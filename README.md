# MiMascota · Proyecto Integrador Momento 3

Plantilla del proyecto integrador de **Bases de Datos** y **Sistemas Operativos y Compiladores (710068)**
· Ingeniería de Software · Universidad Cooperativa de Colombia.

MiMascota es una **aplicación de escritorio en Python (Tkinter, patrón MVC)** que usa **MySQL en el PC
Windows** de la clínica. Una **VM Ubuntu en Azure** recibe cada día una copia de la base, comprueba que se
puede restaurar y la guarda fuera del sitio.

> Guía técnica: [`bd/modelo/Guia_Tecnica_Base_de_Datos_MiMascota_TripleJ_JJJ.pdf`](bd/modelo/Guia_Tecnica_Base_de_Datos_MiMascota_TripleJ_JJJ.pdf)

## Equipo

| Integrante | Usuario de GitHub | Rol principal |
| --- | --- | --- |
| Johan Manuel Restrepo Rosero| Johan5412 | APP |
| Jhojan Camilo Quintero | _@usuario_ |BD |
| Juan David Sanchez Burbano | _@usuario_ | SO|


2. Sigan la guía técnica y los scripts de `bd/` y `so/` según el entorno.

## Estructura

```text
mimascota-equipoXX/
├── README.md                     este archivo; se completa como manual de despliegue (SO7)
├── app/                          aplicación de escritorio (Python, MVC)
│   ├── main.py                   punto de entrada
│   ├── config.py                 lee las credenciales de app/app.env
│   ├── modelo/                   SQL y conexión (el único lugar con SQL)
│   ├── controlador/              validaciones y acciones
│   ├── vista/                    ventanas Tkinter
│   ├── tests/                    pruebas (unittest)
│   ├── requirements.txt
│   └── app.env.example           plantilla de credenciales, sin claves reales
├── bd/                           Bases de Datos (BD1–BD6)
│   ├── 00_base_inicial.sql       base de partida administracionmascotasbd (6 tablas)
│   ├── 01_ddl.sql … 06_usuarios.sql
│   ├── modelo/                   MER, relacional, diccionario, 3FN (BD1)
│   └── pruebas/pruebas_bd5.sql   casos de prueba que deben fallar
├── so/                           Sistemas Operativos (SO1–SO6)
│   ├── windows/                  respaldo.ps1, restaurar.ps1, monitor.ps1, tareas.ps1
│   ├── azure/                    preparar_azure.sh, verificar_respaldo.sh, crontab.txt
│   └── evidencias/               capturas de SO1 a SO6
└── docs/                         guía del proyecto
```

## Ejecutar la aplicación

Requiere Python 3.10 o superior y MySQL 8 corriendo como servicio en el PC.

```powershell
cd app
python -m pip install -r requirements.txt
copy app.env.example app.env    # luego ponga la clave real en ese archivo
python main.py
```

Pruebas (no necesitan MySQL):

```powershell
cd app
python -m unittest discover -s tests -v
```

## Entregables

| Código | Entregable | Dónde | Peso |
| --- | --- | --- | --- |
| BD1 | Modelo de datos (mínimo 10 tablas) | `bd/modelo/` | según guía de BD |
| BD2–BD6 | DDL, datos, consultas y vistas, lógica, usuarios | `bd/01…06` | según guía de BD |
| SO1 | Preparación de los dos equipos | `so/azure/preparar_azure.sh`, evidencias | 10 % |
| SO2 | Motor de base de datos | evidencias del servicio y del firewall | 15 % |
| SO3 | Respaldo y envío a la nube | `so/windows/respaldo.ps1` | 20 % |
| SO4 | Verificación y restauración | `so/azure/verificar_respaldo.sh`, `so/windows/restaurar.ps1` | 20 % |
| SO5 | Tareas programadas | `so/windows/tareas.ps1`, `so/azure/crontab.txt` | 10 % |
| SO6 | Monitoreo y procesos | `so/windows/monitor.ps1`, informe de procesos | 15 % |
| SO7 | Manual de despliegue | este README | 10 % |

## Reglas del repositorio

- **Nunca** se suben contraseñas, llaves privadas ni archivos `.cnf` o `.env` reales: solo los `.example`.
  El `.gitignore` ya los bloquea; revisen antes de cada `git push`.
- Todos los integrantes deben tener commits propios.
- Los scripts de `bd/` deben correr en orden, sin errores, sobre una base vacía.

---

## Manual de despliegue (SO7) · completar por el equipo

> Escriban aquí los pasos para que **otra persona** monte todo desde cero, con los comandos exactos que
> usaron y lo que debe ver en cada paso.

### 1. PC Windows
_Instalación de MySQL como servicio, recuperación, `bind-address`, carpetas y permisos, usuarios de MySQL,
`app.env` y `respaldo.cnf`, llave SSH._

### 2. VM de Azure
_Creación de la VM, `preparar_azure.sh`, primera conexión desde el PC._

### 3. Respaldo, verificación y restauración
_Cómo se programan las tareas, dónde quedan los logs y cómo se restaura._

### 4. Verificación final
_Cómo comprobar que todo funciona (las tres pruebas de fuego)._
