# ==============================================================================
# Script de Monitoreo de Recursos y Servicios - MiMascota (SO6)
# ==============================================================================

$DIR_LOGS     = "C:\mimascota\logs"
$ARCHIVO_LOG  = "$DIR_LOGS\monitor.log"
$UMBRAL_DISCO = 10  # Porcentaje mínimo de disco libre

if (-not (Test-Path $DIR_LOGS)) { New-Item -ItemType Directory -Path $DIR_LOGS | Out-Null }

function Escribir-Log {
    param ([string]$mensaje)
    $timeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$timeStamp] $mensaje" | Out-File -FilePath $ARCHIVO_LOG -Append -Encoding utf8
    Write-Host "[$timeStamp] $mensaje"
}

Escribir-Log "--- AUDITORÍA DE MONITOREO ---"

# 1. Verificación del proceso / servicio MySQL
$MysqlProceso = Get-Process -Name "mysqld" -ErrorAction SilentlyContinue
if ($MysqlProceso) {
    Escribir-Log "ESTADO MYSQL: En ejecución (PID: $($MysqlProceso.Id))"
} else {
    Escribir-Log "ALERTA MYSQL: El servicio/proceso mysqld NO está ejecutándose."
}

# 2. Verificación de espacio en Disco C:
$DiscoC = Get-Volume -DriveLetter C
$PorcentajeLibre = [math]::Round(($DiscoC.SizeRemaining / $DiscoC.Size) * 100, 2)

if ($PorcentajeLibre -lt $UMBRAL_DISCO) {
    Escribir-Log "ALERTA DISCO: Espacio libre crítico en C: ($PorcentajeLibre%)"
} else {
    Escribir-Log "ESTADO DISCO: Espacio libre aceptable en C: ($PorcentajeLibre%)"
}