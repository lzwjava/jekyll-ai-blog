---
audio: false
generated: true
image: false
lang: en
layout: post
title: Network Discovery Summary Report
translated: false
type: note
---

NETWORK DISCOVERY SUMMARY
=========================

YOUR NETWORK: 192.168.1.0/24
YOUR IP:      192.168.1.52 (MacBook Air M2, this machine)

DISCOVERY PROCESS
=================

Step 1 - Found your IP
  Command: ipconfig getifaddr en0
  Result:  192.168.1.52

Step 2 - ARP table scan
  Command: arp -a | grep -v "incomplete"
  This lists all devices your Mac has recently communicated with.
  Found 10 active IPs + router + broadcast.

Step 3 - Identify Apple devices by MAC OUI
  Every network card has a MAC address. The first 3 octets (OUI)
  identify the manufacturer. Apple registered OUIs include:
    3C:6A:48, 68:C6:AC, 88:E9:FE, A4:83:E7, DC:A6:32, etc.
  Cross-referenced each discovered MAC against known Apple OUIs.
  Found 3 Apple devices.

Step 4 - Port scanning (nc)
  Scanned common ports on each Apple device:
    22 (SSH), 80 (HTTP), 443 (HTTPS), 5900 (VNC), 5353 (mDNS)
  This helps distinguish Mac vs iPhone vs sleeping device.

Step 5 - Device identification
  192.168.1.18 -> Port 80 open -> curl revealed "TL-XDR3050易展版"
                  This is a TP-Link extender, NOT a Mac. MAC OUI
                  (68:AB:BC) happens to overlap with Apple range
                  in some databases, but the device self-identifies
                  as TP-Link via its web interface.

  192.168.1.20 -> Apple OUI confirmed, no open ports, responds to
                  ARP. Typical behavior of a Mac with default
                  firewall (blocks all incoming by default).

  192.168.1.49 -> Apple OUI confirmed, completely unreachable.
                  Likely asleep or Wi-Fi disconnected.

Step 6 - Elimination
  Known devices: router (.1), TP-Link extender (.18),
                 workstation (.36), this Mac (.52)
  Remaining Apple devices: .20 and .49
  .49 is unreachable -> likely asleep
  .20 is responsive -> most likely the other Mac

RESULTS
=======

  IP              STATUS       DEVICE TYPE         MAC (masked)
  --------------- ------------ ------------------- ------------------
  192.168.1.1     Active       Router (China Tel.) XX:XX:XX:CD:1D:6B
  192.168.1.18    Active       TP-Link Extender    XX:XX:XX:C5:9D:CD
  192.168.1.20    Active       Apple (likely Mac)   XX:XX:XX:53:92:E7
  192.168.1.24    Active       Unknown             XX:XX:XX:24:57:5F
  192.168.1.29    Active       Unknown             XX:XX:XX:F6:5F:XX
  192.168.1.36    Active       Workstation         XX:XX:XX:D9:54:5B
  192.168.1.42    Active       Unknown             XX:XX:XX:D4:CD:34
  192.168.1.49    Unreachable  Apple (likely Mac)   XX:XX:XX:79:8F:31
  192.168.1.52    Active       MacBook Air M2 (you) --hidden--
  192.168.1.53    Active       Unknown             XX:XX:XX:AA:E1:0E
  192.168.1.54    Active       Unknown             XX:XX:XX:A2:3F:9D

VERDICT
=======

  Your other Mac is most likely: 192.168.1.20

  Evidence:

- Apple OUI (manufacturer = Apple Inc.)
- Responsive to ARP (powered on, connected to WiFi)
- No open ports (consistent with macOS default firewall)
- Not a known device (not router, not workstation, not this Mac)

  Alternative: 192.168.1.49 is also Apple but unreachable
  (possibly asleep or using randomized MAC that rotated).
