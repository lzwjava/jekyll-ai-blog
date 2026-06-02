---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Geolocation Behind a Proxy
translated: false
type: note
---

Here's the full story:

**Problem:** `ww weather` used `wttr.in` which auto-detects location via IP. But your traffic routes through a hysteria2 proxy server in Los Angeles, so it showed LA weather instead of Guangzhou.

**Attempt 1 — macOS CoreLocation (GPS):**
- Wrote a Swift script using `CoreLocation` framework to get real GPS coordinates
- Failed: macOS Sequoia requires Location Services permission for Terminal, which needs a GUI prompt in System Settings. The request just timed out.

**Attempt 2 — WiFi BSSID geolocation:**
- Tried to get your WiFi router's BSSID (MAC address) via CoreWLAN, `system_profiler`, `ioreg`, and the old `airport` CLI
- Failed on all fronts: macOS Sequoia redacts SSID/BSSID for privacy. `ioreg` shows `<SSID Redacted>` and BSSID as `000000000000`. Even compiled Swift binaries hit the same wall — the OS blocks it at the kernel level without Location Services consent.

**Attempt 3 — Router admin page (192.168.1.1):**
- Your router runs OpenWrt/LuCI at 192.168.1.1
- Hit the LuCI web page successfully, but the API endpoints (`/cgi-bin/luci/api/status`, `/cgi-bin/luci/api/network/wireless`) aren't registered — no programmatic access to WAN IP or WiFi info without authentication

**Attempt 4 — Bypass proxy for IP geolocation (the winner):**
- Key insight: `curl --noproxy '*'` or Python's `urllib.ProxyHandler({})` bypasses the hysteria2 proxy and hits the internet directly from your real IP (ChinaNet backbone, 14.19.30.x)
- Tested three geolocation services:
  - `ipinfo.io` → Shenzhen (22.54, 114.06) — wrong city, ~100km off
  - `ip-api.com` → **Guangzhou** (23.12, 113.25) — correct! Close to Zengcheng
  - `ipapi.co` → returned nulls (rate limited)
- Winner: `ip-api.com` — more accurate for Chinese ISP IPs, correctly identifies Guangzhou

**What `--detail` shows and where each piece comes from:**
- **City**: `ip-api.com` geolocation via your real (non-proxy) WAN IP
- **ISP**: `ip-api.com` — "Chinanet (Chinanet GD)" = ChinaNet Guangdong backbone
- **Local IP**: `ipconfig getifaddr en0` — your LAN address on the router
- **Gateway**: `netstat -rn` parsing the default route — your router at 192.168.1.1
- **WiFi channel/PHY**: `system_profiler SPAirPortDataType` — this data isn't redacted, only SSID/BSSID are
- **Signal strength**: same `system_profiler` output — RSSI -49 dBm is good signal

**Why Zengcheng shows as "Guangzhou":** Zengcheng (增城) is a district of Guangzhou prefecture. IP geolocation resolves to the city level, not district. The coordinates from `ip-api.com` (23.12, 113.25) are actually very close to Zengcheng's center. Weather-wise it's the same — within 30km.
