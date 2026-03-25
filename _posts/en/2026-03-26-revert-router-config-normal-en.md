---
audio: false
generated: true
image: false
lang: en
layout: post
title: Reverting Router Configuration to Normal Machine
translated: false
type: note
---

Sure, here's the full rundown of what happened:

---

## Session Summary: Reverting 192.168.1.42 from Router to Normal

### Goal
Reset 192.168.1.42 (lzwjava-Lenovo-G490) back to a normal machine after it was configured as a router for an iPad via USB ethernet adapter.

### Step 1: SSH Connection
- Needed `sshpass` since the server (lzw-server) has no ssh-askpass for interactive password input
- Credentials: `lzwjava@192.168.1.42`, password `88888888`
- Had to pipe password to `sudo -S` on the remote side since sudo also needed interactive auth

### Step 2: Discovery (what was still "routerified")
Ran a comprehensive audit across all the config areas you listed. Found:

| Component | Status |
|---|---|
| IP forwarding | **Enabled** — both runtime (`/proc/sys/net/ipv4/ip_forward = 1`) and persistent (`/etc/sysctl.conf`) |
| dnsmasq | **Active** — with `/etc/dnsmasq.d/usb-lan.conf` serving DHCP on `enx00e04c362f89` (192.168.201.50–150) |
| Clash | **Running** — PID 12975, `clash-meta` in TPROXY mode |
| UFW | Already inactive — you'd cleaned this up previously |
| iptables NAT/FORWARD | Appeared empty at discovery time |
| Network interfaces | Main `enp2s0` at 192.168.1.42, USB adapter `enx00e04c362f89` DOWN (no iPad connected) |
| Netplan | Using `renderer: NetworkManager` — left untouched |

### Step 3: Reverting (what I did)
Ran a single remote command with `sudo -S` that performed:

1. **Disabled IP forwarding** — commented out `net.ipv4.ip_forward=1` in `/etc/sysctl.conf`, set runtime to `0`
2. **Stopped & disabled dnsmasq** — `systemctl stop/disable dnsmasq`
3. **Removed USB LAN config** — deleted `/etc/dnsmasq.d/usb-lan.conf`
4. **Killed Clash** — `kill 12975`
5. **Flushed iptables** — `iptables -F`, `iptables -t nat -F`, cleared all chains

All five reported success in the output.

### Step 4: Machine Went Dark
Immediately after, the machine stopped responding:
- SSH connections fail with exit code 255
- Ping shows 100% packet loss to 192.168.1.42
- Multiple retry attempts over ~2 minutes all failed

### What Likely Went Wrong
The **iptables flush** was probably too aggressive. Clash in TPROXY mode hooks into the network stack with rules like:
- `TPROXY` rules to intercept traffic
- `mangle` table rules for packet marking
- Possibly `filter` table INPUT/OUTPUT rules

When I flushed ALL chains (`iptables -F` + `iptables -X`), it may have removed rules that were keeping the main ethernet interface (`enp2s0`) functional. If Clash was acting as the system's DNS resolver (which the config suggests — `no-resolv` in dnsmasq, Clash handling DNS via fake-IP), killing it + flushing iptables together could have left the machine with no DNS and broken routing simultaneously.

Alternatively, the machine may have simply rebooted due to some system reaction, and is still in the boot process.

### What Was Definitely Fixed
- IP forwarding: **off** ✅
- dnsmasq: **stopped + disabled** ✅
- USB LAN DHCP config: **removed** ✅
- Clash: **killed** ✅

### What Still Needs Verification (after machine comes back)
- Main ethernet interface still gets DHCP from the router (192.168.1.1)
- Default route is correct
- No stray iptables rules remain
- NetworkManager is managing `enp2s0` properly
- The `enx00e04c362f89` USB adapter can be ignored or removed from config

### Lesson Learned
Should have been more surgical with iptables — only flush `nat` and `mangle` tables (where Clash TPROXY rules live) instead of nuking everything. The `filter` table's default policies (ACCEPT) should have been fine, but the flush may have had side effects on connection tracking or other kernel networking state.