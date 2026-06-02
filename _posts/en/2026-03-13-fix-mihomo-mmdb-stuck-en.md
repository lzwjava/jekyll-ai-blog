---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Mihomo MMDB Download Stuck
translated: false
type: note
---

Question: Why does mihomo get stuck at "Can't find MMDB, start download" during startup?

Answer:

## Why Mihomo Gets Stuck at MMDB Download

When you see this log sequence:

```
INFO Can't find MMDB, start download
```

...and it just **hangs there**, it means mihomo is trying to download the **GeoIP MMDB database** (MaxMind DB format, used for IP geolocation rules) but the download is **stalling or failing silently**.

---

## Root Causes

### 1. **Network / Connectivity Issue (Most Common)**

Mihomo is trying to reach a remote URL (usually hosted on GitHub or jsDelivr CDN) to download `Country.mmdb` or `geoip.metadb`. If your machine:

- Has no internet access yet at startup time
- Is behind a firewall/proxy that blocks GitHub raw file downloads
- Is in a region where GitHub CDN is slow or unreliable

...the download just hangs without a timeout error message.

### 2. **Default Download URL is Blocked**

The default MMDB source URL often points to GitHub releases, which is frequently throttled or blocked in China and some other regions.

### 3. **No Pre-existing MMDB File**

If there's no cached MMDB file in mihomo's working/config directory, it **must** download one before it can proceed. There's no fallback.

---

## How to Fix

### ✅ Fix 1: Manually Download and Place the MMDB File

Download the file manually and place it in mihomo's config directory (e.g. `~/.config/mihomo/` or wherever your `config.yaml` lives):

```bash
wget -O ~/.config/mihomo/Country.mmdb \
  https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/country.mmdb
```

Then restart mihomo. It will find the file and skip the download step.

---

### ✅ Fix 2: Set a Custom (Faster) MMDB Download URL in `config.yaml`

Add the `geox-url` section to point to a more accessible mirror:

```yaml
geox-url:
  mmdb: "https://fastly.jsdelivr.net/gh/MetaCubeX/meta-rules-dat@release/country.mmdb"
  geoip: "https://fastly.jsdelivr.net/gh/MetaCubeX/meta-rules-dat@release/geoip.dat"
  geosite: "https://fastly.jsdelivr.net/gh/MetaCubeX/meta-rules-dat@release/geosite.dat"
```

Or use an alternative mirror like:

```yaml
mmdb: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/release/country.mmdb"
```

---

### ✅ Fix 3: Switch to `.dat` format (skip MMDB entirely)

If you don't need MMDB specifically, switch to `geodata-mode: true` which uses `.dat` files instead:

```yaml
geodata-mode: true
```

This makes mihomo use `geoip.dat` and `geosite.dat` instead of the MMDB format, which may be easier to source.

---

### ✅ Fix 4: Pre-download at System Level

If you are running mihomo as a system service (e.g. on a router or Linux server), the service may start before networking is fully up. Add a startup delay or `After=network-online.target` in your systemd unit:

```ini
[Unit]
After=network-online.target
Wants=network-online.target
```

---

## Summary Table

| Cause | Fix |
|---|---|
| No internet / network not ready | Wait, or fix startup order |
| GitHub CDN blocked/slow | Use jsDelivr or alternate mirror URL |
| No cached MMDB file | Manually pre-download the file |
| Want to avoid MMDB entirely | Use `geodata-mode: true` |

References:

- [mihomo Issue #931 – MMDB update failure](https://github.com/MetaCubeX/mihomo/issues/931)
- [mihomo General Configuration Docs](https://wiki.metacubex.one/en/config/general/)
- [mihomo Issue #1083 – GeoIP MMDB problems](https://github.com/MetaCubeX/mihomo/issues/1083)
