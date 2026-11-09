#!/usr/bin/env bash
# preparar_azure.sh · MiMascota · SO1 y SO2 (VM de Azure)
# Deja la VM lista como bodega de respaldos. Ejecutar una vez como root
# (Ejecutar comando en el portal, o sudo bash preparar_azure.sh).
set -Eeuo pipefail

# Pegue aquí la línea completa de su llave PÚBLICA (mimascota_respaldo.pub, generada en el PC)
CLAVE_PUBLICA='PEGUE_AQUI_LA_LINEA_ssh-ed25519_COMPLETA'
BASE=/var/backups/mimascota

# 1. Paquetes: MySQL para verificar, unzip para abrir los .zip de Windows, ufw como firewall
export DEBIAN_FRONTEND=noninteractive NEEDRESTART_SUSPEND=1
apt-get update -qq
apt-get install -y -qq mysql-server unzip ufw >/dev/null

timedatectl set-timezone America/Bogota   # la hora del log coincide con la del PC

# 2. Usuario que solo recibe respaldos: sin sudo y sin contraseña (entra con llave)
id respaldo &>/dev/null || adduser --disabled-password --gecos "" respaldo

# 3. Carpetas y permisos
#    entrantes   respaldo puede escribir (llegan las copias)
#    verificados respaldo puede leer pero NO borrar: si roban el PC, no pueden borrar las copias buenas
install -d -o root     -g respaldo -m 750 "$BASE"
install -d -o respaldo -g respaldo -m 750 "$BASE/entrantes"
install -d -o root     -g respaldo -m 750 "$BASE/verificados"
install -d -o root     -g root     -m 700 "$BASE/rechazados"
install -d -o root     -g adm      -m 750 /var/log/mimascota

# 4. Llave del PC. "restrict" quita reenvío de puertos y terminal interactiva; scp sigue funcionando
install -d -o respaldo -g respaldo -m 700 /home/respaldo/.ssh
echo "restrict $CLAVE_PUBLICA" > /home/respaldo/.ssh/authorized_keys
chown respaldo:respaldo /home/respaldo/.ssh/authorized_keys
chmod 600 /home/respaldo/.ssh/authorized_keys

# 5. MySQL solo local y firewall con un único puerto abierto
systemctl enable --now mysql
ss -tlnp | grep -q '127.0.0.1:3306' && echo "MySQL escucha solo en 127.0.0.1"
ufw allow OpenSSH
ufw --force enable

echo "Listo. Revise: ls -la $BASE  |  ufw status  |  systemctl status mysql"
