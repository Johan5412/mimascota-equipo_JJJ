<#
  tareas.ps1 · MiMascota · SO5 (PC Windows)
  Registra las dos tareas programadas. Ejecutar una vez, como el usuario que usa la app.
#>
$dir = 'C:\mimascota\so\windows'
$ps  = 'powershell.exe'

# Respaldo diario a las 7:00 p. m.; si el PC estaba apagado, corre apenas se encienda
$accion  = New-ScheduledTaskAction -Execute $ps -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$dir\respaldo.ps1`""
$cuando  = New-ScheduledTaskTrigger -Daily -At '19:00'
$ajustes = New-ScheduledTaskSettingsSet -StartWhenAvailable
Register-ScheduledTask -TaskName 'MiMascota-Respaldo' -Action $accion -Trigger $cuando -Settings $ajustes `
  -Description 'Respaldo diario de la base y envío a Azure' -Force

# Monitoreo cada 5 minutos entre las 7:00 a. m. y las 9:00 p. m. (horario de la clínica)
$accion = New-ScheduledTaskAction -Execute $ps -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$dir\monitor.ps1`""
$cuando = New-ScheduledTaskTrigger -Daily -At '07:00'
$cuando.Repetition = (New-ScheduledTaskTrigger -Once -At '07:00' -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Hours 14)).Repetition
Register-ScheduledTask -TaskName 'MiMascota-Monitor' -Action $accion -Trigger $cuando -Settings $ajustes `
  -Description 'Monitoreo de MySQL, disco, RAM y respaldos' -Force

Get-ScheduledTask -TaskName 'MiMascota-*' | Select-Object TaskName, State
