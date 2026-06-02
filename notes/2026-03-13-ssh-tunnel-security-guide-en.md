---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSH Tunnel Security Explained
translated: false
type: note
---

Question: Is it secure to use SSH tunneling (`ssh -N -L 18789:127.0.0.1:18789 lzw@192.168.1.36`) to access OpenClaw on a second home computer? Will it be exposed to the public internet or scanned by bots?

Answer:

## Short Answer: **You Are Safe**

Your setup uses a **local LAN IP address (`192.168.1.36`)** — this is a private network address. It is **not reachable from the public internet** at all.

---

## Why This Setup Is Secure

### 1. `192.168.1.x` is a Private IP Address

| IP Range | Type | Internet Accessible? |
|---|---|---|
| `192.168.0.0/16` | Private LAN | ❌ No |
| `10.0.0.0/8` | Private LAN | ❌ No |
| `172.16.0.0/12` | Private LAN | ❌ No |
| `1.x.x.x`, `8.x.x.x` etc. | Public IP | ✅ Yes (exposed) |

`192.168.1.36` is **your home LAN address only**. Internet bots, scanners (like Shodan), and attackers **cannot reach it** because your home router does NAT (Network Address Translation) and blocks unsolicited inbound traffic by default.

---

### 2. SSH Tunnel Binds to `127.0.0.1` (Localhost Only)

Your tunnel command:

```bash
ssh -N -L 18789:127.0.0.1:18789 lzw@192.168.1.36
```

- `127.0.0.1:18789` on the **left side** = the port opens only on **your own machine's localhost**
- Nobody on LAN, nobody on the internet, can connect to port `18789` on your machine — only **you** on that same machine can open `http://localhost:18789`

---

### 3. Traffic is SSH Encrypted

All data between your two home computers travels inside an **SSH encrypted tunnel**. Even on your own LAN, no one can sniff the OpenClaw traffic.

---

## What You Should Still Check

### ✅ Verify Port 18789 is NOT exposed externally

On the OpenClaw server (`192.168.1.36`), run:

```bash
ss -tlnp | grep 18789
```

You should see it bound to `127.0.0.1:18789` — **not** `0.0.0.0:18789`.

If you see `0.0.0.0:18789`, that means it's listening on all interfaces — fix it:

```bash
# Edit OpenClaw config to bind localhost only
openclaw config set server.host 127.0.0.1
openclaw restart
```

---

### ✅ Check your router has no port forwarding to port 18789

Log into your home router (usually `192.168.1.1`) and confirm there is **no port forwarding rule** pointing to `192.168.1.36:18789`. If there is none, you are safe.

---

### ✅ SSH Hardening on `192.168.1.36` (Recommended)

Since you are SSHing into the second computer, good practice:

```bash
# Disable password login, use SSH key only
sudo nano /etc/ssh/sshd_config
```

Set these:

```
PasswordAuthentication no
PermitRootLogin no
PubkeyAuthentication yes
```

Then reload:

```bash
sudo systemctl reload sshd
```

---

### ✅ Check if SSH port (22) is forwarded in router

If you **do** have SSH port 22 forwarded to your home from the internet (for remote access), bots **will** scan your SSH port. Mitigate this:

```bash
# Install fail2ban to auto-ban brute-force attempts
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

Or change SSH to a non-standard port (e.g., 2222).

---

## Summary

| Risk | Your Setup | Verdict |
|---|---|---|
| OpenClaw dashboard exposed to internet | Bound to `127.0.0.1`, LAN IP only | ✅ Safe |
| Port scanned by Shodan/bots | Private `192.168.1.x` not reachable | ✅ Safe |
| LAN users can access dashboard | Only via your SSH tunnel | ✅ Safe |
| SSH brute force (if port 22 forwarded) | Depends on router config | ⚠️ Check router |
| Unencrypted traffic | SSH tunnel encrypts everything | ✅ Safe |

**Your current setup is correctly configured and not exposed to the public internet.** The only thing worth double-checking is your router's port forwarding settings.
