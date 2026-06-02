---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Configuring a Switch Trunk Port
translated: false
type: note
---

Question: Which command is used to configure a port as a trunk port on a switch?

Answer:

The correct answer is **B) switchport mode trunk**.

### Explanation:
- On Cisco switches (the most common context for this question), the command **switchport mode trunk** explicitly configures an interface to operate as a trunk port, allowing it to carry traffic for multiple VLANs.
- **A) switchport mode access**: This configures the port as an access port (for a single VLAN only), which is the opposite of a trunk.
- **C) switchport trunk encapsulation dot1q**: This specifies the trunk encapsulation type (802.1Q) but does not by itself make the port a trunk. It is used *after* setting the mode to trunk on older switches that support multiple encapsulation types (e.g., ISL or dot1q). On modern switches, 802.1Q is often the default or only option.
- **D) switchport access vlan 10**: This assigns a specific VLAN to an access port and is unrelated to trunk configuration.

To fully configure a basic trunk port, you typically enter:
```
interface GigabitEthernet0/1
switchport mode trunk
```
Additional commands like encapsulation or allowed VLAN lists may follow depending on requirements, but **switchport mode trunk** is the core command that sets the port to trunk mode.
