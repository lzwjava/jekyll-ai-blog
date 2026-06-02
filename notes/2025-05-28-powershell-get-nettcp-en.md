---
audio: false
generated: true
lang: en
layout: post
title: 'PowerShell: Get-NetTCPConnection Usage'
translated: false
type: note
---

The `Get-NetTCPConnection` cmdlet in PowerShell retrieves information about TCP connections on a Windows system. It's part of the `NetTCPIP` module, available on Windows 8/Windows Server 2012 and later. Below is a concise guide on how to use it:

### Basic Usage
Run `Get-NetTCPConnection` to list all active TCP connections:

```powershell
Get-NetTCPConnection
```

This returns details like LocalAddress, LocalPort, RemoteAddress, RemotePort, State, and OwningProcess.

### Common Parameters
- **-State**: Filter by connection state (e.g., Established, Listening, TimeWait).
  ```powershell
  Get-NetTCPConnection -State Established
  ```
- **-LocalPort**: Filter by local port number.
  ```powershell
  Get-NetTCPConnection -LocalPort 80
  ```
- **-RemoteAddress**: Filter by remote IP address.
  ```powershell
  Get-NetTCPConnection -RemoteAddress 192.168.1.1
  ```
- **-RemotePort**: Filter by remote port.
  ```powershell
  Get-NetTCPConnection -RemotePort 443
  ```
- **-OwningProcess**: Filter by the process ID (PID) owning the connection.
  ```powershell
  Get-NetTCPConnection -OwningProcess 1234
  ```

### Combining Filters
You can combine parameters for more specific results:
```powershell
Get-NetTCPConnection -State Established -LocalPort 80
```

### Display Specific Properties
Use `Select-Object` to show only desired properties:
```powershell
Get-NetTCPConnection | Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, State
```

### Find Process Details
To identify the process behind a connection, combine with `Get-Process`:
```powershell
Get-NetTCPConnection -LocalPort 80 | ForEach-Object { Get-Process -Id $_.OwningProcess }
```

### Sort and Format Output
Sort results (e.g., by LocalPort) and format as a table:
```powershell
Get-NetTCPConnection | Sort-Object LocalPort | Format-Table LocalAddress, LocalPort, RemoteAddress, RemotePort, State
```

### Practical Examples
1. **List all listening connections:**
   ```powershell
   Get-NetTCPConnection -State Listening
   ```
2. **Find connections to a specific remote server:**
   ```powershell
   Get-NetTCPConnection -RemoteAddress "8.8.8.8"
   ```
3. **Check which process is using a specific port:**
   ```powershell
   $connection = Get-NetTCPConnection -LocalPort 8080
   Get-Process -Id $connection.OwningProcess
   ```

### Notes
- **Admin Privileges**: Some details (e.g., OwningProcess for system processes) may require running PowerShell as Administrator.
- **IPv4/IPv6**: The cmdlet handles both IPv4 and IPv6 connections.
- **Export Results**: Save output to a file with `Export-Csv`:
  ```powershell
  Get-NetTCPConnection | Export-Csv -Path "tcp_connections.csv" -NoTypeInformation
  ```

For more details, run:
```powershell
Get-Help Get-NetTCPConnection -Full
```

If you need specific examples or have a particular use case, let me know!
