---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Windows Server 2012上启用SSH
translated: true
type: note
---

**问题：Windows Server 2012 能否通过 SSH 访问？**

**答案：可以。** Windows Server 2012 可以使用 SSH，但**默认情况下未像 Linux 那样启用**。你需要安装并配置 SSH 服务器。

目前常用的选择是 **OpenSSH Server for Windows**。

### 选项 1：安装 OpenSSH Server（推荐）

Windows Server 2012 没有现代版的“可选功能 → OpenSSH Server”界面，因此需要手动安装。

1. 下载适用于 Windows 的 OpenSSH：

[Win32-OpenSSH GitHub 仓库](https://github.com/PowerShell/Win32-OpenSSH?utm_source=chatgpt.com)

选择适当的构建版本：

* `OpenSSH-Win64.zip` 适用于 64 位 Windows Server 2012

解压：

```powershell
C:\Program Files\OpenSSH
```

安装：

```powershell
cd "C:\Program Files\OpenSSH"

.\install-sshd.ps1
```

启动 SSH 服务：

```powershell
Start-Service sshd
```

设置为开机自启：

```powershell
Set-Service sshd -StartupType Automatic
```

检查：

```powershell
Get-Service sshd
```

---

### 2. 开放 Windows 防火墙端口 22

```powershell
New-NetFirewallRule `
    -Name sshd `
    -DisplayName "OpenSSH Server" `
    -Protocol TCP `
    -LocalPort 22 `
    -Action Allow
```

---

### 3. 从 Linux/macOS 连接

```bash
ssh username@server-ip
```

示例：

```bash
ssh administrator@192.168.1.100
```

从另一台 Windows 机器连接：

```powershell
ssh administrator@192.168.1.100
```

---

### 选项 2：改用 PowerShell 远程管理

Windows 原生替代方案：

```powershell
Enter-PSSession -ComputerName server2012
```

或：

```powershell
Invoke-Command -ComputerName server2012 -ScriptBlock {
    hostname
}
```

但这通常需要配置 WinRM，且更偏向 Windows 环境。

---

### Server 2012 注意事项

* SSH 在 Windows Server 2012 / 2012 R2 上运行良好。
* 请使用 **OpenSSH**，不要用旧版第三方 SSH 服务器（如 PuTTY 的服务器）。
* 如果服务器暴露在互联网上：

  * 禁用密码登录
  * 使用 SSH 密钥
  * 限制防火墙源 IP

SSH 密钥登录示例：

客户端：

```bash
ssh-keygen
```

复制密钥：

```bash
scp ~/.ssh/id_rsa.pub administrator@server:/tmp/key.pub
```

然后配置：

```
C:\Users\Administrator\.ssh\authorized_keys
```

---

一个典型的现代配置如下：

```
Linux/macOS 笔记本
        |
        | ssh
        v
Windows Server 2012
        |
        +-- PowerShell
        +-- IIS
        +-- .NET 应用程序
        +-- SQL Server
```

因此，是的，Windows Server 2012 可以通过 SSH 几乎像 Linux 服务器一样进行管理。
