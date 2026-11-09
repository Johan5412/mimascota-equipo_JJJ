<#
  restaurar.ps1 · MiMascota · SO4 (PC Windows)
  Trae de Azure la última copia verificada y la restaura en la base local.
  Cierre la aplicación antes de ejecutarlo. Pide la contraseña de root de MySQL.
#>
param(
  [string]  $Mysql          = 'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe',
  [string[]]$Credenciales   = @('--user=root', '--password', '--host=127.0.0.1'),
  [string]  $BaseDatos      = 'administracionmascotasbd',
  [string]  $DirRestaurar   = 'C:\mimascota\restaurar',
  [string]  $Log            = 'C:\mimascota\logs\respaldo.log',
  [string]  $Llave          = "$HOME\.ssh\mimascota_respaldo",
  [string]  $Servidor       = 'respaldo@IP_DE_LA_VM',
  [string]  $DirVerificados = '/var/backups/mimascota/verificados',
  [switch]  $Si
)
$ErrorActionPreference = 'Stop'

function Escribir-Log([string]$Nivel, [string]$Mensaje) {
  $linea = '{0} [{1}] {2}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Nivel, $Mensaje
  Add-Content -Path $Log -Value $linea
  Write-Output $linea
}

try {
  New-Item -ItemType Directory -Force -Path $DirRestaurar, (Split-Path $Log) | Out-Null

  # 1. Buscar la copia verificada más reciente en Azure
  $remoto = & ssh -i $Llave -o BatchMode=yes -o ConnectTimeout=15 $Servidor "ls -1t $DirVerificados/mimascota_*.zip 2>/dev/null | head -n 1"
  if ($LASTEXITCODE -ne 0 -or -not $remoto) { throw 'No hay copias verificadas en Azure o la VM no responde' }
  $nombre = Split-Path $remoto -Leaf
  Write-Output "Copia más reciente verificada: $nombre"

  # 2. Confirmación: la restauración reemplaza las tablas actuales
  if (-not $Si) {
    $r = Read-Host "Se reemplazará la base $BaseDatos con $nombre. Escriba SI para continuar"
    if ($r -ne 'SI') { Write-Output 'Cancelado'; exit 2 }
  }

  # 3. Descargar y descomprimir
  $zip = Join-Path $DirRestaurar $nombre
  & scp -i $Llave -o BatchMode=yes "$($Servidor):$remoto" $zip
  if ($LASTEXITCODE -ne 0) { throw "No se pudo descargar $nombre" }
  Expand-Archive -Path $zip -DestinationPath $DirRestaurar -Force
  $sql = Join-Path $DirRestaurar ($nombre -replace '\.zip$', '.sql')

  # 4. Restaurar. mysql.exe no recibe archivos con "<" en PowerShell: se usa el comando source
  $ruta = $sql -replace '\\', '/'
  & $Mysql @Credenciales -e "CREATE DATABASE IF NOT EXISTS $BaseDatos; USE $BaseDatos; source $ruta; SELECT COUNT(*) AS tablas FROM information_schema.tables WHERE table_schema = '$BaseDatos';"
  if ($LASTEXITCODE -ne 0) { throw "mysql terminó con código $LASTEXITCODE" }
  Escribir-Log 'OK' "Base $BaseDatos restaurada desde $nombre"
  Remove-Item $sql
  exit 0
}
catch {
  Escribir-Log 'ERROR' "Restauración: $($_.Exception.Message)"
  exit 1
}
