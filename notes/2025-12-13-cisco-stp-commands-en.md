---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Cisco Spanning Tree Protocol Commands
translated: false
type: note
---

Question: What are the typical commands for Spanning Tree Protocol (STP) on a Cisco switch?

Answer:

Spanning Tree Protocol (STP) is enabled by default on Cisco switches, often running Rapid Per-VLAN Spanning Tree (Rapid PVST+) or PVST+. Typical commands fall into two categories: **verification/show commands** (most commonly used for monitoring and troubleshooting) and **configuration commands** (for tuning STP behavior).

### Verification/Show Commands

These are the most frequently used to check STP status, root bridge, port roles, and topology.

- `show spanning-tree`
  Displays detailed STP information for all VLANs, including root bridge, port roles (Root, Designated, Blocked), costs, and states.

- `show spanning-tree vlan <vlan-id>`
  Shows STP details for a specific VLAN (recommended when many VLANs exist to avoid lengthy output).

- `show spanning-tree summary`
  Provides a high-level overview: STP mode (e.g., PVST, Rapid PVST+), root status, port counts per state, and enabled features like PortFast or Loopguard.

- `show spanning-tree detail`
  More verbose details, including timers and port information.

- `show spanning-tree bridge`
  Displays the local bridge ID and timers.

- `clear spanning-tree counters [interface]`
  Clears STP BPDU counters for troubleshooting.

- `clear spanning-tree detected-protocols`
  Forces STP protocol migration renegotiation.

### Configuration Commands

Entered in global or interface configuration mode. STP is enabled by default; these tune it.

#### Global Configuration

- `spanning-tree mode {rapid-pvst | pvst | mst | rstp | stp}`
  Sets the STP mode. Rapid PVST+ is common/default on many Catalyst switches for faster convergence.

- `spanning-tree vlan <vlan-id> priority <value>`
  Sets bridge priority for a VLAN (multiples of 4096, lower = more likely root). Default: 32768.

- `spanning-tree vlan <vlan-id> root primary`
  Automatically sets low priority to make this switch the root bridge.

- `spanning-tree vlan <vlan-id> root secondary`
  Makes it secondary root.

- `spanning-tree hello-time <seconds>`
  Sets hello interval (default: 2 seconds).

- `spanning-tree forward-time <seconds>`
  Sets forward delay (default: 15 seconds).

- `spanning-tree max-age <seconds>`
  Sets max age timer (default: 20 seconds).

#### Interface Configuration

- `spanning-tree portfast`
  Enables PortFast (immediate forwarding on edge ports; use on access ports to hosts).

- `spanning-tree bpduguard enable`
  Disables port if it receives BPDUs (protects against accidental loops).

- `spanning-tree cost <value>`
  Manually sets port path cost.

- `spanning-tree port-priority <value>`
  Sets port priority (influences role selection).

- `spanning-tree guard root`
  Enables root guard (prevents inferior BPDUs from making port root).

- `spanning-tree link-type point-to-point`
  Assumes full-duplex point-to-point link for faster RSTP convergence.

These commands vary slightly by switch model and IOS version (e.g., Catalyst 9200/9300 vs. older 2960). Always verify with `show running-config | include spanning-tree`.

References:

- [Cisco Catalyst Spanning Tree Configuration Guide](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9200/software/release/16-12/configuration_guide/lyr2/b_1612_lyr2_9200_cg/configuring_spanning_tree_protocol.html)
- [Cisco Spanning Tree Protocol Guide with Examples](https://www.networkstraining.com/cisco-spanning-tree-protocol/)
- [Cisco CLI Guide for Spanning Tree Commands](https://www.cisco.com/c/en/us/td/docs/switches/campus-lan-switches-access/Catalyst-1200-and-1300-Switches/cli/C1200-cli/spanning-tree-commands.html)
- [Cisco Press: Spanning Tree Configuration](https://www.ciscopress.com/articles/article.asp?p=2832407&seqNum=6)
