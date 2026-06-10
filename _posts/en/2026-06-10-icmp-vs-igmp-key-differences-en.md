---
audio: false
generated: true
image: false
lang: en
layout: post
title: "ICMP vs IGMP: Key Differences"
translated: false
type: note
---

**Question:** What's the difference between ICMP and IGMP?

**Answer:**

They sound similar but solve completely different problems. Both sit directly on top of IP (no TCP/UDP), but that's where the similarity ends.

**ICMP (protocol number 1)** — error reporting and diagnostics for IP itself. When something goes wrong delivering a packet (TTL expired, host unreachable, fragmentation needed), routers/hosts send ICMP messages back to the source. It's the feedback channel IP lacks, since IP is fire-and-forget.

Key message types:

- Type 8/0 — Echo Request/Reply (`ping`)
- Type 11 — Time Exceeded (what `traceroute` exploits: send packets with TTL=1,2,3... and collect Type 11s from each hop)
- Type 3 — Destination Unreachable (code 4, "fragmentation needed but DF set," drives Path MTU Discovery)
- Type 5 — Redirect

**IGMP (protocol number 2)** — multicast group membership management, used only on the local subnet between hosts and their first-hop router. A host says "I want to receive traffic for 239.1.1.1" via an IGMP Membership Report; the router periodically sends Queries to learn which groups still have listeners, so it knows whether to forward multicast traffic onto that segment. Without IGMP, routers would have to flood all multicast everywhere.

Versions: IGMPv2 (join/leave), IGMPv3 (source-specific multicast — "I want group G but only from source S", needed for SSM). IPv6 dropped IGMP entirely; the equivalent is MLD, which is implemented *as ICMPv6 messages* — which tells you the two protocols are siblings, not the same thing.

Quick comparison:

| | ICMP | IGMP |
|---|---|---|
| IP proto # | 1 | 2 |
| Purpose | error reporting, diagnostics | multicast group membership |
| Scope | end-to-end (any hop can generate) | link-local only (TTL=1) |
| Users | ping, traceroute, PMTUD | IPTV, mDNS-adjacent stacks, routing protocols using multicast (OSPF's 224.0.0.5) |
| IPv6 equivalent | ICMPv6 | MLD (subsumed into ICMPv6) |

Hands-on with scapy to make it concrete:

```python
from scapy.all import *

# ICMP echo request (ping)
ans = sr1(IP(dst="1.1.1.1")/ICMP(type=8), timeout=2)
ans.show()  # type=0 echo-reply

# Craft an IGMPv2 membership report (join 239.1.1.1)
load_contrib("igmp")
pkt = IP(dst="239.1.1.1", ttl=1)/IGMP(type=0x16, gaddr="239.1.1.1")
send(pkt)

# Watch real IGMP on your LAN (router queries every ~125s)
# sniff(filter="igmp", prn=lambda p: p.summary())
```

And the kernel does IGMP for you automatically when you join a multicast group via socket API:

```python
import socket, struct
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
             struct.pack("4s4s", socket.inet_aton("239.1.1.1"),
                                 socket.inet_aton("0.0.0.0")))
# ^ this single setsockopt triggers the kernel to emit an IGMP Membership Report
```

Run `tcpdump -i en0 igmp` while executing that and you'll see the report go out — good 5-minute experiment.

Mental model: **ICMP is IP's error/control plane; IGMP is multicast's signaling plane.** One reports failures, the other declares interest.
