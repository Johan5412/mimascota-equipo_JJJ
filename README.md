# MiMascota · Proyecto Integrador Momento 3 (Equipo JJJ)

Sistema de información clínica veterinaria desarrollado para las asignaturas de **Bases de Datos** y **Sistemas Operativos** · Ingeniería de Software (4.º Semestre) · **Universidad Cooperativa de Colombia — Campus Popayán**.

**MiMascota** es una **aplicación de escritorio multiplataforma en Python 3 (Tkinter, patrón Modelo-Vista-Controlador)** ejecutada en estaciones cliente Windows, conectada mediante TCP/IP (puerto `3306`) a un motor **MySQL Server 8.0** desplegado en una máquina virtual **Ubuntu Server 22.04 LTS en Microsoft Azure** (`20.114.49.220`), con respaldos automáticos diarios mediante `cron` + `mysqldump`, tolerancia a fallos gestionada por `systemd` y respaldo manual bajo demanda desde el módulo administrativo.

* **Guía Técnica de Base de Datos (v2):** [`bd/modelo/Guia_Tecnica_Base_de_Datos_MiMascota_TripleJ_JJJ_v2.docx`](bd/modelo/Guia_Tecnica_Base_de_Datos_MiMascota_TripleJ_JJJ_v2.docx)
* **Guía Técnica de Sistemas Operativos (v2):** [`so/evidencias/Guia_Tecnica_Sistemas_Operativos_MiMascota_TripleJ_JJJ_v2.docx`](so/evidencias/Guia_Tecnica_Sistemas_Operativos_MiMascota_TripleJ_JJJ_v2.docx)

---

## Equipo de Desarrollo (Grupo JJJ)

| Integrante | Usuario GitHub | Rol Principal |
| :--- | :--- | :--- |
| **Johan Manuel Restrepo Rosero** | [@Johan5412](https://github.com/Johan5412) | Arquitectura MVC, Interfaz Tkinter, Integración Cloud |
| **Jhojan Camilo Quintero** | `@jhojanquintero` | Modelado Relacional (3FN), DDL/DML, Procedimientos y Triggers |
| **Juan David Sánchez Burbano** | `@juandavidsanchez` | Infraestructura Linux Ubuntu, Systemd, Permisos POSIX y Cron |

---

## Estructura del Repositorio

```text
mimascota-equipo_JJJ/
├── README.md                                                # Manual de despliegue y sustentación (SO7)
├── .gitignore                                               # Exclusión de cachés (__pycache__) y archivos temporales
├── app/                                                     # Aplicación de escritorio (Python 3 + Tkinter MVC)
│   ├── main.py                                              # Punto de entrada y control de acceso por roles (RBAC)
│   ├── mimascota.ico                                        # Ícono nativo para acceso directo en Windows
│   ├── requirements.txt                                     # Dependencia mysql-connector-python
│   ├── modelo/                                              # Conexión TCP/IP a Azure y consultas parametrizadas (%s)
│   ├── controlador/                                         # Validaciones de dominio, transacciones y respaldo SQL
│   └── vista/                                               # Interfaces gráficas (Recepción, Veterinario, Admin y Estilos)
├── bd/                                                      # Ingeniería de Datos (BD1–BD6)
│   ├── 00_base_inicial.sql ... 07_migracion_veterinario.sql # Scripts DDL, datos maestros, triggers y migraciones
│   ├── modelo/
│   │   ├── Modelo_Entidad_Relacion.dia                      # Diagrama Entidad-Relación (10 entidades)
│   │   ├── Modelo_Relacional.dia                            # Esquema relacional normalizado (3FN)
│   │   └── Guia_Tecnica_Base_de_Datos_MiMascota_TripleJ_JJJ_v2.docx
│   ├── pruebas/                                             # Casos de prueba de integridad referencial y restricciones
│   └── respaldos/                                           # Volcados lógicos (.sql) generados y sincronizados
└── so/                                                      # Infraestructura y Sistemas Operativos (S01–S07)
    ├── windows/                                             # Scripts PowerShell de administración local
    │   ├── monitor.ps1                                      # Monitoreo de procesos y estado del servicio
    │   ├── respaldo.cnf.example                             # Plantilla de configuración de credenciales seguras
    │   ├── respaldo.ps1                                     # Automatización de respaldo en cliente Windows
    │   ├── restaurar.ps1                                    # Script de restauración ante desastres
    │   └── tareas.ps1                                       # Gestión de tareas programadas en Windows
    ├── azure/                                               # Scripts Bash y planificación en Ubuntu Server 22.04
    │   ├── crontab.txt                                      # Definición de tarea programada diaria (02:00 AM)
    │   ├── preparar_azure.sh                                # Aprovisionamiento y seguridad en nodo Linux
    │   └── verificar_respaldo.sh                            # Auditoría e integridad de volcados .sql
    └── evidencias/
        └── Guia_Tecnica_Sistemas_Operativos_MiMascota_TripleJ_JJJ_v2.docx

```
Ejecutar la Aplicación (Nodo Cliente Windows)
Requiere Python 3.10 o superior y conexión a Internet para comunicarse con el servidor MySQL en Azure (20.114.49.220:3306):

```
cd app
python -m pip install -r requirements.txt
python main.py
```
Credenciales de Acceso por Rol (RBAC)
Usuario / Recepción: Ingreso directo (registro de propietarios, mascotas, programación y cancelación filtrada de citas).

Médico Veterinario: PIN 2468 (consulta de citas pendientes, diagnóstico, prescripción en detalle_atencion y vacunación).

Administrador: Contraseña 12345 (CRUD completo sobre las 10 entidades y exportación manual de respaldo .sql).

Manual de Despliegue y Verificación en Nube (SO7)
1. Arquitectura Cliente-Servidor (Windows + Azure Ubuntu 22.04 LTS)
Servidor Cloud (mimascota-vm): Instancia Standard B2ats v2 (2 vCPU, 1 GiB RAM) en Microsoft Azure con IP pública 20.114.49.220 y reglas NSG habilitadas únicamente para 22/TCP (SSH/SCP) y 3306/TCP (MySQL).

Motor MySQL 8.0: Configurado con bind-address = 0.0.0.0, motor transaccional InnoDB y usuario dedicado app_mimascota bajo principio de mínimo privilegio.

2. Verificación de Respaldos Automáticos Diarios (02:00 AM)
En Ubuntu Server se configuró el archivo oculto /home/azureuser/.my.cnf con permisos POSIX chmod 600 y el script ejecutable /home/azureuser/backups_mimascota/backup_bd.sh (chmod +x), programado en crontab todos los días a las 02:00 AM. Para auditarlo en Azure (RunShellScript):
```
echo "=== 1. TAREA PROGRAMADA EN CRONTAB (2:00 AM) ==="
crontab -u azureuser -l

echo "=== 2. ESTADO DEL DEMONIO CRON EN UBUNTU ==="
systemctl is-active cron

echo "=== 3. SCRIPT BASH Y PERMISOS POSIX ==="
ls -lh /home/azureuser/backups_mimascota/backup_bd.sh
cat /home/azureuser/backups_mimascota/backup_bd.sh

echo "=== 4. ARCHIVOS DE RESPALDO GENERADOS AUTOMÁTICAMENTE (.sql) ==="
ls -lh /home/azureuser/backups_mimascota/*.sql

echo "=== 5. ÚLTIMAS LÍNEAS DEL LOG DE EJECUCIÓN ==="
tail -n 10 /home/azureuser/backups_mimascota/backup.log 2>/dev/null || echo "Sin errores registrados en backup.log"
```
3. Prueba de Tolerancia a Fallos con Systemd (SIGKILL) y Continuidad de la App
Para demostrar que systemd recupera automáticamente el demonio mysqld (Restart=on-failure) sin interrumpir la aplicación cliente en Windows:
```
echo "=== 1. PID ORIGINAL DE MYSQL ==="
PID_ANTES=$(pidof mysqld)
echo "PID antes del fallo: $PID_ANTES"

echo "=== 2. ENVIANDO SEÑAL DE TERMINACIÓN ABRUPTA (SIGKILL / kill -9) ==="
sudo kill -9 $PID_ANTES

echo "=== 3. ESPERANDO RECUPERACIÓN AUTOMÁTICA DE SYSTEMD ==="
sleep 3
PID_DESPUES=$(pidof mysqld)
echo "PID recuperado por systemd: $PID_DESPUES"
systemctl status mysql --no-pager | head -n 10
```
4. Descarga Segura (SCP) y Restauración ante Desastres
```
# Descargar respaldos generados en Azure hacia la carpeta local bd/respaldos/
scp azureuser@20.114.49.220:~/backups_mimascota/*.sql C:\Users\JOHAN\Desktop\Mimascota_equipo-JJJ\bd\respaldos\
```
```
# Restaurar un volcado lógico (.sql) en el servidor Ubuntu
mysql -u app_mimascota -p123456 mimascota < /home/azureuser/backups_mimascota/ARCHIVO_RESPALDO.sql
