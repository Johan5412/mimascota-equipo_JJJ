# ==============================================================================
# Script de Restauración de Base de Datos - MiMascota (SO4)
# ==============================================================================

param (
    [string]$NombreArchivoZip  # Ejemplo: backup_administracionmascotasbd_20261110_230000.zip
)

$IP_AZURE       = "20.114.49.220"
$USUARIO_AZURE  = "respaldo"
$LLAVE_SSH      = "$HOME\.ssh\mimascota_respaldo"

$DIR_CONFIG     = "C:\mimascota\config\respaldo.cnf"
$DIR_BACKUPS    = "C:\mimascota\backups"
$DIR_LOGS       = "C:\mimascota\logs"
$BASE_DATOS     = "administracionmascotasbd"
$ARCHIVO_LOG    = "$DIR_LOGS\restaurar.log"

function Escribir-Log {
    param ([string]$mensaje)
    $timeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$timeStamp] $mensaje" | Out-File -FilePath $ARCHIVO_LOG -Append -Encoding utf8
    Write-Host "[$timeStamp] $mensaje"
}

if (-not $NombreArchivoZip) {
    Write-Host "Uso: .\restaurar.ps1 -NombreArchivoZip 'backup_administracionmascotasbd_YYYYMMDD_HHMMSS.zip'" -ForegroundColor Yellow
    exit 1
}

Escribir-Log "=== INICIANDO PROCESO DE RESTAURACIÓN ==="

$MYSQL = "mysql"
if (-not (Get-Command mysql -ErrorAction SilentlyContinue)) {
    if (Test-Path "C:\xampp\mysql\bin\mysql.exe") {
        $MYSQL = "C:\xampp\mysql\bin\mysql.exe"
    }
}

try {
    $RutaZipLocal = "$DIR_BACKUPS\$NombreArchivoZip"
    Escribir-Log "Descargando $NombreArchivoZip desde Azure..."
    scp -i $LLAVE_SSH -o StrictHostKeyChecking=no "${USUARIO_AZURE}@${IP_AZURE}:/var/backups/mimascota/$NombreArchivoZip" $RutaZipLocal

    Escribir-Log "Descomprimiendo archivo de respaldo..."
    Expand-Archive -Path $RutaZipLocal -DestinationPath $DIR_BACKUPS -Force
    $ArchivoSql = $RutaZipLocal.Replace(".zip", ".sql")

    Escribir-Log "Restaurando base de datos '$BASE_DATOS'..."
    Get-Content $ArchivoSql | & $MYSQL "--defaults-extra-file=$DIR_CONFIG" $BASE_DATOS

    Escribir-Log "RESTAURACIÓN COMPLETADA CON ÉXITO."
    Remove-Item -Path $ArchivoSql -Force
} catch {
    Escribir-Log "ERROR EN LA RESTAURACIÓN: $_"
}

Escribir-Log "=== FIN DEL PROCESO DE RESTAURACIÓN ==="