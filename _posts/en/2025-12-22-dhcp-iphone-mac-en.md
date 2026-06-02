---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: DHCP Issues with iPhone and Mac
translated: false
type: note
---

Question: In what cases does DHCP fail when connecting an iPhone and Mac via adapters/converters to a 5-port Mercury Ethernet switch, which is then connected to a router, and why does the connection order matter (e.g., needing to connect the iPhone first after disconnecting the Mac)?

Answer:

Your setup involves connecting both an iPhone (likely via a USB-C/Lightning to Ethernet adapter) and a Mac (via Thunderbolt/USB-C to Ethernet adapter) to a 5-port unmanaged Ethernet switch (probably a Mercusys or similar brand basic switch), with one port on the switch uplinked to your router. The router acts as the DHCP server, assigning IP addresses to devices on the network.

The intermittent DHCP issues, where one device (often the iPhone) fails to get an IP address unless connected in a specific order, are commonly caused by one of the following:

### 1. **ARP Cache or MAC Address Table Issues in the Switch**

- Unmanaged switches maintain a MAC address table to forward traffic efficiently.
- If the Mac connects first, the switch learns the Mac's Ethernet MAC address on the uplink port (toward the router).
- When the iPhone connects later and sends a DHCP request (broadcast), the switch may incorrectly forward it based on the stale entry, or there could be an ARP resolution conflict.
- The router's ARP table might also cache the first device's MAC, causing it to ignore or fail to respond properly to the second device's request.
- Reversing the order (iPhone first) works temporarily because it clears or updates the cache for the iPhone's MAC.

### 2. **Router DHCP Server Limitation or Bug**

- Some home routers (especially ISP-provided ones) have quirks where they associate the network with the first connected device's MAC address.
- Similar to "modem-only" mode issues reported with certain providers, the DHCP server may only reliably assign addresses to one device behind the switch until rebooted or reordered.
- Apple devices (iPhone and Mac) seem more prone to this due to how iOS/macOS handles DHCP requests over USB Ethernet adapters.

### 3. **Adapter-Specific Behavior**

- USB-based Ethernet adapters on Apple devices can sometimes cause delayed or failed DHCP negotiations, especially when multiple are behind a switch.
- Issues like slow ARP resolution or adapters not fully initializing until plugged in a certain sequence have been reported.

### Recommended Fixes

- **Power cycle the router and switch**: Unplug both for 30 seconds, then reconnect. This clears ARP/MAC tables.
- **Renew DHCP lease manually**:
  - On Mac: System Settings > Network > Ethernet > Details > Renew DHCP Lease.
  - On iPhone: Settings > Ethernet > Renew Lease (or toggle Ethernet off/on).
- **Try different connection order or ports**: Test swapping cables/ports on the switch.
- **Use static IPs temporarily**: Assign manual IPs in the router's range (e.g., 192.168.1.x) to test if connectivity works without DHCP.
- **Best long-term solution**: Connect the router directly to one device if possible, or add a better switch/router. If your router supports it, reserve IPs by MAC address in its DHCP settings.
- **Reboot router when switching devices**: This reliably resets the caches.

This behavior is a known quirk in some home networks with switches and USB Ethernet adapters, particularly with Apple devices.

References:

- <https://apple.stackexchange.com/questions/317888/apple-usb-ethernet-adapter-has-a-self-assigned-ip-address-and-will-not-be-able-t>
- <https://discussions.apple.com/thread/6497865>
- <https://apple.stackexchange.com/questions/297328/my-mac-wont-connect-with-ethernet-but-will-to-wireless>
- <https://forums.tomshardware.com/threads/can-dhcp-be-effected-by-a-network-switch.3696191/>
- <https://serverfault.com/questions/161225/router-dhcp-not-working-with-switch>
