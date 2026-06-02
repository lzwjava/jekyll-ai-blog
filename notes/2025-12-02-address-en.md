---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Address Resolution Protocol in Networking
translated: false
type: note
---

Question: What is ARP in networking?

Answer: ARP (Address Resolution Protocol) is a fundamental protocol in TCP/IP networks that translates IP addresses (Layer 3) into MAC addresses (Layer 2), allowing devices on the same local network (LAN) to communicate at the data-link layer.

### How ARP Works
1. A device (e.g., Computer A) wants to send data to another device (Computer B) on the same LAN and knows Computer B's IP address but not its MAC address.
2. Computer A broadcasts an ARP Request packet to the entire local network:
   “Who has IP address 192.168.1.10? Tell 192.168.1.5” (including its own MAC and IP).
3. All devices on the LAN receive the broadcast, but only the device with the matching IP (Computer B) replies with an ARP Reply (unicast):
   “IP 192.168.1.10 is at MAC 00:1A:2B:3C:4D:5E”.
4. Computer A receives the reply, updates its local ARP cache (a temporary table of IP-to-MAC mappings), and can now send Ethernet frames directly to Computer B’s MAC address.

### Key Points
- Operates at Layer 2 (Data Link) of the OSI model but is required for Layer 3 (IP) communication on LANs.
- Used only within the same broadcast domain (same subnet/LAN). Routers do not forward ARP broadcasts.
- ARP is stateless and connectionless.
- Entries in the ARP cache typically expire after a few minutes (e.g., 2–10 minutes depending on OS) to handle changes in hardware.

### ARP Packet Structure (simplified)

| Field              | Purpose                              |
|--------------------|--------------------------------------|
| Hardware Type      | Usually 1 (Ethernet)                 |
| Protocol Type      | Usually 0x0800 (IPv4)                |
| Hardware Address Length | 6 bytes for MAC                   |
| Protocol Address Length | 4 bytes for IPv4                  |
| Operation          | 1 = Request, 2 = Reply               |
| Sender MAC & IP    | Source device info                   |
| Target MAC & IP    | Destination info (target MAC is 00:00:00:00:00:00 in requests) |

### Variants and Related Protocols
- Gratuitous ARP: A device announces its own IP-to-MAC mapping (used when IP changes or to detect duplicates).
- Proxy ARP: A router answers ARP requests on behalf of devices in another subnet.
- ARP Spoofing/Poisoning: A common attack where a malicious device sends fake ARP replies to associate its MAC with someone else’s IP (basis for man-in-the-middle attacks).

### Example (Linux/Windows command)
```bash
# View ARP table
arp -a          # Windows
ip neigh show   # Linux
```

In short: Without ARP, devices on a local network wouldn’t know which physical (MAC) address belongs to a given IP address, and Ethernet communication would fail.
