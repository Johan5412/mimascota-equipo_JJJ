# ==============================================================================
# Script de Respaldo Automatizado - MiMascota (SO3)
# ==============================================================================

$IP_AZURE       = "20.114.49.220"  # Reemplaza por la IP pública real de tu VM en Azure
$USUARIO_AZURE  = "respaldo"
$LLAVE_SSH      = "$HOME\.ssh\mimascota_respaldo"

$DIR_CONFIG     = "C:\mimascota\config\respaldo.cnf"
$DIR_BACKUPS    = "C:\mimascota\backups"
$DIR_LOGS       = "C:\mimascota\logs"

$FECHA          = Get-Date -Format "yyyyMMdd_HHmmss"
$BASE_DATOS     = "administracionmascotasbd"
$ARCHIVO_SQL    = "$DIR_BACKUPS\backup_${BASE_DATOS}_$FECHA.sql"
$ARCHIVO_ZIP    = "$DIR_BACKUPS\backup_${BASE_DATOS}_$FECHA.zip"
$ARCHIVO_LOG    = "$DIR_LOGS\respaldo.log"

if (-not (Test-Path $DIR_BACKUPS)) { New-Item -ItemType Directory -Path $DIR_BACKUPS | Out-Null }
if (-not (Test-Path $DIR_LOGS))    { New-Item -ItemType Directory -Path $DIR_LOGS | Out-Null }

function Escribir-Log {
    param ([string]$mensaje)
    $timeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$timeStamp] $mensaje" | Out-File -FilePath $ARCHIVO_LOG -Append -Encoding utf8
    Write-Host "[$timeStamp] $mensaje"
}

Escribir-Log "=== INICIANDO PROCESO DE RESPALDO ==="

$MYSQLDUMP = "mysqldump"
if (-not (Get-Command mysqldump -ErrorAction SilentlyContinue)) {
    if (Test-Path "C:\xampp\mysql\bin\mysqldump.exe") {
        $MYSQLDUMP = "C:\xampp\mysql\bin\mysqldump.exe"
    } else {
        Escribir-Log "ERROR: No se encontró mysqldump.exe."
        exit 1
    }
}

try {
    Escribir-Log "Generando volcado SQL de '$BASE_DATOS'..."
    & $MYSQLDUMP "--defaults-extra-file=$DIR_CONFIG" $BASE_DATOS --result-file=$ARCHIVO_SQL

    if (-not (Test-Path $ARCHIVO_SQL) -or (Get-Item $ARCHIVO_SQL).Length -eq 0) {
        throw "El archivo SQL no se generó o está vacío."
    }

    Escribir-Log "Comprimiendo archivo a ZIP..."
    Compress-Archive -Path $ARCHIVO_SQL -DestinationPath $ARCHIVO_ZIP -Force
    Remove-Item -Path $ARCHIVO_SQL -Force

    Escribir-Log "Enviando archivo ZIP a Azure VM ($IP_AZURE)..."
    scp -i $LLAVE_SSH -o StrictHostKeyChecking=no $ARCHIVO_ZIP "${USUARIO_AZURE}@${IP_AZURE}:/var/backups/mimascota/"

    if ($LASTEXITCODE -eq 0) {
        Escribir-Log "TRANSFERENCIA EXITOSA a la VM en Azure."
    } else {
        throw "Fallo en la transferencia por SCP."
    }
} catch {
    Escribir-Log "ERROR EN EL PROCESO: $_"
}

Escribir-Log "=== FIN DEL PROCESO DE RESPALDO ==="