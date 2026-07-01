---
audio: false
generated: true
image: false
lang: en
layout: post
title: MacOS Security Assessment Summary
translated: false
type: note
---

Here's my full security assessment of this macOS machine:

## Login Activity Summary

**Only one user has logged in: `lzwjava`** (plus the system `root` account, which is normal).

| When | User | Terminal | Notes |
| ------ | ------ | ---------- | ------- |
| Sun Apr 12 22:36 (tonight) | lzwjava | ttys010 | Still logged in (this AI agent) |
| Sun Apr 12 22:32 (tonight) | lzwjava | ttys001 | Still logged in (terminal) |
| Sat Apr 11 22:31 | lzwjava | ttys009 | Still logged in |
| Sat Apr 11 05:55 | lzwjava | ttys007 | Still logged in |
| Fri Apr 10 21:45 (boot time) | lzwjava | console + 4 ttys | Still logged in |

The machine rebooted **Friday Apr 10 at 21:41**, which explains why many sessions say "still logged in" -- they're just stale entries from the pre-reboot session. The last `root` login was at console for 1 minute before shutdown. No suspicious remote (SSH) logins anywhere in the log.

## Security Assessment: LOW RISK

**No obvious signs of compromise**, but here's what I found:

### What looks normal

- Only one user account (`lzwjava`) with actual logins -- no unknown users
- No failed login attempts recorded
- No SSH login attempts at all (good if you don't use SSH)
- Three admin accounts exist: `root`, `macadmin`, `lzwjava` -- `macadmin` is a standard macOS admin group account
- No SSH authorized_keys files found (no unauthorized SSH key access)
- No cron jobs
- Running processes are all recognizable apps

### Things worth noting (not necessarily bad)

1. **Proxy/VPN tools**: ClashX Pro, ShadowsocksX-NG, and V2RayU are installed. These are common in China for GFW-bypass, but open listening ports that could theoretically be misconfigured
2. **nginx on port 8081**: Running as user lzwjava -- check if you intentionally set this up
3. **Redis on port 6379**: Bound to localhost only, so not externally accessible
4. **PostgreSQL on port 5432**: Bound to localhost only, same as Redis
5. **WeChat** listening on multiple localhost ports -- normal behavior
6. **mihomo** (clash-based proxy) running as active process (PID 92432)
7. **Multipass** (Canonical VM tool) and **Docker** daemon helpers are installed

### Recommendations if you're concerned

1. Run `sudo log show --predicate 'eventMessage contains "authentication"' --last 24h` in a local terminal to see all authentication events
2. Check if port 8081 (nginx) is intentional -- if not, stop it with `brew services stop nginx`
3. Make sure Firewall is enabled: `sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate`
4. Change your password if you have any doubt: System Preferences > Users & Groups
