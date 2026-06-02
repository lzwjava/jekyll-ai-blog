---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Huawei Switch STP Configuration Commands
translated: false
type: note
---

Question: What are the typical commands for Spanning Tree Protocol (STP) on Huawei switches?

Answer:

Huawei switches support multiple spanning tree modes: STP (traditional), RSTP (rapid), and MSTP (multiple instances, default on many models). Classic STP is configured by setting the mode to STP, though RSTP or MSTP is more commonly used today.

### Global Configuration Commands

- `stp mode stp`
  Sets the spanning tree mode to classic STP (options: stp, rstp, mstp).

- `stp enable`
  Globally enables STP (often enabled by default).

- `stp disable`
  Globally disables STP.

- `stp priority <value>`
  Sets the bridge priority (0–61440, multiples of 4096; lower value preferred for root).

- `stp root primary`
  Configures the switch as primary root bridge (sets priority to 0).

- `stp root secondary`
  Configures the switch as secondary root bridge (sets priority to 4096).

### Interface Configuration Commands

Enter interface view first: `interface <interface-type> <interface-number>`

- `stp enable`
  Enables STP on the specific interface.

- `stp disable`
  Disables STP on the interface (useful for edge ports).

- `stp cost <value>`
  Manually sets the path cost on the port.

- `stp edged-port enable`
  Configures the port as an edge port (quickly transitions to forwarding; for end-device connections).

- `stp root-protection`
  Enables root protection (blocks port if it receives superior BPDUs).

- `stp loop-protection`
  Enables loop protection (blocks port if it stops receiving BPDUs).

- `stp bpdu-protection`
  (Global or interface) Protects against unexpected BPDUs on edge ports.

### Display and Verification Commands

- `display stp`
  Shows detailed STP status and topology.

- `display stp brief`
  Shows a summary of STP status.

- `display stp interface <interface>`
  Shows STP information for a specific interface.

- `display stp region-configuration`
  (Relevant in MSTP mode) Shows MST region details.

These commands are executed in system view unless specified otherwise. Configurations should be committed or saved as needed on cloud-engine models.

References:

- [https://ipcisco.com/lesson/stp-configuration-on-huawei/](https://ipcisco.com/lesson/stp-configuration-on-huawei/)
- [https://support.huawei.com/enterprise/en/doc/EDOC1100198418/9ccc5041/stp-rstp-mstp-vbst-configuration-commands](https://support.huawei.com/enterprise/en/doc/EDOC1100198418/9ccc5041/stp-rstp-mstp-vbst-configuration-commands)
- [https://support.huawei.com/enterprise/en/doc/EDOC1000178165/9ccc5041/stp-rstp-mstp-vbst-configuration-commands](https://support.huawei.com/enterprise/en/doc/EDOC1000178165/9ccc5041/stp-rstp-mstp-vbst-configuration-commands)
