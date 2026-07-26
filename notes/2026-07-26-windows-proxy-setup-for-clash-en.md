---
audio: false
generated: true
image: false
lang: en
layout: post
title: Windows Proxy Setup for Clash
translated: false
type: note
---

Question: **How to set Windows system proxy to use your Mihomo/Clash config (`mixed-port: 7892`)?**

Answer:

Your Mihomo config exposes:

```yaml
port: 7890          # HTTP proxy
socks-port: 7891    # SOCKS5 proxy
mixed-port: 7892    # HTTP + SOCKS combined
allow-lan: true
```

For **Windows system proxy**, use the **HTTP proxy port** or **mixed port**.

## Option 1: Windows GUI

1. Open:

```
Settings
→ Network & Internet
→ Proxy
```

2. Under **Manual proxy setup**:

Enable:

```
Use a proxy server: On
```

Set:

```
Address: 127.0.0.1
Port:    7892
```

Example:

```
http://127.0.0.1:7892
```

Save.

---

## Option 2: PowerShell (fast)

Run as normal user:

```powershell
netsh winhttp set proxy 127.0.0.1:7892
```

Check:

```powershell
netsh winhttp show proxy
```

Reset:

```powershell
netsh winhttp reset proxy
```

---

## Option 3: Environment proxy (for CLI tools)

Many developer tools use environment variables:

PowerShell:

```powershell
$env:HTTP_PROXY="http://127.0.0.1:7892"
$env:HTTPS_PROXY="http://127.0.0.1:7892"
```

Permanent:

```powershell
[Environment]::SetEnvironmentVariable(
  "HTTP_PROXY",
  "http://127.0.0.1:7892",
  "User"
)

[Environment]::SetEnvironmentVariable(
  "HTTPS_PROXY",
  "http://127.0.0.1:7892",
  "User"
)
```

---

## Verify

Open PowerShell:

```powershell
curl https://www.google.com
```

or:

```powershell
curl https://api.ipify.org
```

You should see the proxy exit IP.

---

## Important: `allow-lan`

Your config:

```yaml
allow-lan: true
```

means other devices can access Mihomo, but for the **same Windows machine** you only need:

```
127.0.0.1:7892
```

No firewall changes needed.

---

## If Mihomo runs on another machine (Mac)

Your prompt shows:

```
lzwjava@lzw-mac
```

If Mihomo is running on your Mac and Windows connects to it:

1. Find Mac IP:

```bash
ifconfig en0 | grep inet
```

Example:

```
192.168.1.100
```

2. Windows proxy:

```
Address: 192.168.1.100
Port: 7892
```

3. Ensure Mac firewall allows port 7892.

Your current:

```yaml
allow-lan: true
```

is already correct for this scenario.
