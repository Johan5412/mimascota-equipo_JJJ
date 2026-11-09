# bd/ · Bases de Datos

| Archivo | Entregable | Qué contiene |
| --- | --- | --- |
| `00_base_inicial.sql` | Recurso de partida | Volcado de `administracionmascotasbd` (phpMyAdmin, MariaDB 10.4). Importa sin errores en MySQL 8.0 |
| `modelo/` | BD1 | MER, modelo relacional, diccionario de datos y 3FN |
| `01_ddl.sql` | BD2 | Modelo completo del equipo (mínimo 10 tablas), con integridad e índices |
| `02_dml.sql` | BD3 | Datos de prueba ficticios y coherentes |
| `03_consultas.sql`, `04_vistas.sql` | BD4 | 15 consultas de negocio y 3 vistas |
| `05_logica.sql` | BD5 | Procedimientos, disparadores, función y transacción |
| `06_usuarios.sql` | BD6 | Usuarios con privilegios mínimos (host `127.0.0.1`) |
| `pruebas/pruebas_bd5.sql` | BD5 | Casos de prueba, incluidos los que deben fallar |

`00_base_inicial.sql` es el punto de partida: sus 6 tablas (`tb_pet`, `tb_dog`, `tb_cat`, `tb_doctor`,
`tb_hospital`, `tb_pet_hospital`) se amplían en `01_ddl.sql` con propietarios, citas, historial y vacunas.

Orden de carga sobre una base vacía:

```powershell
mysql -u root -p -e "CREATE DATABASE administracionmascotasbd"
mysql -u root -p administracionmascotasbd -e "source C:/ruta/al/repo/bd/01_ddl.sql"
# … 02 a 06 en orden
```

Cuando el modelo cambie de número de tablas, actualicen `TABLAS_MIN` en `so/azure/crontab.txt`
(y en `/etc/cron.d/mimascota` de la VM).
