---
audio: false
generated: true
image: false
lang: en
layout: post
title: Grant OpenClaw Sudo Access on Linux
translated: false
type: note
---

Question: How do I give OpenClaw sudo access on Linux?

Answer:

## ⚠️ Why OpenClaw Needs sudo Access

OpenClaw runs shell commands on your behalf as an AI agent. When it needs to run system-level commands (e.g., `apt install`, `systemctl`, file operations in `/etc`), it needs sudo privileges.

---

## Option 1 — Add OpenClaw User to sudo Group (Simplest)

Since OpenClaw runs as your user (`lzw`), just ensure `lzw` is in the sudo group:

```bash
sudo usermod -aG sudo lzw
```

Verify:

```bash
groups lzw
# should show: lzw : lzw sudo
```

This requires password every time sudo is used. OpenClaw may fail on unattended commands because it **cannot type a password**.

---

## Option 2 — Passwordless sudo for Your User (Recommended for OpenClaw)

Allow `lzw` to run ALL sudo commands without password prompt:

### Step 1 — Edit sudoers safely

```bash
sudo visudo
```

### Step 2 — Add this line at the bottom

```
lzw ALL=(ALL) NOPASSWD: ALL
```

Save and exit (`Ctrl+X` → `Y` → Enter if using nano).

### Step 3 — Test it works

```bash
sudo whoami
# should return: root  (without asking for password)
```

---

## Option 3 — Passwordless sudo for Specific Commands Only (Most Secure)

If you want to limit what OpenClaw can do with sudo, whitelist only specific commands:

```bash
sudo visudo
```

Add at the bottom:

```
lzw ALL=(ALL) NOPASSWD: /usr/bin/apt, /usr/bin/apt-get, /bin/systemctl, /usr/bin/npm, /bin/mkdir, /bin/cp, /bin/mv, /bin/rm, /bin/chmod, /bin/chown
```

Adjust the command list to whatever you expect OpenClaw to need.

---

## Option 4 — Create a Dedicated sudoers Drop-in File (Cleanest)

Instead of editing the main sudoers file, create a separate file:

```bash
sudo nano /etc/sudoers.d/openclaw
```

Add:

```
lzw ALL=(ALL) NOPASSWD: ALL
```

Set correct permissions:

```bash
sudo chmod 0440 /etc/sudoers.d/openclaw
```

Verify it is valid:

```bash
sudo visudo -c
# should say: /etc/sudoers.d/openclaw: parsed OK
```

---

## Verify OpenClaw Can Use sudo

Test by asking OpenClaw in chat to run a sudo command:

```
run: sudo apt update
```

Or test directly in terminal as `lzw`:

```bash
sudo apt update
# should run without password prompt
```

---

## Summary

| Option | Security | Convenience | Recommended? |
|---|---|---|---|
| Add to sudo group only | 🟡 Medium | ❌ Needs password | ❌ Won't work unattended |
| `NOPASSWD: ALL` in visudo | 🟡 Home use OK | ✅ Full access | ✅ Best for home server |
| `NOPASSWD` specific commands | ✅ Most secure | 🟡 Limited | ✅ Best for production |
| Drop-in `/etc/sudoers.d/openclaw` | 🟡 Same as above | ✅ Clean | ✅ Cleanest approach |

For a **home server** like yours, Option 2 or Option 4 with `NOPASSWD: ALL` is the most practical choice. Since your server is already behind your home router and UFW, the security risk is minimal.