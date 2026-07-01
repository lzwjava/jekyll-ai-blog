---
audio: false
generated: true
lang: zh
layout: post
title: PowerShell 命令指南
translated: true
type: note
---

## PowerShell 简介

PowerShell 是微软推出的任务自动化与配置管理框架，包含命令行外壳和脚本语言。它基于 .NET Framework（新版本基于 .NET Core）构建，使管理员能够在 Windows、Linux 和 macOS 系统上执行复杂任务。

PowerShell 命令称为 **cmdlet**（发音为 command-lets），遵循 `动词-名词` 命名规范（例如 `Get-Process`、`Set-Item`）。本指南按功能分类介绍常用 cmdlet，并通过示例演示其用法。

---

## 1. PowerShell 核心概念

在深入学习命令前，理解关键概念至关重要：

- **Cmdlet**：执行特定功能的轻量级命令
- **管道**：通过 `|` 操作符将一个 cmdlet 的输出作为另一个 cmdlet 的输入
- **模块**：扩展 PowerShell 功能的 cmdlet、脚本和函数集合
- **提供程序**：访问数据存储（如文件系统、注册表）的接口，使其如同驱动器一样操作
- **对象**：PowerShell 处理的是对象而非纯文本，支持结构化数据操作

---

## 2. 按功能分类的常用 Cmdlet

### 2.1 系统信息

这些 cmdlet 用于获取系统、进程和服务相关信息。

| Cmdlet | 描述 | 示例 |
| -------- | ------------- | --------- |
| `Get-ComputerInfo` | 获取系统硬件和软件详情 | `Get-ComputerInfo | Select-Object WindowsProductName, OsVersion` |
| `Get-Process` | 列出运行中的进程 | `Get-Process | Where-Object {$_.CPU -gt 1000}` |
| `Get-Service` | 显示系统服务 | `Get-Service | Where-Object {$_.Status -eq "Running"}` |
| `Get-HotFix` | 列出已安装的 Windows 更新 | `Get-HotFix | Sort-Object InstalledOn -Descending` |

**示例**：按 CPU 使用率排序列出所有运行中的进程

```powershell
Get-Process | Sort-Object CPU -Descending | Select-Object Name, CPU, Id -First 5
```

### 2.2 文件和目录管理

PowerShell 将文件系统视为提供程序，允许像操作驱动器一样进行导航。

| Cmdlet | 描述 | 示例 |
| -------- | ------------- | --------- |
| `Get-Item` | 获取文件或目录 | `Get-Item C:\Users\*.txt` |
| `Set-Item` | 修改项目属性（如文件属性） | `Set-Item -Path C:\test.txt -Value "New content"` |
| `New-Item` | 创建新文件或目录 | `New-Item -Path C:\Docs -Name Report.txt -ItemType File` |
| `Remove-Item` | 删除文件或目录 | `Remove-Item C:\Docs\OldFile.txt` |
| `Copy-Item` | 复制文件或目录 | `Copy-Item C:\Docs\Report.txt D:\Backup` |
| `Move-Item` | 移动文件或目录 | `Move-Item C:\Docs\Report.txt C:\Archive` |

**示例**：创建目录和文件，然后复制到其他位置

```powershell
New-Item -Path C:\Temp -Name MyFolder -ItemType Directory
New-Item -Path C:\Temp\MyFolder -Name Test.txt -ItemType File
Copy-Item C:\Temp\MyFolder\Test.txt C:\Backup
```

### 2.3 系统管理

用于管理系统设置、服务和用户的 cmdlet。

| Cmdlet | 描述 | 示例 |
| -------- | ------------- | --------- |
| `Start-Service` | 启动服务 | `Start-Service -Name "wuauserv"` |
| `Stop-Service` | 停止服务 | `Stop-Service -Name "wuauserv"` |
| `Restart-Computer` | 重启系统 | `Restart-Computer -Force` |
| `Get-EventLog` | 获取事件日志条目 | `Get-EventLog -LogName System -Newest 10` |
| `Set-ExecutionPolicy` | 设置脚本执行策略 | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |

**示例**：检查 Windows 更新服务状态，如果停止则启动

```powershell
$service = Get-Service -Name "wuauserv"
if ($service.Status -eq "Stopped") {
    Start-Service -Name "wuauserv"
}
```

### 2.4 网络管理

用于网络配置和诊断的 cmdlet。

| Cmdlet | 描述 | 示例 |
| -------- | ------------- | --------- |
| `Test-Connection` | ping 远程主机 | `Test-Connection google.com` |
| `Get-NetAdapter` | 列出网络适配器 | `Get-NetAdapter | Select-Object Name, Status` |
| `Get-NetIPAddress` | 获取 IP 地址配置 | `Get-NetIPAddress -AddressFamily IPv4` |
| `Resolve-DnsName` | 解析 DNS 名称 | `Resolve-DnsName www.google.com` |

**示例**：ping 服务器并检查其 DNS 解析

```powershell
Test-Connection -ComputerName google.com -Count 2
Resolve-DnsName google.com
```

### 2.5 用户和组管理

用于管理本地用户和组的 cmdlet。

| Cmdlet | 描述 | 示例 |
| -------- | ------------- | --------- |
| `New-LocalUser` | 创建本地用户账户 | `New-LocalUser -Name "TestUser" -Password (ConvertTo-SecureString "P@ssw0rd" -AsPlainText -Force)` |
| `Remove-LocalUser` | 删除本地用户账户 | `Remove-LocalUser -Name "TestUser"` |
| `Get-LocalGroup` | 列出本地组 | `Get-LocalGroup | Select-Object Name` |
| `Add-LocalGroupMember` | 将用户添加到本地组 | `Add-LocalGroupMember -Group "Administrators" -Member "TestUser"` |

**示例**：创建新本地用户并添加到管理员组

```powershell
$password = ConvertTo-SecureString "P@ssw0rd" -AsPlainText -Force
New-LocalUser -Name "TestUser" -Password $password -FullName "Test User" -Description "Test account"
Add-LocalGroupMember -Group "Administrators" -Member "TestUser"
```

### 2.6 脚本编写与自动化

PowerShell 在自动化脚本编写方面表现卓越。

| Cmdlet | 描述 | 示例 |
| -------- | ------------- | --------- |
| `Write-Output` | 向管道输出数据 | `Write-Output "Hello, World!"` |
| `ForEach-Object` | 遍历管道中的项目 | `Get-Process | ForEach-Object { $_.Name }` |
| `Where-Object` | 基于条件过滤对象 | `Get-Service | Where-Object { $_.Status -eq "Running" }` |
| `Invoke-Command` | 在本地或远程计算机上运行命令 | `Invoke-Command -ComputerName Server01 -ScriptBlock { Get-Process }` |
| `New-ScheduledTask` | 创建计划任务 | `New-ScheduledTask -Action (New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File C:\script.ps1") -Trigger (New-ScheduledTaskTrigger -Daily -At "3AM")` |

**示例**：创建脚本将运行中的进程记录到文件

```powershell
$logPath = "C:\Logs\ProcessLog.txt"
Get-Process | Select-Object Name, CPU, StartTime | Export-Csv -Path $logPath -NoTypeInformation
```

### 2.7 模块管理

模块扩展 PowerShell 功能。

| Cmdlet | 描述 | 示例 |
| -------- | ------------- | --------- |
| `Get-Module` | 列出可用或已导入的模块 | `Get-Module -ListAvailable` |
| `Import-Module` | 导入模块 | `Import-Module ActiveDirectory` |
| `Install-Module` | 从存储库安装模块 | `Install-Module -Name PSWindowsUpdate -Force` |
| `Find-Module` | 在存储库中搜索模块 | `Find-Module -Name *Azure*` |

**示例**：安装并导入 PSWindowsUpdate 模块以管理 Windows 更新

```powershell
Install-Module -Name PSWindowsUpdate -Force
Import-Module PSWindowsUpdate
Get-WUList
```

---

## 3. 管道操作

管道 (`|`) 允许将 cmdlet 串联起来顺序处理数据。例如：

```powershell
Get-Process | Where-Object { $_.WorkingSet64 -gt 100MB } | Sort-Object WorkingSet64 -Descending | Select-Object Name, WorkingSet64 -First 5
```

此命令：

1. 获取所有进程
2. 过滤使用超过 100MB 内存的进程
3. 按内存使用量降序排序
4. 选择前 5 个进程，显示其名称和内存使用量

---

## 4. 变量、循环和条件

PowerShell 支持脚本结构以实现自动化。

### 变量

```powershell
$path = "C:\Logs"
$services = Get-Service
Write-Output "Log path is $path"
```

### 循环

- **ForEach-Object**：

```powershell
Get-Service | ForEach-Object { Write-Output $_.Name }
```

- **For 循环**：

```powershell
for ($i = 1; $i -le 5; $i++) { Write-Output "Iteration $i" }
```

### 条件

```powershell
$service = Get-Service -Name "wuauserv"
if ($service.Status -eq "Running") {
    Write-Output "Windows Update is running."
} else {
    Write-Output "Windows Update is stopped."
}
```

---

## 5. 错误处理

使用 `Try`、`Catch` 和 `Finally` 实现健壮的脚本。

```powershell
Try {
    Get-Item -Path C:\NonExistentFile.txt -ErrorAction Stop
}
Catch {
    Write-Output "Error: $($_.Exception.Message)"
}
Finally {
    Write-Output "Operation completed."
}
```

---

## 6. 远程管理

PowerShell 支持使用 `Invoke-Command` 和 `Enter-PSSession` 进行远程管理。

**示例**：在远程计算机上运行命令

```powershell
Invoke-Command -ComputerName Server01 -ScriptBlock { Get-Service | Where-Object { $_.Status -eq "Running" } }
```

**示例**：启动交互式远程会话

```powershell
Enter-PSSession -ComputerName Server01
```

---

## 7. 实用脚本示例

以下是一个监控磁盘空间并在使用率超过 80% 时发出警报的示例脚本。

```powershell
$disks = Get-Disk
$threshold = 80

foreach ($disk in $disks) {
    $freeSpacePercent = ($disk.FreeSpace / $disk.Size) * 100
    if ($freeSpacePercent -lt (100 - $threshold)) {
        Write-Output "Warning: Disk $($disk.Number) is at $("{0:N2}" -f (100 - $freeSpacePercent))% capacity."
    }
}
```

---

## 8. 高效使用 PowerShell 的技巧

- **使用别名提高效率**：常用别名如 `dir` (`Get-ChildItem`)、`ls` (`Get-ChildItem`) 或 `gci` (`Get-ChildItem`) 可在交互式会话中节省时间
- **Get-Help**：使用 `Get-Help <cmdlet>` 获取详细文档（例如 `Get-Help Get-Process -Full`）
- **Update-Help**：使用 `Update-Help` 保持帮助文件更新
- **配置文件**：通过编辑 `$PROFILE` 自定义 PowerShell 环境（例如 `notepad $PROFILE`）
- **Tab 补全**：按 `Tab` 键自动补全 cmdlet、参数和路径
- **使用详细输出**：向 cmdlet 添加 `-Verbose` 参数获取详细执行信息

---

## 9. 其他资源

- **官方文档**：[Microsoft PowerShell 文档](https://docs.microsoft.com/en-us/powershell/)
- **PowerShell Gallery**：[PowerShell Gallery](https://www.powershellgallery.com/) 获取模块
- **社区**：查看 X 平台或 Stack Overflow 等论坛获取实时提示和脚本
- **学习资源**：如《PowerShell in Depth》或《Learn PowerShell in a Month of Lunches》等书籍

---

PowerShell 是微软开发的强大脚本语言和命令行外壳，广泛用于任务自动化和配置管理。以下是除 `Get-NetTCPConnection` 外的一些常用 PowerShell 命令：

1. **Get-Process**：获取本地计算机或远程计算机上运行的进程信息

2. **Get-Service**：获取本地或远程计算机上的服务

3. **Get-EventLog**：从事件日志（包括应用程序、安全和系统日志）检索事件

4. **Get-ChildItem**：获取指定位置中的项目和子项目（类似于命令提示符中的 `dir`）

5. **Get-Content**：获取指定位置处项目的内容（类似于命令提示符中的 `type`）

6. **Set-ExecutionPolicy**：更改用户对 PowerShell 执行策略的偏好设置

7. **Invoke-Command**：在本地和远程计算机上运行命令

8. **New-Item**：创建新项目，如文件或目录

9. **Remove-Item**：删除指定项目

10. **Copy-Item**：将项目从一个位置复制到另一个位置

11. **Move-Item**：将项目从一个位置移动到另一个位置

12. **Rename-Item**：重命名 PowerShell 提供程序命名空间中的项目

13. **Get-Help**：显示有关 PowerShell 命令和概念的信息

14. **Select-Object**：选择对象或对象集的指定属性

15. **Where-Object**：根据属性值从集合中选择对象

16. **Sort-Object**：按属性值对对象排序

17. **Export-Csv**：将对象转换为一系列 CSV 字符串并将字符串保存到文件

18. **Import-Csv**：导入 CSV 文件并将其转换为对象

19. **Start-Process**：在本地计算机上启动一个或多个进程

20. **Stop-Process**：停止一个或多个正在运行的进程

这些命令只是 PowerShell 功能的少数示例。该语言具有高度可扩展性，您可以创建自定义 cmdlet 和脚本来自动化复杂任务。
