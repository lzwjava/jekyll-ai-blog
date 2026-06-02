---
audio: false
generated: true
image: false
lang: en
layout: post
title: Clash Proxy DNS Setup Options
translated: false
type: note
---

Question: In the Linux Mint proxy router setup with Clash TUN, do we need to stop the `systemd-resolved` service?

Answer:

## Short Answer: **No, you don't need to stop it — but you have options depending on your goal.**

Your current working setup already proves this: Clash is running, the proxy works, and `systemd-resolved` handles DNS for the laptop itself. The conflict was already solved by setting `dns: enable: false` in Clash config and `port=0` in dnsmasq.

---

## Understanding the Roles in Your Setup

| Component | Role |
|---|---|
| `systemd-resolved` | Handles DNS for the **laptop itself** (port 53 on `127.0.0.53`) |
| `dnsmasq` | Provides **DHCP only** to LAN clients (`port=0` disables its DNS) |
| `Clash TUN` | Intercepts and proxies traffic (including DNS via `dns-hijack: any:53`) |

---

## The Three Approaches

### ✅ Option 1: Keep systemd-resolved (Your Current Setup — Recommended)

This is what you're already doing and it works:

- `systemd-resolved` handles DNS for the **laptop's own processes**
- Clash hijacks DNS from **LAN clients** via TUN (`dns-hijack: any:53`)
- dnsmasq only does DHCP (`port=0`)
- **No conflict, no disruption to the laptop's own connectivity**

**When to choose this:** You still use the laptop normally (browse, SSH, etc.) and need it to resolve DNS for itself.

---

### ⚠️ Option 2: Disable the DNS Stub Listener (Middle Ground)

The DNS stub listener is a lightweight DNS server built into `systemd-resolved` that listens for DNS queries on port 53 at `127.0.0.53`. You can disable just the stub listener without stopping the full service.

Edit `/etc/systemd/resolved.conf`:
```ini
[Resolve]
DNSStubListener=no
```
Then:
```bash
sudo systemctl restart systemd-resolved
sudo ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf
```

This frees port 53 completely while keeping `systemd-resolved`'s caching and upstream forwarding. Useful if you want dnsmasq to also serve DNS to clients.

---

### 🔴 Option 3: Fully Disable systemd-resolved (Router-Only Mode)

You can fully disable it with `sudo systemctl disable systemd-resolved` and `sudo systemctl stop systemd-resolved`, then manually set `/etc/resolv.conf` to a static nameserver like `8.8.8.8`.

```bash
sudo systemctl disable systemd-resolved
sudo systemctl stop systemd-resolved
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```

**When to choose this:** The laptop is a **dedicated headless router** — you don't use it as a desktop, and you want dnsmasq to fully handle all DNS for the LAN.

**Risk:** If Clash or your proxy goes down, the laptop itself loses DNS resolution entirely unless you have a fallback.

---

## Recommendation for Your Case

Since your setup is **already working** with `systemd-resolved` running:

> ✅ **Keep it as-is.** The `port=0` in dnsmasq and `dns: enable: false` in Clash already avoid all conflicts. Stopping `systemd-resolved` is unnecessary and could break DNS on the laptop itself if Clash ever goes down.

The only scenario where you'd want to disable it is if you want dnsmasq to serve **both DHCP and DNS** to LAN clients (e.g., for custom domain filtering or split DNS). In that case, go with **Option 2** (disable stub listener only), not a full stop.

References:

- [How to Avoid Conflicts Between dnsmasq and systemd-resolved – Baeldung](https://www.baeldung.com/linux/dnsmasq-systemd-resolved-conflicts)
- [Install and Configure Dnsmasq on Ubuntu – ComputingForGeeks](https://computingforgeeks.com/install-and-configure-dnsmasq-on-ubuntu/)
- [systemd-resolved – ArchWiki](https://wiki.archlinux.org/title/Systemd-resolved)
