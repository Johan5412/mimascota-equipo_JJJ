# ==============================================================================
# Registro en Programador de Tareas de Windows - MiMascota (SO5)
# ==============================================================================

$NombreTarea = "MiMascota_Respaldo_Diario"
$RutaScript  = "C:\mimascota\scripts\respaldo.ps1"

# Definir la acción (Ejecutar PowerShell con el script de respaldo)
$Accion = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$RutaScript`""

# Definir el disparador (Todos los días a las 23:00)
$Disparador = New-ScheduledTaskTrigger -Daily -At "23:00"

# Definir configuraciones de la tarea
$Configuracion = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

# Registrar la tarea en el sistema
Register-ScheduledTask -TaskName $NombreTarea -Action $Accion -Trigger $Disparador -Settings $Configuracion -User "SYSTEM" -RunLevel Highest -Force

Write-Host "Tarea programada '$NombreTarea' registrada con éxito en Windows." -ForegroundColor Green