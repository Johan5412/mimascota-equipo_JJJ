<#
  respaldo.ps1 · MiMascota · SO3 (PC Windows)
  Respalda la base local, comprueba que el respaldo esté completo, lo comprime,
  guarda una copia local con rotación y envía otra a la VM de Azure por SSH.
  Uso manual:  powershell -NoProfile -ExecutionPolicy Bypass -File respaldo.ps1
#>
param(
  [string]$Mysqldump    = 'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe',
  [string]$Cnf          = 'C:\mimascota\config\respaldo.cnf',
  [string]$BaseDatos    = 'administracionmascotasbd',
  [string]$DirRespaldos = 'C:\mimascota\respaldos',
  [string]$Log          = 'C:\mimascota\logs\respaldo.log',
  [int]   $Dias         = 7,
  [string]$Llave        = "$HOME\.ssh\mimascota_respaldo",
  [string]$Destino      = 'respaldo@IP_DE_LA_VM:/var/backups/mimascota/entrantes/'
)
$ErrorActionPreference = 'Stop'

function Escribir-Log([string]$Nivel, [string]$Mensaje) {
  $linea = '{0} [{1}] {2}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Nivel, $Mensaje
  Add-Content -Path $Log -Value $linea
  Write-Output $linea
}

New-Item -ItemType Directory -Force -Path $DirRespaldos, (Split-Path $Log) | Out-Null
$marca = Get-Date -Format 'yyyyMMdd_HHmmss'
$sql   = Join-Path $DirRespaldos "mimascota_$marca.sql"
$zip   = Join-Path $DirRespaldos "mimascota_$marca.zip"

try {
  # 1. Respaldo. --result-file escribe el archivo tal cual: con ">" PowerShell 5.1 lo pasaría a UTF-16 y lo dañaría
  & $Mysqldump "--defaults-file=$Cnf" --single-transaction --routines --triggers --no-tablespaces "--result-file=$sql" $BaseDatos
  if ($LASTEXITCODE -ne 0) { throw "mysqldump terminó con código $LASTEXITCODE" }

  # 2. Verificación: existe, no está vacío y mysqldump alcanzó a escribir su última línea
  if (-not (Test-Path $sql) -or (Get-Item $sql).Length -eq 0) { throw 'El respaldo quedó vacío' }
  if (-not (Select-String -Path $sql -Pattern '-- Dump completed' -SimpleMatch -Quiet)) { throw 'El respaldo está incompleto' }

  # 3. Compresión
  Compress-Archive -Path $sql -DestinationPath $zip -Force
  Remove-Item $sql
  $kb = [math]::Round((Get-Item $zip).Length / 1KB, 1)
  Escribir-Log 'OK' "Respaldo local $(Split-Path $zip -Leaf) ($kb KB)"

  # 4. Envío a Azure. BatchMode evita que se quede esperando una contraseña
  & scp -i $Llave -o BatchMode=yes -o ConnectTimeout=15 $zip $Destino
  if ($LASTEXITCODE -ne 0) { throw "scp terminó con código $($LASTEXITCODE): la copia local quedó, pero no llegó a Azure" }
  Escribir-Log 'OK' 'Copia enviada a Azure'

  # 5. Rotación de la copia local
  Get-ChildItem -Path $DirRespaldos -Filter 'mimascota_*.zip' |
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-$Dias) } |
    ForEach-Object { Remove-Item $_.FullName; Escribir-Log 'INFO' "Rotado $($_.Name)" }
  exit 0
}
catch {
  Escribir-Log 'ERROR' $_.Exception.Message
  if (Test-Path $sql) { Remove-Item $sql -ErrorAction SilentlyContinue }
  exit 1
}
