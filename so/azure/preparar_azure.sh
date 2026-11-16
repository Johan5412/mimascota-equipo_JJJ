#!/bin/bash
# ==============================================================================
# Script de Preparación de Entorno en Azure VM (SO1 / SO2)
# ==============================================================================

# 1. Crear directorio de respaldos y asignar permisos
sudo mkdir -p /var/backups/mimascota
sudo chmod 770 /var/backups/mimascota

# 2. Crear usuario de respaldo en Linux (si no existe)
if ! id "respaldo" &>/dev/null; then
    sudo useradd -m -s /bin/bash respaldo
fi

# 3. Asignar propietario del directorio
sudo chown -R respaldo:respaldo /var/backups/mimascota

# 4. Configurar directorio SSH para el usuario respaldo
sudo mkdir -p /home/respaldo/.ssh
sudo chmod 700 /home/respaldo/.ssh

# 5. Configurar llave pública SSH
# Reemplaza el texto entre comillas por tu llave pública completa (ssh-ed25519 ...)
LLAVE_PUBLICA="PEGUE_AQUI_LA_LINEA_ssh-ed25519_COMPLETA"

echo "$LLAVE_PUBLICA" | sudo tee /home/respaldo/.ssh/authorized_keys > /dev/null
sudo chmod 600 /home/respaldo/.ssh/authorized_keys
sudo chown -R respaldo:respaldo /home/respaldo/.ssh

echo "Entorno en Azure VM configurado con éxito."