---
audio: false
generated: true
lang: en
layout: post
title: PowerShell Commands Guide
translated: false
type: note
---

## Introduction to PowerShell

PowerShell is a task automation and configuration management framework from Microsoft, consisting of a command-line shell and a scripting language. It is built on the .NET Framework (and .NET Core in newer versions), enabling administrators to perform complex tasks across Windows, Linux, and macOS systems.

PowerShell commands, known as **cmdlets** (pronounced "command-lets"), follow a `Verb-Noun` naming convention (e.g., `Get-Process`, `Set-Item`). This guide covers essential cmdlets, categorized by functionality, with examples to demonstrate their use.

---

## 1. Core PowerShell Concepts

Before diving into commands, understanding key concepts is crucial:

- **Cmdlets**: Lightweight commands that perform specific functions.
- **Pipelines**: Allow the output of one cmdlet to be passed as input to another using the `|` operator.
- **Modules**: Collections of cmdlets, scripts, and functions that extend PowerShell functionality.
- **Providers**: Interfaces to access data stores (e.g., file system, registry) as if they were drives.
- **Objects**: PowerShell works with objects, not plain text, enabling structured data manipulation.

---

## 2. Essential Cmdlets by Category

### 2.1 System Information

These cmdlets retrieve information about the system, processes, and services.

| Cmdlet | Description | Example |
|--------|-------------|---------|
| `Get-ComputerInfo` | Retrieves system hardware and software details. | `Get-ComputerInfo | Select-Object WindowsProductName, OsVersion` |
| `Get-Process` | Lists running processes. | `Get-Process | Where-Object {$_.CPU -gt 1000}` |
| `Get-Service` | Displays services on the system. | `Get-Service | Where-Object {$_.Status -eq "Running"}` |
| `Get-HotFix` | Lists installed Windows updates. | `Get-HotFix | Sort-Object InstalledOn -Descending` |

**Example**: List all running processes sorted by CPU usage.

```powershell
Get-Process | Sort-Object CPU -Descending | Select-Object Name, CPU, Id -First 5
```

### 2.2 File and Directory Management

PowerShell treats the file system as a provider, allowing navigation similar to a drive.

| Cmdlet | Description | Example |
|--------|-------------|---------|
| `Get-Item` | Retrieves files or directories. | `Get-Item C:\Users\*.txt` |
| `Set-Item` | Modifies item properties (e.g., file attributes). | `Set-Item -Path C:\test.txt -Value "New content"` |
| `New-Item` | Creates a new file or directory. | `New-Item -Path C:\Docs -Name Report.txt -ItemType File` |
| `Remove-Item` | Deletes files or directories. | `Remove-Item C:\Docs\OldFile.txt` |
| `Copy-Item` | Copies files or directories. | `Copy-Item C:\Docs\Report.txt D:\Backup` |
| `Move-Item` | Moves files or directories. | `Move-Item C:\Docs\Report.txt C:\Archive` |

**Example**: Create a directory and a file, then copy it to another location.

```powershell
New-Item -Path C:\Temp -Name MyFolder -ItemType Directory
New-Item -Path C:\Temp\MyFolder -Name Test.txt -ItemType File
Copy-Item C:\Temp\MyFolder\Test.txt C:\Backup
```

### 2.3 System Management

Cmdlets for managing system settings, services, and users.

| Cmdlet | Description | Example |
|--------|-------------|---------|
| `Start-Service` | Starts a service. | `Start-Service -Name "wuauserv"` |
| `Stop-Service` | Stops a service. | `Stop-Service -Name "wuauserv"` |
| `Restart-Computer` | Restarts the system. | `Restart-Computer -Force` |
| `Get-EventLog` | Retrieves event log entries. | `Get-EventLog -LogName System -Newest 10` |
| `Set-ExecutionPolicy` | Sets script execution policy. | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |

**Example**: Check the status of the Windows Update service and start it if stopped.

```powershell
$service = Get-Service -Name "wuauserv"
if ($service.Status -eq "Stopped") {
    Start-Service -Name "wuauserv"
}
```

### 2.4 Network Management

Cmdlets for network configuration and diagnostics.

| Cmdlet | Description | Example |
|--------|-------------|---------|
| `Test-Connection` | Pings a remote host. | `Test-Connection google.com` |
| `Get-NetAdapter` | Lists network adapters. | `Get-NetAdapter | Select-Object Name, Status` |
| `Get-NetIPAddress` | Retrieves IP address configurations. | `Get-NetIPAddress -AddressFamily IPv4` |
| `Resolve-DnsName` | Resolves DNS names. | `Resolve-DnsName www.google.com` |

**Example**: Ping a server and check its DNS resolution.

```powershell
Test-Connection -ComputerName google.com -Count 2
Resolve-DnsName google.com
```

### 2.5 User and Group Management

Cmdlets for managing local users and groups.

| Cmdlet | Description | Example |
|--------|-------------|---------|
| `New-LocalUser` | Creates a local user account. | `New-LocalUser -Name "TestUser" -Password (ConvertTo-SecureString "P@ssw0rd" -AsPlainText -Force)` |
| `Remove-LocalUser` | Deletes a local user account. | `Remove-LocalUser -Name "TestUser"` |
| `Get-LocalGroup` | Lists local groups. | `Get-LocalGroup | Select-Object Name` |
| `Add-LocalGroupMember` | Adds a user to a local group. | `Add-LocalGroupMember -Group "Administrators" -Member "TestUser"` |

**Example**: Create a new local user and add them to the Administrators group.

```powershell
$password = ConvertTo-SecureString "P@ssw0rd" -AsPlainText -Force
New-LocalUser -Name "TestUser" -Password $password -FullName "Test User" -Description "Test account"
Add-LocalGroupMember -Group "Administrators" -Member "TestUser"
```

### 2.6 Scripting and Automation

PowerShell excels in scripting for automation.

| Cmdlet | Description | Example |
|--------|-------------|---------|
| `Write-Output` | Outputs data to the pipeline. | `Write-Output "Hello, World!"` |
| `ForEach-Object` | Loops through items in a pipeline. | `Get-Process | ForEach-Object { $_.Name }` |
| `Where-Object` | Filters objects based on conditions. | `Get-Service | Where-Object { $_.Status -eq "Running" }` |
| `Invoke-Command` | Runs commands on local or remote computers. | `Invoke-Command -ComputerName Server01 -ScriptBlock { Get-Process }` |
| `New-ScheduledTask` | Creates a scheduled task. | `New-ScheduledTask -Action (New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File C:\script.ps1") -Trigger (New-ScheduledTaskTrigger -Daily -At "3AM")` |

**Example**: Create a script to log running processes to a file.

```powershell
$logPath = "C:\Logs\ProcessLog.txt"
Get-Process | Select-Object Name, CPU, StartTime | Export-Csv -Path $logPath -NoTypeInformation
```

### 2.7 Module Management

Modules extend PowerShell functionality.

| Cmdlet | Description | Example |
|--------|-------------|---------|
| `Get-Module` | Lists available or imported modules. | `Get-Module -ListAvailable` |
| `Import-Module` | Imports a module. | `Import-Module ActiveDirectory` |
| `Install-Module` | Installs a module from a repository. | `Install-Module -Name PSWindowsUpdate -Force` |
| `Find-Module` | Searches for modules in a repository. | `Find-Module -Name *Azure*` |

**Example**: Install and import the PSWindowsUpdate module to manage Windows updates.

```powershell
Install-Module -Name PSWindowsUpdate -Force
Import-Module PSWindowsUpdate
Get-WUList
```

---

## 3. Working with Pipelines

The pipeline (`|`) allows chaining cmdlets to process data sequentially. For example:

```powershell
Get-Process | Where-Object { $_.WorkingSet64 -gt 100MB } | Sort-Object WorkingSet64 -Descending | Select-Object Name, WorkingSet64 -First 5
```

This command:

1. Retrieves all processes.
2. Filters those using more than 100MB of memory.
3. Sorts them by memory usage in descending order.
4. Selects the top 5 processes, displaying their name and memory usage.

---

## 4. Variables, Loops, and Conditions

PowerShell supports scripting constructs for automation.

### Variables

```powershell
$path = "C:\Logs"
$services = Get-Service
Write-Output "Log path is $path"
```

### Loops

- **ForEach-Object**:

```powershell
Get-Service | ForEach-Object { Write-Output $_.Name }
```

- **For Loop**:

```powershell
for ($i = 1; $i -le 5; $i++) { Write-Output "Iteration $i" }
```

### Conditions

```powershell
$service = Get-Service -Name "wuauserv"
if ($service.Status -eq "Running") {
    Write-Output "Windows Update is running."
} else {
    Write-Output "Windows Update is stopped."
}
```

---

## 5. Error Handling

Use `Try`, `Catch`, and `Finally` for robust scripts.

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

## 6. Remote Management

PowerShell supports remote administration using `Invoke-Command` and `Enter-PSSession`.

**Example**: Run a command on a remote computer.

```powershell
Invoke-Command -ComputerName Server01 -ScriptBlock { Get-Service | Where-Object { $_.Status -eq "Running" } }
```

**Example**: Start an interactive remote session.

```powershell
Enter-PSSession -ComputerName Server01
```

---

## 7. Practical Script Example

Below is a sample script to monitor disk space and alert if usage exceeds 80%.

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

## 8. Tips for Effective PowerShell Usage

- **Use Aliases for Speed**: Common aliases like `dir` (`Get-ChildItem`), `ls` (`Get-ChildItem`), or `gci` (`Get-ChildItem`) save time in interactive sessions.
- **Get-Help**: Use `Get-Help <cmdlet>` for detailed documentation (e.g., `Get-Help Get-Process -Full`).
- **Update-Help**: Keep help files updated with `Update-Help`.
- **Profiles**: Customize your PowerShell environment by editing `$PROFILE` (e.g., `notepad $PROFILE`).
- **Tab Completion**: Press `Tab` to auto-complete cmdlets, parameters, and paths.
- **Use Verbose Output**: Add `-Verbose` to cmdlets for detailed execution information.

---

## 9. Additional Resources

- **Official Documentation**: [Microsoft PowerShell Docs](https://docs.microsoft.com/en-us/powershell/)
- **PowerShell Gallery**: [PowerShell Gallery](https://www.powershellgallery.com/) for modules.
- **Community**: Check posts on X or forums like Stack Overflow for real-time tips and scripts.
- **Learning**: Books like *PowerShell in Depth* or *Learn PowerShell in a Month of Lunches*.

---

PowerShell is a powerful scripting language and command-line shell developed by Microsoft. It is widely used for task automation and configuration management. Here are some commonly used PowerShell commands besides `Get-NetTCPConnection`:

1. **Get-Process**: Retrieves information about the processes that are running on the local computer or a remote computer.

2. **Get-Service**: Gets the services on a local or remote computer.

3. **Get-EventLog**: Retrieves events from event logs, including application, security, and system logs.

4. **Get-ChildItem**: Gets the items and child items in one or more specified locations (similar to `dir` in Command Prompt).

5. **Get-Content**: Gets the content of the item at the specified location (similar to `type` in Command Prompt).

6. **Set-ExecutionPolicy**: Changes the user preference for the PowerShell execution policy.

7. **Invoke-Command**: Runs commands on local and remote computers.

8. **New-Item**: Creates a new item, such as a file or directory.

9. **Remove-Item**: Deletes the specified items.

10. **Copy-Item**: Copies an item from one location to another.

11. **Move-Item**: Moves an item from one location to another.

12. **Rename-Item**: Renames an item in a PowerShell provider namespace.

13. **Get-Help**: Displays information about PowerShell commands and concepts.

14. **Select-Object**: Selects specified properties of an object or set of objects.

15. **Where-Object**: Selects objects from a collection based on their property values.

16. **Sort-Object**: Sorts objects by property values.

17. **Export-Csv**: Converts objects into a series of CSV strings and saves the strings to a file.

18. **Import-Csv**: Imports a CSV file and converts it into objects.

19. **Start-Process**: Starts one or more processes on the local computer.

20. **Stop-Process**: Stops one or more running processes.

These commands are just a few examples of what you can do with PowerShell. The language is highly extensible, and you can create custom cmdlets and scripts to automate complex tasks.
