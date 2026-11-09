<#
  monitor.ps1 · MiMascota · SO6 (PC Windows)
  Una línea por ejecución en monitor.log; [ALERTA] si algo supera un umbral.
#>
param(
  [string]$Servicio      = 'MySQL80',
  [string]$Log           = 'C:\mimascota\logs\monitor.log',
  [string]$DirRespaldos  = 'C:\mimascota\respaldos',
  [int]   $MinDiscoLibre = 15,   # % mínimo libre en C:
  [int]   $MinRamLibre   = 15,   # % mínimo de RAM libre
  [int]   $HorasRespaldo = 26    # edad máxima del último respaldo local
)
$ErrorActionPreference = 'Stop'
$alertas = @()

$os         = Get-CimInstance Win32_OperatingSystem
$ramLibre   = [math]::Round(100 * $os.FreePhysicalMemory / $os.TotalVisibleMemorySize, 1)
$disco      = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"
$discoLibre = [math]::Round(100 * $disco.FreeSpace / $disco.Size, 1)
$cpu        = [math]::Round((Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average)

$svc    = Get-Service -Name $Servicio -ErrorAction SilentlyContinue
$estado = if ($svc) { [string]$svc.Status } else { 'NoExiste' }
$proc   = Get-Process -Name mysqld -ErrorAction SilentlyContinue | Select-Object -First 1
$memMB  = if ($proc) { [math]::Round($proc.WorkingSet64 / 1MB) } else { 0 }
$pid_   = if ($proc) { $proc.Id } else { '-' }
$ultimo = Get-ChildItem -Path $DirRespaldos -Filter 'mimascota_*.zip' -ErrorAction SilentlyContinue |
          Sort-Object LastWriteTime -Descending | Select-Object -First 1

if ($ramLibre -lt $MinRamLibre)     { $alertas += "RAM libre $ramLibre %" }
if ($discoLibre -lt $MinDiscoLibre) { $alertas += "disco C: libre $discoLibre %" }
if ($estado -ne 'Running')          { $alertas += "servicio $Servicio en estado $estado" }
if (-not $ultimo -or $ultimo.LastWriteTime -lt (Get-Date).AddHours(-$HorasRespaldo)) {
  $alertas += "sin respaldo local en las últimas $HorasRespaldo h"
}

$nivel = if ($alertas.Count -gt 0) { 'ALERTA' } else { 'OK' }
$linea = '{0} [{1}] cpu={2}% ram_libre={3}% disco_libre={4}% {5}={6} mysqld_pid={7} mysqld_mem={8}MB {9}' -f `
  (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $nivel, $cpu, $ramLibre, $discoLibre, $Servicio, $estado, $pid_, $memMB, ($alertas -join '; ')
New-Item -ItemType Directory -Force -Path (Split-Path $Log) | Out-Null
Add-Content -Path $Log -Value $linea
Write-Output $linea
