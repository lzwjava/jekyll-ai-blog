---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enabling SSH on Windows Server 2012
translated: false
type: note
---

**Question: Can Windows Server 2012 be accessed through SSH?**

**Answer: Yes.** Windows Server 2012 can use SSH, but it is **not enabled by default** like Linux. You need to install and configure an SSH server.

The common choice today is **OpenSSH Server for Windows**.

### Option 1: Install OpenSSH Server (recommended)

Windows Server 2012 does not have the modern "Optional Features → OpenSSH Server" UI, so install it manually.

1. Download OpenSSH for Windows:

[Win32-OpenSSH GitHub repository](https://github.com/PowerShell/Win32-OpenSSH?utm_source=chatgpt.com)

Choose the appropriate build:

* `OpenSSH-Win64.zip` for 64-bit Windows Server 2012

Extract:

```powershell
C:\Program Files\OpenSSH
```

Install:

```powershell
cd "C:\Program Files\OpenSSH"

.\install-sshd.ps1
```

Start SSH service:

```powershell
Start-Service sshd
```

Enable at boot:

```powershell
Set-Service sshd -StartupType Automatic
```

Check:

```powershell
Get-Service sshd
```

---

### 2. Open Windows Firewall port 22

```powershell
New-NetFirewallRule `
    -Name sshd `
    -DisplayName "OpenSSH Server" `
    -Protocol TCP `
    -LocalPort 22 `
    -Action Allow
```

---

### 3. Connect from Linux/macOS

```bash
ssh username@server-ip
```

Example:

```bash
ssh administrator@192.168.1.100
```

From another Windows machine:

```powershell
ssh administrator@192.168.1.100
```

---

### Option 2: Use PowerShell Remoting instead

Windows-native alternative:

```powershell
Enter-PSSession -ComputerName server2012
```

or:

```powershell
Invoke-Command -ComputerName server2012 -ScriptBlock {
    hostname
}
```

But this usually requires WinRM configuration and is more Windows-specific.

---

### Notes for Server 2012

* SSH works fine on Windows Server 2012 / 2012 R2.
* Use **OpenSSH**, not old third-party SSH servers like PuTTY's server.
* If the server is exposed to the Internet:

  * disable password login
  * use SSH keys
  * restrict firewall source IPs

Example SSH key login:

Client:

```bash
ssh-keygen
```

Copy key:

```bash
scp ~/.ssh/id_rsa.pub administrator@server:/tmp/key.pub
```

Then configure:

```
C:\Users\Administrator\.ssh\authorized_keys
```

---

A typical modern setup is:

```
Linux/macOS laptop
        |
        | ssh
        v
Windows Server 2012
        |
        +-- PowerShell
        +-- IIS
        +-- .NET apps
        +-- SQL Server
```

So yes, Windows Server 2012 can be managed almost like a Linux server over SSH.
