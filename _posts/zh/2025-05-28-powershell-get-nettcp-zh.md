---
audio: false
generated: true
lang: zh
layout: post
title: PowerShell：Get-NetTCPConnection 命令详解
translated: true
type: note
---

PowerShell 中的 `Get-NetTCPConnection` cmdlet 用于获取 Windows 系统上的 TCP 连接信息。该命令属于 `NetTCPIP` 模块，适用于 Windows 8/Windows Server 2012 及更高版本。以下是简明使用指南：

### 基础用法

运行 `Get-NetTCPConnection` 可列出所有活跃的 TCP 连接：

```powershell
Get-NetTCPConnection
```

该命令将返回本地地址、本地端口、远程地址、远程端口、连接状态和所属进程等详细信息。

### 常用参数

- **-State**：按连接状态筛选（如 Established、Listening、TimeWait）

  ```powershell
  Get-NetTCPConnection -State Established
  ```

- **-LocalPort**：按本地端口号筛选

  ```powershell
  Get-NetTCPConnection -LocalPort 80
  ```

- **-RemoteAddress**：按远程 IP 地址筛选

  ```powershell
  Get-NetTCPConnection -RemoteAddress 192.168.1.1
  ```

- **-RemotePort**：按远程端口筛选

  ```powershell
  Get-NetTCPConnection -RemotePort 443
  ```

- **-OwningProcess**：按连接所属的进程 ID (PID) 筛选

  ```powershell
  Get-NetTCPConnection -OwningProcess 1234
  ```

### 组合筛选

可组合多个参数进行精确查询：

```powershell
Get-NetTCPConnection -State Established -LocalPort 80
```

### 显示指定属性

通过 `Select-Object` 仅显示所需属性：

```powershell
Get-NetTCPConnection | Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, State
```

### 追溯进程信息

结合 `Get-Process` 定位连接对应的进程：

```powershell
Get-NetTCPConnection -LocalPort 80 | ForEach-Object { Get-Process -Id $_.OwningProcess }
```

### 排序与格式化输出

按指定字段（如本地端口）排序并以表格形式展示：

```powershell
Get-NetTCPConnection | Sort-Object LocalPort | Format-Table LocalAddress, LocalPort, RemoteAddress, RemotePort, State
```

### 实用场景示例

1. **列出所有监听状态的连接：**

   ```powershell
   Get-NetTCPConnection -State Listening
   ```

2. **查找特定远程服务器的连接：**

   ```powershell
   Get-NetTCPConnection -RemoteAddress "8.8.8.8"
   ```

3. **检查特定端口的占用进程：**

   ```powershell
   $connection = Get-NetTCPConnection -LocalPort 8080
   Get-Process -Id $connection.OwningProcess
   ```

### 注意事项

- **管理员权限**：获取系统进程等详细信息时需以管理员身份运行 PowerShell
- **IPv4/IPv6**：该 cmdlet 同时支持 IPv4 和 IPv6 连接
- **结果导出**：可通过 `Export-Csv` 保存输出结果：

  ```powershell
  Get-NetTCPConnection | Export-Csv -Path "tcp_connections.csv" -NoTypeInformation
  ```

如需完整帮助文档，请运行：

```powershell
Get-Help Get-NetTCPConnection -Full
```

若有特定使用场景需求，欢迎随时提出！
