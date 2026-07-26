---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enable SSH Server on Windows 11
translated: false
type: note
---

Question: **How to enable SSH server on Windows 11 so another machine can SSH into it?**

Answer:

Windows 11 includes **OpenSSH Server** as an optional feature. Enable it, start the service, and open the firewall.

## 1. Install OpenSSH Server

Open **PowerShell as Administrator**:

```powershell
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH*'
```

You should see:

```
OpenSSH.Client~~~~0.0.1.0   Installed
OpenSSH.Server~~~~0.0.1.0   NotPresent
```

Install server:

```powershell
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
```

---

## 2. Start SSH service

```powershell
Start-Service sshd
```

Enable auto-start:

```powershell
Set-Service -Name sshd -StartupType Automatic
```

Check:

```powershell
Get-Service sshd
```

Expected:

```
Status   Name
------   ----
Running  sshd
```

---

## 3. Allow SSH through Windows Firewall

Usually installation creates this automatically, but verify:

```powershell
Get-NetFirewallRule -Name *ssh*
```

If missing:

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

## 4. Find Windows machine IP

```powershell
ipconfig
```

Example:

```
IPv4 Address . . . . . . : 192.168.1.100
```

---

## 5. Connect from another machine

From Linux/macOS:

```bash
ssh username@192.168.1.100
```

Example:

```bash
ssh lzw@192.168.1.100
```

First connection:

```
The authenticity of host ... can't be established.
Are you sure you want to continue connecting?
```

Type:

```
yes
```

Then enter the Windows account password.

---

## 6. Recommended: use SSH keys

On your Linux/macOS client:

```bash
ssh-keygen -t ed25519
```

Copy key:

```bash
ssh-copy-id username@192.168.1.100
```

Windows OpenSSH stores keys here:

```
C:\Users\<username>\.ssh\authorized_keys
```

---

## 7. Check SSH config

Windows SSH server config:

```
C:\ProgramData\ssh\sshd_config
```

Useful settings:

```text
Port 22
PubkeyAuthentication yes
PasswordAuthentication yes
```

After changing:

```powershell
Restart-Service sshd
```

---

For a **Lenovo Xiaoxin Windows 11 machine on your LAN**, this is enough. Then you can treat it like a Linux box:

```bash
ssh lenovo@192.168.1.x
```

and run commands remotely.
