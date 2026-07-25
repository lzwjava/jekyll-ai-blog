---
audio: false
generated: true
image: false
lang: en
layout: post
title: Discord Update Hang Analysis Review
translated: false
type: note
---

I've reviewed the Discord hang analysis you shared. It's thorough and technically accurate. Here's my assessment:

## Review of Your Discord "Checking for Updates" Analysis

### ✅ Spot On

1. **Update server unreachability** — Your analysis of the startup flow (check manifest → download → verify → launch) is correct. Discord uses `updates.discord.com` and Squirrel (Windows) / Electron auto-updater, and these **are** often blocked or degraded from mainland China. The `curl` diagnostic commands you gave are the right first step.

2. **Cache corruption** — Electron's local update state (`%AppData%/Discord`, `%LocalAppData%/Discord`) is a common cause of persistent hang loops. The `rmdir` + reinstall approach is the nuclear but reliable fix.

3. **DNS routing** — China ISPs (China Telecom, Unicom, Mobile) frequently return suboptimal routes to Cloudflare IPs. Your `1.1.1.1` / `8.8.8.8` suggestion is good, though note `8.8.8.8` itself can have elevated latency from China. `1.1.1.1` via Cloudflare's China partnership with Baidu is often more reliable.

4. **Proxy/VPN mismatch** — Critical point: Squirrel updater inherits system proxy settings, but Discord's Electron app uses its own Chromium networking stack which may not. This split-brain scenario is extremely common.

### 🔍 Nuances / Additions

| Point | Your Analysis | My Additions |
|-------|--------------|--------------|
| **TLS fingerprinting** | Not mentioned | China's DPI (Deep Packet Inspection) can detect and block Discord's TLS handshake even over Cloudflare IPs. A simple curl check might show connectivity, but the full update download may still fail due to SNI-based blocking. |
| **Squirrel update protocol** | Good overview | Discord uses Squirrel (Windows) / Squirrel.Mac. It checks `RELEASES` file first, then downloads individual `.nupkg` packages. If the `RELEASES` file download fails or returns a stale response, the update hangs silently. |
| **`Hosts` file interference** | Not mentioned | Users often add Discord IPs to `/etc/hosts` or `C:\Windows\System32\drivers\etc\hosts` for VPN split-tunneling. A stale host entry pointing to an old IP can cause the updater to hang. |
| **Windows Update / Background Intelligent Transfer Service (BITS)** | Not mentioned | Squirrel can use BITS for background downloads. If BITS is disabled or corrupted, updates hang. `net start bits && sc query bits` verifies this. |
| **macOS variant** | Windows-focused | On macOS, Discord stores updates in `~/Library/Application Support/discord/`. The `.dmg`-based updater is slightly different but same principles apply. |

### 💡 Bonus Diagnostic for Your Toolbox

```bash
# Check if Discord's domains resolve to blocked/reserved IPs
for domain in discord.com updates.discord.com cdn.discordapp.com; do
  echo "=== $domain ==="
  nslookup $domain 2>&1 | tail -3
  curl -sI "https://$domain" -o /dev/null -w "HTTP %{http_code}, Time: %{time_total}s\n" --connect-timeout 5
done

# Check for split-tunnel proxy routing
curl -s --proxy http://127.0.0.1:7890 https://discord.com -o /dev/null -w "Via proxy: %{http_code}\n"
curl -s --noproxy '*' https://discord.com -o /dev/null -w "Direct: %{http_code}\n"
```

### 🔗 Relevance to This Project

Your analysis aligns well with existing tools in `ww`:

| Existing ww tool | What it covers |
|---|---|
| `ww network ip-scan / port-scan` | Network diagnostics layer |
| `ww clash query-dns` | DNS resolution checks |
| `ww macos settings-proxy / linux proxy-setup` | Proxy configuration |
| `ww utils request-proxy` | Proxy-aware HTTP requests |
| `ww.try.solve` | General problem-solving methodology |

If you wanted, this Discord-specific diagnostic flow could be added as a new command (e.g., `ww try discord-diagnose`) leveraging the existing `ww/network/` and proxy utilities. Want me to draft that?
