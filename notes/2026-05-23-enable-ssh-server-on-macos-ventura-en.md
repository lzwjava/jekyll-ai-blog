---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enable SSH Server on macOS Ventura
translated: false
type: note
---

**Question:** How to set up an SSH server on macOS Ventura so other LAN hosts can connect to it?

**Answer:**

macOS has a built-in OpenSSH server. One command to enable it:

```bash
sudo systemsetup -setremotelogin on
```

Verify it's running:

```bash
sudo systemsetup -getremotelogin
# Remote Login: On

sudo launchctl list | grep ssh
# Should show com.openssh.sshd
```

Check your LAN IP:

```bash
ipconfig getifaddr en0   # Wi-Fi
ipconfig getifaddr en1   # Ethernet
```

From another LAN machine, connect:

```bash
ssh zhiwei@192.168.1.x
```

---

**Optional hardening (recommended):**

Edit `/etc/ssh/sshd_config`:

```
PasswordAuthentication no        # key-only auth
PermitRootLogin no
AllowUsers zhiwei
```

Restart sshd after config changes:

```bash
sudo launchctl stop com.openssh.sshd
sudo launchctl start com.openssh.sshd
```

---

**Firewall note:** If you have the macOS firewall on (`System Settings → Network → Firewall`), SSH (port 22) is automatically allowed when Remote Login is enabled. No manual rule needed.

**To turn it off later:**

```bash
sudo systemsetup -setremotelogin off
```