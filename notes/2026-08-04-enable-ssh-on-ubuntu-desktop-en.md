---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enable SSH on Ubuntu Desktop
translated: false
type: note
---

Question: How to enable SSH access to an Ubuntu Desktop machine on a local LAN?

Answer:

On Ubuntu Desktop, install and enable the OpenSSH server.

### 1. Install SSH server

```bash
sudo apt update
sudo apt install openssh-server
```

Check status:

```bash
systemctl status ssh
```

You should see:

```
Active: active (running)
```

If not:

```bash
sudo systemctl enable --now ssh
```

---

### 2. Find the Ubuntu machine's LAN IP

Run:

```bash
ip addr
```

Example:

```
enp3s0:
    inet 192.168.1.100/24
```

Your SSH address is:

```
192.168.1.100
```

or:

```bash
hostname -I
```

---

### 3. SSH from another machine

From another Linux/macOS machine:

```bash
ssh username@192.168.1.100
```

Example:

```bash
ssh lzw@192.168.1.100
```

First connection:

```
The authenticity of host '192.168.1.100' can't be established.
Are you sure you want to continue connecting?
```

Type:

```
yes
```

Enter Ubuntu user's password.

---

### 4. If firewall is enabled

Check:

```bash
sudo ufw status
```

If active:

```bash
sudo ufw allow ssh
```

or:

```bash
sudo ufw allow 22/tcp
```

---

### 5. Better: use SSH keys (no password)

On your client machine:

```bash
ssh-keygen
```

Copy key:

```bash
ssh-copy-id username@192.168.1.100
```

Then:

```bash
ssh username@192.168.1.100
```

No password needed.

---

### 6. Optional: make it easier with hostname

Install mDNS:

```bash
sudo apt install avahi-daemon
```

Then from another machine:

```bash
ssh username@ubuntu-desktop.local
```

Check hostname:

```bash
hostname
```

---

### 7. Debug if connection fails

On Ubuntu server:

```bash
sudo ss -tlnp | grep ssh
```

Expected:

```
LISTEN 0 128 0.0.0.0:22
```

From client:

```bash
ping 192.168.1.100
```

Then:

```bash
ssh -v username@192.168.1.100
```

Common issues:

| Problem            | Fix                                   |
| ------------------ | ------------------------------------- |
| Connection refused | `sudo systemctl restart ssh`          |
| Timeout            | firewall/network issue                |
| Wrong IP           | `hostname -I`                         |
| Permission denied  | wrong username/password or SSH config |

For a home AI lab (Ubuntu + GPU server), I would also set up SSH keys + a static DHCP lease in your router, so the machine always keeps the same LAN IP.
