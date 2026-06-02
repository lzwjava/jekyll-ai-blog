---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Linux Firewall Setup Guide
translated: false
type: note
---

Good question — setting up a firewall in Linux (like **Red Hat** or **Ubuntu**) mainly involves using either **`firewalld`** or **`ufw`**, depending on your system. Below is a clear guide for both families, so you can choose the right one.

---

### 🔹 On **Red Hat / CentOS / Fedora** (firewalld)

#### 1. Check if `firewalld` is installed and running

```bash
sudo systemctl status firewalld
```

If it’s not running:

```bash
sudo systemctl enable firewalld
sudo systemctl start firewalld
```

#### 2. Basic usage

Check active zones (zones group interfaces and rules):

```bash
sudo firewall-cmd --get-active-zones
```

List all rules for the current zone:

```bash
sudo firewall-cmd --list-all
```

#### 3. Allow or block ports/services

Allow a port (e.g. SSH on port 22):

```bash
sudo firewall-cmd --permanent --add-port=22/tcp
```

Allow a known service (e.g. HTTP):

```bash
sudo firewall-cmd --permanent --add-service=http
```

Block/remove one:

```bash
sudo firewall-cmd --permanent --remove-service=http
```

Reload to apply:

```bash
sudo firewall-cmd --reload
```

#### 4. Verify rules

```bash
sudo firewall-cmd --list-all
```

---

### 🔹 On **Ubuntu / Debian** (ufw)

Ubuntu ships with **UFW** (Uncomplicated Firewall), simpler to manage.

#### 1. Enable UFW

```bash
sudo ufw enable
```

#### 2. Allow/deny ports or services

Allow SSH:

```bash
sudo ufw allow ssh
```

Allow HTTP (port 80):

```bash
sudo ufw allow 80/tcp
```

Allow a specific port range:

```bash
sudo ufw allow 1000:2000/tcp
```

Deny a service:

```bash
sudo ufw deny 23/tcp
```

#### 3. Check status

```bash
sudo ufw status verbose
```

#### 4. Reset rules if needed

```bash
sudo ufw reset
```

---

### 🔹 For both systems

To **block all incoming traffic except a few**, you can:

1. Deny all incoming by default

   ```bash
   sudo ufw default deny incoming
   sudo ufw default allow outgoing
   ```

   *(for `firewalld`, use zones or drop zones for similar behavior)*

2. Then selectively allow ports (e.g., 22, 80, 443).

---

### 🔹 Security Tip

Always **allow SSH first** before enabling or changing firewall rules remotely — otherwise you’ll lock yourself out.

---

Would you like me to show an **example minimal firewall setup** (e.g. for a typical web server allowing only SSH + HTTP + HTTPS)?
