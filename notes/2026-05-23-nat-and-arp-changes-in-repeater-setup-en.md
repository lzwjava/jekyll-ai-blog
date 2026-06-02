---
audio: false
generated: true
image: false
lang: en
layout: post
title: NAT and ARP Changes in Repeater Setup
translated: false
type: note
---

```
NETWORK TOPOLOGY — AFTER ROUTER A CONNECTED
=============================================

BEFORE (single router):
  Internet → Router B (China Telecom Gateway, .1) → all devices

NOW (repeater setup):
  Internet → Router A (TP-LINK, .37) ~wireless repeater~ Router B (.1) → devices
                ↓                                            ↓
          Devices behind A                             Devices on B's WiFi

WHAT CHANGED IN ARP TABLE:

  .37 appeared — Router A (TP-LINK)
    MAC: locally administered, "permanent" flag
    Latency: 2ms (very close — it's the router itself)

  .36, .18, .19, .20 now share the SAME MAC address
    → These devices are behind Router A, NAT'd through it
    → Router A rewrites their MACs to its own

  .14, .21, .24, .26, .31, .50, .54 kept their original MACs
    → Still connected directly to Router B's WiFi

DEVICE CLASSIFICATION:

  BEHIND ROUTER A (TP-LINK, NAT'd):
    .36  Workstation (ASRock, wired to Router A)
    .18  TP-LINK device (IoT/smart home?)
    .19  unknown
    .20  Intel device

  ON ROUTER B (China Telecom, direct):
    .1   Router B itself
    .14  Xiaomi
    .21  Apple private WiFi
    .24  Apple private WiFi
    .26  unknown (50:8b:b9)
    .31  Apple private WiFi
    .50  unknown (34:55:06)
    .54  Apple private WiFi

  DISAPPEARED (were on B, now gone):
    .42, .49, .52, .53 — phones/tablets went to sleep
    .52 was your Air, but now shows as .37's network

  NOTE: Your Air (.52) is connected to Router B's WiFi
        but ARP shows it talking through Router A's MAC
        → Air is on Router B's side, not behind Router A
```

The repeater creates two logical zones. Devices behind Router A get NAT'd (same MAC in ARP). Devices on Router B keep their real MACs. Your workstation (.36) is wired to Router A — that's why it appears NAT'd.
