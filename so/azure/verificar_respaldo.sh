#!/bin/bash
# ==============================================================================
# Script de Verificación y Auditoría de Respaldos en Azure VM (SO4)
# ==============================================================================

DIR_BACKUPS="/var/backups/mimascota"
ARCHIVO_LOG="/var/log/verificar_respaldo.log"

timeStamp=$(date "+%Y-%m-%d %H:%M:%S")

echo "[$timeStamp] === AUDITORÍA NOCTURNA DE RESPALDOS ===" >> "$ARCHIVO_LOG"

# Contar cuántos archivos .zip existen
CANTIDAD=$(ls -1 $DIR_BACKUPS/*.zip 2>/dev/null | wc -l)

if [ "$CANTIDAD" -gt 0 ]; then
    echo "[$timeStamp] ESTADO: OK. Se encontraron $CANTIDAD respaldos en $DIR_BACKUPS." >> "$ARCHIVO_LOG"
    ULTIMO=$(ls -t $DIR_BACKUPS/*.zip | head -n 1)
    TAMANO=$(du -h "$ULTIMO" | cut -f1)
    echo "[$timeStamp] ÚLTIMO RESPALDO: $ULTIMO ($TAMANO)" >> "$ARCHIVO_LOG"
else
    echo "[$timeStamp] ALERTA: No se encontraron archivos de respaldo en $DIR_BACKUPS." >> "$ARCHIVO_LOG"
fi

echo "[$timeStamp] === FIN DE AUDITORÍA ===" >> "$ARCHIVO_LOG"