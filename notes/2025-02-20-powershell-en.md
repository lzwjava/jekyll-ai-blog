---
audio: false
generated: false
lang: en
layout: post
title: PowerShell Commands
translated: false
type: note
---

For PowerShell scripts, the conventional file extension is `.ps1`. Here's how you would list these commands in a `.ps1` file:

**File Name: `common_commands.ps1`**

```powershell
Get-Command -Verb Get
Get-Help Get-Process -Full
Get-Process java
Stop-Process -Name java -Force
Start-Process -FilePath "java" -ArgumentList "-jar", "app.jar"
Get-Service -Name mysql
Start-Service -Name mysql
Stop-Service -Name mysql
Get-ChildItem -Path "C:\Projects\MySpringApp"
Remove-Item -Path "C:\Logs\*.log"
Copy-Item -Path "C:\Source\config.properties" -Destination "C:\Destination"
New-Item -Path "C:\Projects\NewSpringProject" -ItemType Directory
Set-Location -Path "C:\Projects\MySpringApp"
Invoke-WebRequest -Uri "http://localhost:8080/api/v1/resource" -Method Get
Test-NetConnection -ComputerName "localhost" -Port 8080
Get-Content -Path "C:\Logs\app.log" -Tail 100
Set-Content -Path "C:\Config\db.properties" -Value "db.url=jdbc:mysql://localhost:3306/mydb"
Add-Content -Path "C:\Logs\app.log" -Value "Application started at $(Get-Date)"
Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Get-Content -Path "C:\Logs\app.log" | Measure-Object -Line
@{Name="John"; Age=30} | ConvertTo-Json
```

This file can be saved with a `.ps1` extension, which identifies it as a PowerShell script. To run this script, you would use:

```powershell
.\common_commands.ps1
```

Please note that you might need to adjust your execution policy to run PowerShell scripts:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

This command allows scripts to run, but remember to set it back or use it cautiously as it affects system security settings.
