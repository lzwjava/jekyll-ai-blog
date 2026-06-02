---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Clash Hysteria2 Error Guide
translated: false
type: note
---

**Question:** How to fix the error "FATA[0000] Parse config error: proxy 1: unsupport proxy type: hysteria2" when running ./clash-darwin-amd64?

**Answer:**

This error occurs because the `hysteria2` (hy2) proxy type is **not supported** by the standard Clash core or older Clash Premium builds. Your current binary (`clash-darwin-amd64`) is most likely a classic Clash or an old Clash Premium version that only knows older proxy types (ss, vmess, trojan, snell, etc.).

Hysteria2 support was added in the **Clash Meta** (mihomo) core starting around version 1.16+ (late 2023 / early 2024), and it is now very well supported in 2025–2026 builds.

### Quick Fix Options (Mac)

1. **Recommended: Switch to mihomo (Clash Meta core)**
   Download a recent macOS AMD64 binary from the official MetaCubeX/mihomo releases:

   - Go to → <https://github.com/MetaCubeX/mihomo/releases>
   - Find the latest version (e.g. v1.18.x or newer in 2026)
   - Download the file named roughly: `mihomo-darwin-amd64` or `mihomo-alpha-darwin-amd64` or `clash.meta-darwin-amd64`
   - Rename it to `clash` or `mihomo` if you want
   - `chmod +x` the file
   - Replace your old `./clash-darwin-amd64` with this new binary
   - Run it again → `./mihomo-darwin-amd64 -d .` (or however you normally start it)

   Most modern Clash GUI clients on macOS (Clash Verge Rev, Mihomo Party, FlClash, etc.) already bundle recent mihomo cores and support hysteria2 out of the box.

2. **Alternative: Use a modern GUI client instead of command-line binary**
   Popular choices in 2025–2026 for macOS:

   - **Clash Verge Rev** → <https://github.com/clash-verge-rev/clash-verge-rev/releases>
     (very actively maintained, excellent hysteria2 / TUIC / VLESS Reality support)

   - **Mihomo Party** → <https://github.com/pompurin404/mihomo-party>
     (very user-friendly, built specifically around mihomo)

   - **FlClash** → <https://github.com/chen08209/FlClash>

   These clients handle config parsing, core updates, and hy2 nodes automatically.

3. **If you must keep using command-line only**
   - Download mihomo binary (as in option 1)
   - Or compile from source: <https://github.com/MetaCubeX/mihomo>
     (go install github.com/MetaCubeX/mihomo@alpha)

### Summary Table

| Current binary          | Supports hysteria2? | Recommendation                  |
|-------------------------|----------------------|----------------------------------|
| Classic Clash           | No                  | Switch to mihomo                |
| Old Clash Premium       | No                  | Switch to mihomo                |
| Recent mihomo / Clash Meta | Yes              | Use this (download latest)      |
| Clash Verge Rev / Mihomo Party | Yes           | Easiest & most convenient       |

After replacing the binary with a mihomo version, the `type: hysteria2` nodes in your config should parse and work normally.

**References:**

- <https://github.com/MetaCubeX/mihomo/releases>
- <https://github.com/clash-verge-rev/clash-verge-rev/releases>
- <https://wiki.metacubex.one/en/> (mihomo documentation)
