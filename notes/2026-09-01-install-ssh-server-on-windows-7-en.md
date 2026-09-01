---
audio: false
generated: true
image: false
lang: en
layout: post
title: Install SSH Server on Windows 7
translated: false
type: note
---

**Question:** How do I install an SSH server on Windows 7, so I can copy files or use an AI agent to operate that computer remotely?

---

**Answer:**

Windows 7 doesn't have a built-in SSH server, but you can install **Win32-OpenSSH** from Microsoft's GitHub. Win32-OpenSSH GitHub releases support Windows 7 and up. Here's the full process:

---

## Step 1 — Download Win32-OpenSSH

Go to: **https://github.com/PowerShell/Win32-OpenSSH/releases**

Download `OpenSSH-Win64.zip` (for 64-bit) or `OpenSSH-Win32.zip` (for 32-bit).

---

## Step 2 — Install

Extract the contents to `C:\Program Files\OpenSSH`. Make sure that folder has Write permissions only for SYSTEM and Administrator groups — authenticated users should have Read and Execute only.

Then open **PowerShell as Administrator** and run:

```powershell
cd "C:\Program Files\OpenSSH"
powershell.exe -ExecutionPolicy Bypass -File install-sshd.ps1
```

---

## Step 3 — Open Firewall (Windows 7 method)

For Windows 7 (client desktop / Windows 2008 R2 and below), use this command instead of `New-NetFirewallRule`:

```cmd
netsh advfirewall firewall add rule name=sshd dir=in action=allow protocol=TCP localport=22
```

Or go to **Control Panel → Windows Firewall → Advanced Settings → Inbound Rules** and add a new rule for TCP port 22.

---

## Step 4 — Start the SSH Service

```powershell
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
```

---

## Step 5 — Connect & Use

**Copy files** from another machine using SCP or SFTP:

```bash
# Copy a file TO the Windows 7 machine
scp myfile.txt username@192.168.1.x:/C:/Users/username/Desktop/

# Or use an SFTP client like WinSCP or FileZilla
```

**Run commands remotely** via SSH:

```bash
ssh username@192.168.1.x
```

---

## Using an AI Agent to Operate It Remotely

Once SSH is running, an AI agent (like Claude via Claude Code, or any automation tool) can connect over SSH and:

- Execute shell commands
- Read/write files via SFTP
- Run scripts or programs

For **Claude specifically**, Claude Code supports SSH-based remote operation — you'd point it at the Windows 7 machine's IP with your credentials or SSH key. Alternatively, tools like **Fabric**, **Paramiko** (Python), or **Ansible** can script operations over SSH.

> ⚠️ **Security note:** Windows 7 is end-of-life (no security updates since 2020). Exposing SSH on a public IP is risky. Use it only on a local/private network, or behind a VPN.

---

References:
- [Install Win32-OpenSSH (GitHub Wiki)](https://github.com/PowerShell/Win32-OpenSSH/wiki/Install-Win32-OpenSSH)
- [Win32-OpenSSH Releases](https://github.com/PowerShell/Win32-OpenSSH/releases)
- [WinSCP: Installing SSH Server on Windows](https://winscp.net/eng/docs/guide_windows_openssh_server)
- [How to install OpenSSH on Windows 7/10 – Fred_151](https://fred151.net/site/2018/09/23/how-to-install-openssh-on-windows-7-10/)
