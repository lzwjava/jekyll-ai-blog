---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing SSH After Port Change Lockout
translated: false
type: note
---

Question:
How can I fix my server after changing the SSH port from 2222 to 22 and now I can’t connect?

Answer:

You likely locked yourself out due to a mismatch between **SSH configuration**, **firewall rules**, or **port availability**. Let’s walk through the fastest recovery path.

---

# 🚨 Most Likely Causes

When you changed from `2222 → 22`, one of these happened:

1. **Port 22 is blocked by firewall**
2. **SSH service failed to restart**
3. **Another service already uses port 22**
4. **Cloud provider / router not allowing port 22**
5. **You edited the wrong config or made a syntax error**

---

# 🛠️ How to Recover (Step-by-step)

## ✅ 1. Use Console Access (IMPORTANT)

You cannot fix this over SSH anymore.

Use one of these:

* VPS provider console (AWS / GCP / DigitalOcean / etc.)
* Physical machine terminal
* Hypervisor console (VMware / Proxmox / VirtualBox)

---

## ✅ 2. Check SSH status

```bash
sudo systemctl status ssh
```

If it failed, restart:

```bash
sudo systemctl restart ssh
```

If restart fails → config error.

---

## ✅ 3. Verify SSH config

Open:

```bash
sudo nano /etc/ssh/sshd_config
```

Check this line:

```bash
Port 22
```

⚠️ Also check:

* No duplicate `Port` lines
* No syntax errors

Then test config:

```bash
sudo sshd -t
```

If no output → config is valid.

---

## ✅ 4. Check if port 22 is actually listening

```bash
sudo ss -tlnp | grep :22
```

If nothing shows → SSH is NOT running on port 22.

---

## ✅ 5. Check firewall (VERY COMMON ISSUE)

### If using UFW

```bash
sudo ufw status
```

If port 22 is not allowed:

```bash
sudo ufw allow 22/tcp
sudo ufw reload
```

---

### If using iptables

```bash
sudo iptables -L -n
```

Make sure port 22 is allowed.

---

## ✅ 6. Check if port 22 is already occupied

```bash
sudo lsof -i :22
```

If something else is using it (e.g. another SSH instance or service):

* Either stop that service
* Or revert to port 2222

---

## ✅ 7. Quick Recovery (Safest Option)

If you're stuck, just revert to old working port:

```bash
sudo nano /etc/ssh/sshd_config
```

Change back:

```bash
Port 2222
```

Then:

```bash
sudo systemctl restart ssh
```

---

## ✅ 8. Verify before disconnecting next time

Before closing your current session:

```bash
ssh -p 22 user@your_ip
```

Always test new port in a **second terminal**.

---

# 🧠 Pro Tips (Important)

* Always keep **at least one active SSH session** when changing ports
* Open firewall BEFORE switching port
* You can run multiple ports:

```bash
Port 22
Port 2222
```

This avoids lockout entirely.

---

# 🔥 Your Situation (Most Likely Diagnosis)

Based on your description:

👉 90% chance: **Firewall still allows 2222 but blocks 22**

So SSH is running, but you cannot reach it.

---

# ✅ Fastest Fix Summary

From console:

```bash
sudo ufw allow 22/tcp
sudo systemctl restart ssh
```

OR revert:

```bash
Port 2222
```

---

If you tell me:

* your OS (Ubuntu / CentOS / etc.)
* where it's hosted (local / VPS)

I can give you a **precise 1-command fix**.
