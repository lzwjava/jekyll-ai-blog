---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: DHCP IPv4 Operation Explained
translated: false
type: note
---

**Question:** How does DHCP work in IPv4?

**Answer:**

Dynamic Host Configuration Protocol (DHCP) in IPv4 is a client-server protocol that automatically assigns IP addresses and other network configuration parameters (such as subnet mask, default gateway, and DNS servers) to devices (clients) on a network. This eliminates the need for manual configuration, reduces errors, and efficiently manages IP address allocation from a pool.

### Key Components
- **DHCP Client**: The device (e.g., computer, phone) requesting configuration.
- **DHCP Server**: Maintains a pool of IP addresses and assigns them with a lease time.
- **DHCP Relay Agent** (optional): Forwards requests across subnets if the server is not on the same local network.

DHCP uses UDP ports: 67 (server) and 68 (client).

### The DHCP Process: DORA
The core process for obtaining a new IP address is called **DORA** (Discover, Offer, Request, Acknowledge). All initial messages are broadcast because the client has no IP address yet.

1. **Discover (DHCPDISCOVER)**
   The client broadcasts a DHCPDISCOVER message to find available servers.
   - Source IP: 0.0.0.0
   - Destination IP: 255.255.255.255 (broadcast)
   - It includes the client's MAC address for identification.

2. **Offer (DHCPOFFER)**
   One or more DHCP servers respond with a DHCPOFFER message, proposing an IP address and configuration options.
   - Broadcast (since client has no IP yet).
   - Includes offered IP, lease duration, subnet mask, gateway, DNS, etc.

3. **Request (DHCPREQUEST)**
   The client selects one offer (usually the first received) and broadcasts a DHCPREQUEST to accept it.
   - This informs other servers that their offers are declined.

4. **Acknowledge (DHCPACK)**
   The selected server sends a DHCPACK to confirm the assignment.
   - The client can now use the IP address.
   - If the server cannot fulfill (e.g., address in use), it sends DHCPNAK (negative acknowledgment).

### Additional Message Types
- **DHCPRELEASE**: Client releases the IP address back to the server.
- **DHCPDECLINE**: Client declines an offered address (e.g., if it detects a conflict).
- **DHCPINFORM**: Client requests additional options without needing a new IP.
- **DHCPNAK**: Server rejects a request.

### Lease Management
- IP addresses are leased for a limited time.
- Clients renew leases (usually at 50% of lease time) using unicast DHCPREQUEST to the original server.
- If renewal fails, clients retry at later intervals or restart DORA.

This process ensures efficient, dynamic IP management in IPv4 networks.

**References:**

- [Dynamic Host Configuration Protocol - Wikipedia](https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol)
- [What is DHCP (Dynamic Host Configuration Protocol)? | TechTarget](https://www.techtarget.com/searchnetworking/definition/DHCP)
- [DHCP defined and how it works | Network World](https://www.networkworld.com/article/966242/dhcp-defined-and-how-it-works.html)
- [What is the DHCP DORA Process? | nwkings.com](https://www.nwkings.com/dora-process-in-dhcp)
