---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Understanding IPv4 Routing Table Output
translated: false
type: note
---

### Understanding Your `ip route` Output

This is the IPv4 routing table from your Linux system (likely using the `ip` command from iproute2). It shows how your machine decides where to send packets based on destination IPs. Routes are matched by longest prefix (most specific first), and the default route catches everything else.

I'll break it down entry by entry in a table for clarity, then summarize what it means overall. This ties back to our earlier chat: it's a real-world example of a simple routing table with connected routes (local subnets) and a default gateway for the internet.

| Destination       | Gateway (Next Hop) | Device    | Protocol | Scope | Source IP     | Metric | Notes |
|-------------------|--------------------|-----------|----------|-------|---------------|--------|-------|
| **0.0.0.0/0** (default) | 192.168.1.1       | enp4s0   | dhcp    | global| (none)       | 100   | All traffic not matching other routes goes here. Points to your router (likely your home gateway) on the Ethernet interface enp4s0. Discovered via DHCP. |
| **169.254.0.0/16** | (direct)          | enp4s0   | kernel  | link  | (none)       | 1000  | Link-local (APIPA) range for auto-config when DHCP fails. High metric means it's a fallback—only used if no better route. |
| **172.17.0.0/16** | (direct)          | docker0  | kernel  | link  | 172.17.0.1   | (none)| Docker's default bridge network. "linkdown" means the interface is down (no active containers?). Your host acts as gateway for this subnet. |
| **172.18.0.0/16** | (direct)          | br-c33e38e216df | kernel | link  | 172.18.0.1   | (none)| Another Docker bridge (user-defined network?). Active, so containers on this bridge can reach the host via 172.18.0.1. |
| **192.168.1.0/24** | (direct)         | enp4s0   | kernel  | link  | 192.168.1.35 | 100   | Your local LAN subnet. Directly connected via enp4s0—packets to other devices on 192.168.1.x stay local (e.g., to your router at .1). Your machine's IP is 192.168.1.35. |

#### Key Insights
- **Local/Connected Routes**: The 172.x.x.x and 192.168.1.0/24 entries are "kernel" routes for directly attached networks (no next-hop gateway needed). This matches the simple iteration you described—your system checks if the destination IP falls in these ranges and sends it out the matching device (e.g., enp4s0 for LAN).
- **Docker Influence**: You have Docker installed/running, creating virtual bridges (docker0 and br-...). These allow containers to have their own isolated networks. The "linkdown" on docker0 suggests no containers are using the default bridge right now.
- **Default Route**: Everything else (e.g., google.com) goes via 192.168.1.1 on enp4s0. Metric 100 is low (preferred); the link-local has 1000 to deprioritize it.
- **No Remote Routes**: This table is basic—no dynamic routing protocols (like OSPF) adding entries for distant networks. If you ping something outside 192.168.1.0/24, it'll hit the default.

#### Quick Tests to Verify
- `ping 192.168.1.1` → Should use the local route on enp4s0.
- `ping 8.8.8.8` → Uses default route; trace with `traceroute 8.8.8.8` to see the path.
- `ip addr show enp4s0` → Confirms your interface IP.
- If Docker's involved: `docker network ls` to list bridges.

If this is from your setup and something's not working (e.g., no internet?), common fixes: Check cable/DHCP renewal (`dhclient enp4s0`), or flush routes (`ip route flush cache`). What's going on—troubleshooting connectivity, or just curious about a specific entry?
