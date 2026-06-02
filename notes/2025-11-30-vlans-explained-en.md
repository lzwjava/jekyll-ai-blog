---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: VLANs Explained Simply
translated: false
type: note
---

### What is a VLAN (Virtual Local Area Network)?

A VLAN is a technology that lets you create **multiple separate LANs (broadcast domains) on the same physical network switch** without needing separate switches or cables.

Think of it like this:
Normally, all devices plugged into the same switch are on the same network and can talk to each other freely (same broadcast domain).
With VLANs, you can logically split that one physical switch into many isolated networks — even if the devices are connected to the same switch.

#### Why use VLANs? (Main benefits)

| Benefit                  | Explanation                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| Security                 | Devices in different VLANs cannot communicate directly (even on the same switch) unless you explicitly allow it with a router/firewall. |
| Broadcast control        | Reduces unnecessary traffic — a broadcast in VLAN 10 doesn’t reach VLAN 20. |
| Organization             | Group devices by department, function, or sensitivity (e.g., HR, Guests, IoT, Servers, Voice). |
| Flexibility              | Move a user to a new desk? Just change the switch port VLAN — no rewiring. |
| Cost savings             | One big switch instead of many small ones.                                  |

#### How VLANs actually work

Switches that support VLANs (almost all managed switches) add a **VLAN tag** (usually an 802.1Q tag) to Ethernet frames.

- Each port on the switch can be configured as:
  - **Access port** → belongs to exactly one VLAN (typical for end devices like PCs, printers, IP phones).
  - **Trunk port** → carries traffic for multiple VLANs (used to connect switches together or to a router). Trunk ports add/remove the 4-byte 802.1Q tag.

The tag contains a **VLAN ID** (VID), usually 1–4094.

Example:
```
VLAN 10 → Employees
VLAN 20 → Guests (internet only)
VLAN 30 → VoIP phones
VLAN 99 → Management
```

Even if a guest laptop and an employee laptop are plugged into the same 48-port switch, they are in completely different networks and can’t see each other unless you route between them.

#### Common VLAN types / tagging methods

| Type              | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| Port-based VLANs  | Simplest — assign each switch port to a VLAN (most common).                 |
| MAC-based VLANs   | Device’s MAC address determines VLAN (rare, used in some BYOD scenarios).   |
| Protocol-based    | Old method based on layer-3 protocol (almost never used today).            |
| Tagged (802.1Q)   | Frames carry a VLAN tag — required on trunk links.                          |
| Untagged          | Normal Ethernet frame — used on access ports (the switch adds/removes tag). |

#### Real-world example

A typical small/medium business switch setup:

```
Floor switch ports:
  Ports 1–20 → VLAN 10 (Employees) – untagged
  Ports 21–30 → VLAN 20 (Guests)   – untagged
  Ports 31–40 → VLAN 30 (VoIP)     – untagged
  Port 48      → Trunk to router/firewall (carries VLAN 10,20,30 tagged)
```

The router/firewall has subinterfaces (e.g., GigabitEthernet0/0.10, .20, .30) and applies different policies:
- VLAN 10 → full internal access
- VLAN 20 → internet only, no internal access
- VLAN 30 → QoS priority for voice

#### Important notes

- VLAN 1 is the default VLAN on most switches — avoid using it for real traffic.
- Devices in different VLANs need a Layer-3 device (router or Layer-3 switch) to communicate.
- “Inter-VLAN routing” can be done on the same device (router-on-a-stick) or on a Layer-3 switch for better performance.

In short: VLANs = logical separation of networks on the same physical infrastructure for security, performance, and simplicity. They’re a fundamental building block of almost every modern enterprise network.
