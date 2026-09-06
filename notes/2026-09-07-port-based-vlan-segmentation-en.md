---
audio: false
generated: true
image: false
lang: en
layout: post
title: Port-Based VLAN Segmentation
translated: false
type: note
---

**Question:** How do you use the port-based method to separate VLAN networks?

**Answer:** Port-based VLANs (also called "access port" VLANs) are the most common way to segment a network using a managed switch. Each physical switch port is assigned to exactly one VLAN, and all traffic entering that port is automatically tagged with the corresponding VLAN ID. Devices in different VLANs cannot communicate without going through a router or Layer 3 switch.

Here's a diagram of how it works:**How it works step by step:**

**1. Assign ports to VLANs (access ports)**
Each port is configured as an *access port* belonging to one VLAN. Any device plugged in automatically joins that VLAN — no configuration on the device is needed.

```
! Cisco IOS example
interface FastEthernet0/1
  switchport mode access
  switchport access vlan 10

interface FastEthernet0/4
  switchport mode access
  switchport access vlan 20
```

**2. Traffic is isolated by the switch**
The switch tags incoming frames with the VLAN ID internally. Frames from VLAN 10 are *never* forwarded to VLAN 20 or 30 ports — the switch enforces this in hardware.

**3. Use a trunk port for inter-VLAN routing (if needed)**
A *trunk port* carries tagged traffic for multiple VLANs to a router or Layer 3 switch. The router then routes between VLANs using sub-interfaces (a technique called *Router-on-a-Stick*) or the L3 switch routes internally.

```
! Trunk port config
interface FastEthernet0/8
  switchport mode trunk
  switchport trunk allowed vlan 10,20,30
```

**Key rules to remember:**

- Devices in the *same* VLAN communicate freely through the switch (Layer 2).
- Devices in *different* VLANs are isolated — communication requires a router or L3 switch.
- Port assignment is done per-switch-port, not per-device, so a device inherits the VLAN of the port it's plugged into.
- Trunk ports are the only exception — they carry multiple VLANs simultaneously using 802.1Q tagging.

---

**References:**

- [Cisco VLAN Configuration Guide](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/16-12/configuration_guide/vlan/b_1612_vlan_9300_cg/configuring_vlans.html)
- [IEEE 802.1Q VLAN Standard Overview](https://www.ieee802.org/1/pages/802.1Q.html)
- [Port-Based VLAN — NetworkLessons.com](https://networklessons.com/switching/introduction-to-vlans)
