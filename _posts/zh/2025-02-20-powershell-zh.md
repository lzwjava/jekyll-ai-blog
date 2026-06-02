---
audio: false
generated: false
lang: zh
layout: post
title: PowerShell 命令
translated: true
type: note
---

对于 PowerShell 脚本，常规文件扩展名为 `.ps1`。以下是如何在 `.ps1` 文件中列出这些命令：

**文件名：`common_commands.ps1`**

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

该文件可保存为 `.ps1` 扩展名，标识为 PowerShell 脚本。运行此脚本需使用：

```powershell
.\common_commands.ps1
```

请注意，可能需要调整执行策略才能运行 PowerShell 脚本：

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

此命令允许运行脚本，但请注意这会影响系统安全设置，建议谨慎使用并在使用后恢复原设置。
