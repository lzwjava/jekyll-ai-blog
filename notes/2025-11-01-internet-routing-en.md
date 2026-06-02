---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: How Internet Routing Works
translated: false
type: note
---

Yes, you're spot on with the high-level flow—once your computer has the IP address (like 106.63.15.9 for weibo.com), it initiates a connection that hops through your local network, your router, your ISP's infrastructure, and across the internet's interconnected routers ("layer by layer") until it reaches the target server. This is all handled automatically by the TCP/IP protocol stack, without you doing anything manual beyond typing the URL or running a command like `ping`.

I'll break it down step by step, tying in your `ping` and `traceroute` output for context. I'll keep it practical and focused on what happens under the hood, assuming a typical home setup like yours (Mac on Wi-Fi/Ethernet behind a router).

### 1. **DNS Resolution (Getting the IP)**

- Before any connection, your computer first translates the domain name (e.g., "weibo.com") to an IP via DNS (Domain Name System). This happens via your OS's DNS resolver, which queries public DNS servers (like 8.8.8.8 from Google).
- In your case, `ping weibo.com` automatically does this resolution, confirming 106.63.15.9 as the IPv4 address. (Note: Proxies like your local one at 127.0.0.1:7890 typically handle HTTP/HTTPS traffic, but `ping` uses raw IP/ICMP, so it bypasses the proxy.)
- If DNS fails, no connection happens—everything stops here.

### 2. **Your Computer Prepares the Packet (Local Side)**

- Once it has the IP, your Mac builds a **packet** (a chunk of data) using the TCP/IP layers:
  - **Application Layer**: The command or app (e.g., browser or `ping`) requests data. `Ping` sends an ICMP "echo request" (a simple "hey, are you there?" message).
  - **Transport Layer**: Adds TCP/UDP headers (for reliability/port numbers) or ICMP for ping. Your pings use ICMP, with 56 bytes of data + headers = 64-byte packets.
  - **Network Layer (IP)**: Wraps it in an IP header with source (your local IP, like 192.168.1.x) and destination (106.63.15.9). This is where routing decisions start.
  - **Link Layer (Ethernet/Wi-Fi)**: Adds MAC addresses for the local network hop. Your computer uses ARP (Address Resolution Protocol) to find the router's MAC address.
  - **Physical Layer**: Converts to electrical signals over your cable/Wi-Fi.
- Your computer knows it can't reach 106.63.15.9 directly (it's not on your local 192.168.1.0/24 subnet), so it sends the packet to the **default gateway**—your router at 192.168.1.1.

### 3. **Local Hop: Computer → Router**

- This is the first (and fastest) step, shown in your `traceroute` output:

     ```
     1  192.168.1.1 (192.168.1.1) 26.903 ms 3.150 ms 3.161 ms
     ```

  - `Traceroute` (which sends packets with increasing TTL—Time To Live—to map the path) confirms this hop takes ~3-27ms round-trip.
  - Your router receives the packet, strips off the local Ethernet header, and re-encapsulates it for the next hop. It uses its routing table to forward it toward the internet (via its WAN/ISP connection).
  - Proxies don't affect this—your local proxy (port 7890) is only for app-level traffic like web browsing, not raw IP routing.

### 4. **Router → ISP → Internet Backbone (The "Layer by Layer" Routing)**

- Your router dials up your ISP (e.g., via PPPoE, DHCP, or modem) and hands off the packet to the ISP's edge router. This might involve NAT (Network Address Translation) on your router, swapping your private IP (192.168.1.x) for the public one assigned by your ISP.
- From here, it's a chain of **routers** across the internet:
  - **ISP Routers**: Your ISP (e.g., Comcast or China Telecom) routes it through their core network. Each router decrements the TTL (starts at 64 in your traceroute) and forwards based on BGP (Border Gateway Protocol) tables—essentially a global map of the best path to 106.63.15.9.
  - **Inter-ISP/Backbone Hops**: Packets cross "peering points" between ISPs (e.g., via undersea cables, fiber optics). This could be 5-20 hops total, depending on geography. Weibo.com's IP (106.63.15.9) is in China, so from your location (guessing US/EU based on the proxy), it'd go through trans-Pacific routes.
  - Each hop is a router inspecting the IP header, deciding the next gateway, and forwarding. No single device knows the full path—it's distributed.
- Your `traceroute` got cut off (probably suspended with ^Z), but if you ran it fully, you'd see 10-15 more lines like:

     ```
     2  [ISP router IP] 10 ms ...
     3  [ISP core] 15 ms ...
     ...
     15  106.63.15.9  40 ms ...
     ```

  - Times add up: Your pings show ~40ms total RTT (round-trip time), so one-way to the server is ~20ms.

### 5. **Target Server Receives & Responds**

- The packet arrives at Weibo's server (or a load balancer at 106.63.15.9). It reverses the process: Responds with an ICMP echo reply (for ping) or TCP SYN-ACK (for a web connection).
- The reply follows a similar path back, often the same route but not always (internet routing is asymmetric).
- Your `ping` confirms success: TTL=52 means ~12 hops (64-52=12), and the 40ms latency matches a China-US round trip.

### Why It Feels "Magical" (and Common Gotchas)

- **Automation**: Your OS/kernel handles all this via the network stack (e.g., `ifconfig` or `ip route` shows your routes). No manual config needed unless you're debugging.
- **Your Proxy**: It's transparent for ping/traceroute but would intercept browser traffic to weibo.com, routing it through 127.0.0.1:7890 (likely for VPN/censorship bypass). Disable with `unset HTTP_PROXY HTTPS_PROXY` if testing raw.
- **If It Fails**: Firewalls, MTU mismatches, or route blackholing can drop packets. Tools like `tcpdump` or Wireshark let you sniff this locally.
- **Security Note**: IPs can change (DNS TTL), and HTTPS adds encryption atop this (TLS handshake after TCP connect).

In short, yes—computer → router → ISP → global router mesh → server. It's a beautifully distributed system built on IP routing. If you share a full traceroute or want to dive into a specific part (e.g., TCP handshake for web), let me know!

[TCP/IP Illustrated (Book on Networking Basics)](https://www.oreilly.com/library/view/tcp-ip-illustrated-volume/0201633469/)
[How Traceroute Works (Cloudflare Explanation)](https://www.cloudflare.com/learning/network-layer/what-is-traceroute/)
