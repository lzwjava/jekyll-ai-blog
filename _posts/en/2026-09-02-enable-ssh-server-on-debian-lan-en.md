---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enable SSH Server on Debian LAN
translated: false
type: note
---

Question: How to enable an SSH server on Debian so another computer on the same LAN can connect.

Answer:

On the Debian machine you want to SSH **into**:

### 1. Install OpenSSH server

```bash
sudo apt update
sudo apt install openssh-server
```

### 2. Start and enable SSH

```bash
sudo systemctl enable --now ssh
```

Check:

```bash
systemctl status ssh
```

You want to see:

```text
Active: active (running)
```

### 3. Find the Debian machine's LAN IP

```bash
ip addr
```

Or simpler:

```bash
hostname -I
```

For example:

```text
192.168.1.123
```

### 4. SSH from the other computer

From Linux/macOS:

```bash
ssh your_username@192.168.1.123
```

For example:

```bash
ssh zhiwei@192.168.1.123
```

On the first connection, you'll see a host-key confirmation. Type:

```text
yes
```

Then enter the Debian user's password.

### 5. If it doesn't connect

Check that SSH is listening:

```bash
sudo ss -lntp | grep ':22'
```

You should see something like:

```text
LISTEN 0 128 0.0.0.0:22
```

Check the firewall:

```bash
sudo nft list ruleset
```

If you're using `ufw`:

```bash
sudo ufw status
```

and, if necessary:

```bash
sudo ufw allow 22/tcp
```

### 6. Useful: test from the other machine

```bash
ping 192.168.1.123
```

Then:

```bash
nc -vz 192.168.1.123 22
```

If you get:

```text
Connection to 192.168.1.123 22 port [tcp/ssh] succeeded!
```

the network path and SSH port are working.

**For a normal home/LAN Debian box, that's basically all you need:** install `openssh-server` → start `ssh` → find its LAN IP → `ssh user@IP`.

For security, I would use **SSH keys** rather than exposing password authentication, especially if this machine may eventually be reachable outside your LAN.
