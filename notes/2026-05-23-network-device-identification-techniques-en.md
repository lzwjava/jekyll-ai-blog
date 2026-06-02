---
audio: false
generated: true
image: false
lang: en
layout: post
title: Network Device Identification Techniques
translated: false
type: note
---

```
HOW I IDENTIFIED YOUR NETWORK DEVICES
=======================================

METHOD 1: ARP TABLE
  Command: arp -a
  What it shows: IP → MAC mapping for all devices your Air has talked to.
  The "permanent" flag on .52 = this machine (your Air).
  The "ifscope" = all entries are on en0 (WiFi).

METHOD 2: PING SWEEP
  Command: ping -c 1 -W 1000 <ip> (one at a time, or ww network ip-scan)
  Discovers which IPs are alive vs unreachable.
  Found 13 live hosts out of 254 possible.
  "down" doesn't always mean gone — could be firewall blocking ICMP.

METHOD 3: OUI VENDOR LOOKUP
  The first 3 bytes of a MAC address = manufacturer ID (OUI).
  Used curl to macvendors.com API to identify:
    88:e9:fe → Apple
    68:ab:bc → Xiaomi
    3c:6a:48 → TP-LINK
    68:c6:ac → Intel
    dc:ed:83 → Xiaomi
    4:7c:16  → ASRock (your workstation)

METHOD 4: LOCALLY ADMINISTERED MAC DETECTION
  A MAC is "locally administered" when bit 1 of the first octet is set.
  This means it's NOT a hardware-burned MAC — it's randomized.
  Apple uses this for "Private WiFi Address" (iOS 14+, macOS 12+).
  7 out of 17 devices had locally administered MACs → likely Apple devices.

METHOD 5: TTL ANALYSIS
  TTL 64  → Linux/macOS (router, workstation, MacBook)
  TTL 32  → iPhone/iPad (power-save mode, high jitter)
  TTL 128 → Windows
  .49 had TTL 32 + 95ms latency → phone/tablet, not MacBook.

METHOD 6: LATENCY PATTERN ANALYSIS
  Wired devices (.36):   avg 12ms,  low jitter
  WiFi devices (.1, .49): avg 20-95ms, high jitter
  Power-save devices:    avg 400ms+,  huge jitter (45-1045ms)
  Loopback (.52):        avg 0.6ms (pinging yourself)

METHOD 7: mDNS / BONJOUR
  Tried dns-sd -B _ssh._tcp local. — found nothing.
  Most devices don't advertise services.

WHAT I COULDN'T DO:
  - Router admin page (needs login credentials)
  - Traceroute (hops block ICMP on local LAN)
  - SSH into devices (no credentials)
  - nmap port scan (not installed)

DEVICE IDENTIFICATION SUMMARY:
  .1   = Router (by position + gateway route)
  .36  = Workstation (ARP hostname "myapp.loca" + ASRock OUI)
  .52  = This Air (ARP "permanent" flag + local IP)
  .49  = Apple device (real Apple OUI + TTL 32 = likely phone)
  .14, .33 = Xiaomi (OUI confirmed)
  .18  = TP-LINK (OUI confirmed)
  .20  = Intel (OUI confirmed, likely wired device)
  Rest = Apple private WiFi or unknown
```
