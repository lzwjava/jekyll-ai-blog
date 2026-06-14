---
audio: false
generated: true
image: false
lang: en
layout: post
title: Diagnosing Tailscale SSH Direct Connection
translated: false
type: note
---

## Diagnostic Flow — Tailscale SSH Slowness

**1. SSH config inspection**

```bash
cat ~/.ssh/config
```

Found `lzw-to` with `ProxyCommand none` and catch-all `Host !192.168.*.*` routing through SOCKS5 proxy.

**2. Tailscale status + relay info**

```bash
ssh lzw@<TAILSCALE_IP> "tailscale status"
```

Showed Mac connected via `relay "sin"` (Singapore).

**3. Tailscale ping + netcheck on `to`**

```bash
ssh lzw@<TAILSCALE_IP> "tailscale ping -c 3 --until-direct <TAILSCALE_IP_MAC>"
ssh lzw@<TAILSCALE_IP> "tailscale netcheck"
```

Key findings: `direct connection not established`, DERP(sin) 324–914ms, nearest DERP LAX 163ms, no IPv6, `PortMapping:` empty.

**4. Mac-side Tailscale netcheck**

```bash
tailscale netcheck
```

Found: `Nearest DERP: Singapore (54ms)`, `PortMapping: UPnP`, public IP `<IP_ADDRESS>`.

**5. Reachability tests**

```bash
ping <IP_ADDRESS>                    # to's public IP — 100% loss (NAT blocks ICMP)
ssh dmit "ping -c 3 <IP_ADDRESS>"   # from DMIT — also 100% loss
```

**6. NAT type + endpoint discovery**

```bash
ssh lzw@<TAILSCALE_IP> "tailscale status --json" | python3 -c "..."
```

Parsed JSON for `RelayName`, `CurAddr`, `Endpoints`, `NATType`.

**7. Daemon logs + STUN test**

```bash
ssh lzw@<TAILSCALE_IP> "journalctl -u tailscaled -n 10"
ssh lzw@<TAILSCALE_IP> "nc -u -z -v stun.l.google.com 19302"
ssh lzw@<TAILSCALE_IP> "tailscale debug prefs"
```

STUN works, endpoints discovered (`<IP_ADDRESS>:<PORT>`), cone NAT confirmed.

**8. Force direct connection**

```bash
tailscale ping --until-direct -c 5 <TAILSCALE_IP>
```

Broke through to direct: `via <IP_ADDRESS>:<PORT> in 76ms`.

**9. Verify SSH improvement**

```bash
time ssh lzw-to "echo connected; hostname; uptime"
```

5–6s → 1.9s.

---

All commands run through plain `terminal()` tool — SSH to remote machines, local `tailscale` CLI, `ping`, `nc`, `journalctl`, and Python JSON parsing of `tailscale status --json`.
