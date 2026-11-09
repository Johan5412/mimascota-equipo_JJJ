#!/usr/bin/env bash
# verificar_respaldo.sh · MiMascota · SO4 (VM de Azure)
# Restaura cada copia recibida en una base de prueba. Si funciona, la mueve a verificados/;
# si no, a rechazados/. Corre como root desde cron.
set -Eeuo pipefail
umask 027

BASE=/var/backups/mimascota
ENTRANTES=$BASE/entrantes
VERIFICADOS=$BASE/verificados
RECHAZADOS=$BASE/rechazados
LOG=/var/log/mimascota/verificacion.log
BD_PRUEBA=mimascota_verif
TABLAS_MIN=${TABLAS_MIN:-6}     # número de tablas de su modelo (la base de partida tiene 6)
DIAS=7

log() { printf '%s [%s] %s\n' "$(date '+%F %T')" "$1" "$2" >> "$LOG"; }

mkdir -p "$(dirname "$LOG")"
exec 9>/run/lock/verificar_respaldo.lock
flock -n 9 || { log ERROR "Ya hay una verificación en curso"; exit 1; }

shopt -s nullglob
copias=("$ENTRANTES"/mimascota_*.zip)
(( ${#copias[@]} > 0 )) || log ALERTA "No llegaron respaldos nuevos desde la última verificación"

for zip in "${copias[@]}"; do
  nombre=$(basename "$zip")
  mysql -e "DROP DATABASE IF EXISTS $BD_PRUEBA; CREATE DATABASE $BD_PRUEBA;"
  if unzip -p "$zip" '*.sql' | mysql "$BD_PRUEBA" 2>>"$LOG"; then
    tablas=$(mysql -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$BD_PRUEBA'")
    if (( tablas >= TABLAS_MIN )); then
      mv "$zip" "$VERIFICADOS/"
      chown root:respaldo "$VERIFICADOS/$nombre"; chmod 640 "$VERIFICADOS/$nombre"   # respaldo lee, pero no modifica
      log OK "$nombre restaurado en $BD_PRUEBA: $tablas tablas"
    else
      mv "$zip" "$RECHAZADOS/"
      log ERROR "$nombre: solo $tablas tablas (se esperaban $TABLAS_MIN)"
    fi
  else
    mv "$zip" "$RECHAZADOS/"
    log ERROR "$nombre no se pudo restaurar"
  fi
done

mysql -e "DROP DATABASE IF EXISTS $BD_PRUEBA;"
find "$VERIFICADOS" -name 'mimascota_*.zip' -mtime +"$DIAS" -print -delete | while read -r f; do log INFO "Rotado $(basename "$f")"; done
