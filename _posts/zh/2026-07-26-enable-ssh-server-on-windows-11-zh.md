---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Windows 11上启用SSH服务器
translated: true
type: note
---

问题：**如何在 Windows 11 上启用 SSH 服务器，以便另一台机器可通过 SSH 连接？**

答案：

Windows 11 将 **OpenSSH Server** 作为可选功能提供。启用它，启动服务，并开放防火墙。

## 1. 安装 OpenSSH 服务器

以**管理员身份打开 PowerShell**：

```powershell
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH*'
```

你应看到类似输出：

```
OpenSSH.Client~~~~0.0.1.0   Installed
OpenSSH.Server~~~~0.0.1.0   NotPresent
```

安装服务器：

```powershell
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
```

---

## 2. 启动 SSH 服务

```powershell
Start-Service sshd
```

启用自动启动：

```powershell
Set-Service -Name sshd -StartupType Automatic
```

检查状态：

```powershell
Get-Service sshd
```

预期输出：

```
Status   Name
------   ----
Running  sshd
```

---

## 3. 在 Windows 防火墙中允许 SSH

通常安装时会自动创建此规则，但可验证：

```powershell
Get-NetFirewallRule -Name *ssh*
```

如果缺少规则，则添加：

```powershell
New-NetFirewallRule `
    -Name sshd `
    -DisplayName "OpenSSH Server" `
    -Enabled True `
    -Direction Inbound `
    -Protocol TCP `
    -Action Allow `
    -LocalPort 22
```

---

## 4. 查找 Windows 机器的 IP

```powershell
ipconfig
```

示例：

```
IPv4 Address . . . . . . : 192.168.1.100
```

---

## 5. 从另一台机器连接

在 Linux/macOS 上：

```bash
ssh username@192.168.1.100
```

示例：

```bash
ssh lzw@192.168.1.100
```

首次连接：

```
The authenticity of host ... can't be established.
Are you sure you want to continue connecting?
```

输入：

```
yes
```

然后输入 Windows 账户密码。

---

## 6. 推荐：使用 SSH 密钥

在你的 Linux/macOS 客户端上：

```bash
ssh-keygen -t ed25519
```

复制密钥：

```bash
ssh-copy-id username@192.168.1.100
```

Windows OpenSSH 将密钥存储在此处：

```
C:\Users\<username>\.ssh\authorized_keys
```

---

## 7. 检查 SSH 配置

Windows SSH 服务器配置文件：

```
C:\ProgramData\ssh\sshd_config
```

常用设置：

```text
Port 22
PubkeyAuthentication yes
PasswordAuthentication yes
```

修改后重启服务：

```powershell
Restart-Service sshd
```

---

对于你**局域网中的联想小新 Windows 11 机器**，以上步骤足够。然后你就可以像 Linux 盒子一样使用它：

```bash
ssh lenovo@192.168.1.x
```

并远程运行命令。
