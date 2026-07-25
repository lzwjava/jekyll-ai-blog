---
audio: false
generated: true
image: false
lang: en
layout: post
title: Discord Update Hang in China
translated: false
type: note
---

**Question: Why does Discord stay on “Checking for updates” and hang in China?**

**Answer:**

The most likely reason is **network access to Discord's update servers is failing or very slow from mainland China**.

Discord desktop startup flow:

```
Discord.exe starts
        |
        v
Check update manifest
        |
        v
Download latest app package
        |
        v
Verify package
        |
        v
Launch Electron app
```

The hang usually happens at step 1 or 2.

Common causes in China:

### 1. Discord update servers are unreachable / unstable

Discord uses:

* `discord.com`
* `cdn.discordapp.com`
* `updates.discord.com`
* Cloudflare CDN

If these endpoints are blocked, throttled, or have poor routing, the updater waits indefinitely.

Test:

```bash
curl -I https://discord.com
curl -I https://updates.discord.com
curl -I https://cdn.discordapp.com
```

If they timeout, this is the reason.

---

### 2. Old Discord cache is corrupted

Electron apps keep update state locally.

Try clearing:

Windows:

```
%AppData%\Discord
%LocalAppData%\Discord
```

Delete:

```
Cache
Code Cache
GPUCache
```

Then restart Discord.

Or completely:

```powershell
taskkill /F /IM Discord.exe

rmdir /s /q "%AppData%\Discord"
rmdir /s /q "%LocalAppData%\Discord"
```

Reinstall.

---

### 3. DNS problem

China ISPs sometimes return bad routes.

Try:

```
1.1.1.1
8.8.8.8
```

DNS:

Windows:

```
Network Settings
 -> IPv4
 -> DNS server
 -> 1.1.1.1
```

Then:

```cmd
ipconfig /flushdns
```

---

### 4. Proxy/VPN mismatch

Discord often works only when **both update and app traffic go through the same route**.

Example:

* System proxy enabled → updater uses proxy
* Discord app does not → login fails

Check:

```
Settings
 -> Network & Internet
 -> Proxy
```

---

### 5. Manual update workaround

Download latest Discord installer from:

[Discord Download](https://discord.com/download?utm_source=chatgpt.com)

Install over existing installation.

---

For China specifically, the fastest debugging path:

```bash
# check DNS
nslookup discord.com

# check HTTPS
curl -v https://discord.com

# check CDN
curl -v https://cdn.discordapp.com
```

If all fail → network routing problem, not your PC.

A lot of China users run Discord through a proxy/VPN because Discord's infrastructure is not reliably reachable from mainland networks.
