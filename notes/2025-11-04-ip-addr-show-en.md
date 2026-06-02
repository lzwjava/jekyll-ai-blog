---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Understanding ip addr show enp4s0 Output
translated: false
type: note
---

### Breaking Down Your `ip addr show enp4s0` Output

This command shows detailed info on your Ethernet interface (enp4s0), which is the one handling your local LAN connection from the routing table we discussed. It's up and running smoothly—great for basic connectivity. I'll parse it line by line, then summarize.

#### Key Sections Explained
- **Interface Status**:
  `2: enp4s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000`
  - Index 2 (second interface, after lo).
  - Flags: Supports broadcast/multicast, fully UP (link detected and operational).
  - MTU: 1500 bytes (standard Ethernet frame size—no jumbo frames).
  - Queue discipline: fq_codel (fair queuing for low-latency traffic, common on modern Linux).
  - State: UP (ready to send/receive).

- **Link Layer (MAC Address)**:
  `link/ether 04:7c:16:d9:54:5b brd ff:ff:ff:ff:ff:ff`
  - Your hardware MAC: 04:7c:16:d9:54:5b (unique to this NIC).
  - Broadcast: ff:ff:ff:ff:ff:ff (all-ones for Ethernet broadcasts).

- **IPv4 Address**:
  `inet 192.168.1.35/24 brd 192.168.1.255 scope global dynamic noprefixroute enp4s0`
  `valid_lft 4790sec preferred_lft 4790sec`
  - IP: 192.168.1.35 with /24 subnet (255.255.255.0 mask). Matches the "src 192.168.1.35" in your route table.
  - Broadcast: 192.168.1.255 (for subnet-wide broadcasts).
  - Scope: global (routable beyond this host).
  - Dynamic: Assigned via DHCP (from your router at 192.168.1.1).
  - No prefix route: Doesn't auto-add a connected route (but kernel did anyway, as seen in `ip route`).
  - Lease: ~79 minutes left (4790 seconds) before renewal.

- **IPv6 Address**:
  `inet6 fe80::a884:a0f6:e8b4:4a7d/64 scope link noprefixroute`
  `valid_lft forever preferred_lft forever`
  - Link-local IPv6: fe80::... (auto-generated from MAC; only for local link communication, like neighbor discovery).
  - /64 prefix, scope link (not routable off this interface).
  - Permanent (no expiration).

#### Quick Summary Table
| Aspect       | Value/Details                  | What It Means |
|--------------|--------------------------------|---------------|
| **Status**  | UP, MTU 1500                  | Interface is active and handling standard packets. |
| **MAC**     | 04:7c:16:d9:54:5b             | Your device's hardware address on the wire. |
| **IPv4**    | 192.168.1.35/24 (DHCP)        | Local LAN IP; routes to this subnet stay on enp4s0. |
| **IPv6**    | fe80::a884:a0f6:e8b4:4a7d/64  | Local-only IPv6; useful for IPv6 neighbor stuff. |
| **Lease**   | ~79 min left                  | DHCP will refresh soon—check with `dhclient -r enp4s0 && dhclient enp4s0` if needed. |

This setup explains why your default route points here for internet access and why local 192.168.1.x traffic is direct. If you're pinging within the LAN, it'll ARP for the MAC and send frames out this interface.

Everything look good, or is there an issue (e.g., no IPv6 global address, or connectivity drops)? If you share `ip addr` for other interfaces or `ping` results, I can dig deeper. What's next—testing Docker bridges, or something else?
