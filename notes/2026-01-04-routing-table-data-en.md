---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Routing Table Structure and Stored Data
translated: false
type: note
---

Question: What does a routing table look like, and what information needs to be stored in a routing table? Specifically, does it include MAC addresses, IP addresses, and information about where to route packets?

Answer:

A **routing table** is a data structure maintained by routers (and IP-enabled hosts) that determines where to forward IP packets based on their destination IP address.

### Typical Appearance of a Routing Table
On most systems, the routing table is displayed using commands like:

- Linux/macOS: `ip route show` or `route -n`
- Windows: `route print`

A sample routing table (from a Linux system) might look like this:

```
default via 192.168.1.1 dev eth0 proto dhcp metric 100
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.100 metric 100
10.0.0.0/24 via 10.0.0.254 dev tun0
172.16.0.0/16 via 192.168.1.50 dev eth0
```

Or in the traditional `netstat -rn` / `route` format:

```
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.1.1     0.0.0.0         UG    100    0        0 eth0
192.168.1.0     0.0.0.0         255.255.255.0   U     100    0        0 eth0
10.0.0.0        10.0.0.254      255.255.255.0   UG    0      0        0 tun0
```

### Key Information Stored in Each Routing Table Entry
Each entry in the routing table typically contains the following fields:

- **Destination network/prefix**: The network or host IP address range this route applies to (e.g., 192.168.1.0/24 or 0.0.0.0/0 for default).
- **Prefix length / Netmask**: Defines the size of the destination network (e.g., /24 or 255.255.255.0).
- **Gateway / Next hop**: The IP address of the next router to forward packets to if the destination is not directly connected. If the gateway is 0.0.0.0 or absent, the network is directly connected.
- **Interface / Output interface**: The local network interface (e.g., eth0, wlan0, tun0) through which the packet should be sent.
- **Metric / Administrative distance**: A value used to prefer one route over another when multiple routes exist for the same destination (lower is better).
- **Protocol / Source**: How the route was learned (static, kernel, DHCP, RIP, OSPF, BGP, etc.).
- **Flags**: Indicators such as U (up/usable), G (gateway), H (host route), D (dynamic), etc.

### Does the Routing Table Contain MAC Addresses?
**No.**
Routing tables operate at **Layer 3 (IP layer)** of the OSI model and do **not** store MAC addresses. MAC addresses are Layer 2 (data link layer) information and are handled separately by the **ARP table** (Address Resolution Protocol cache).

- The routing table decides **which next-hop IP address** or **which interface** to use.
- Once the next-hop IP is determined, if the packet must be sent over a local link (Ethernet, Wi-Fi, etc.), the system consults the **ARP table** to resolve the next-hop IP to a MAC address for framing the Ethernet packet.

### Does the Routing Table Contain IP Addresses?
**Yes.**
- Destination network (IP prefix)
- Next-hop IP address (gateway)
- Sometimes the source IP used for the interface

### Does It Tell "Which Packet to Route Where"?
**Yes.**
The primary purpose of the routing table is exactly that: for a given destination IP address in a packet, perform a **longest-prefix match** against the destination entries to decide:
- Whether to forward the packet to a specific next-hop router (gateway IP), or
- Send it directly out a local interface (if the destination is on a directly connected network).

In summary:

| Information                  | Present in Routing Table? | Notes |
|------------------------------|---------------------------|-------|
| Destination IP network/prefix| Yes                       | Core field |
| Netmask / Prefix length      | Yes                       | Defines network size |
| Next-hop / Gateway IP        | Yes (if not directly connected) | IP address of next router |
| Output interface             | Yes                       | Local interface to use |
| Metric / Priority            | Yes                       | For route selection |
| MAC addresses                | No                        | Handled by ARP table (Layer 2) |
| Source IP (sometimes)        | Yes                       | For policy-based routing or interface assignment |

References:

- [Cisco: Understanding Routing Tables](https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/13762-40.html)
- [Linux ip-route man page](https://man7.org/linux/man-pages/man8/ip-route.8.html)
- [Microsoft: Route Command Reference](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/route_ws2008)
