---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: VLAN Tagging and Port Frame Handling
translated: false
type: note
---

Question: How does the overall process of VLAN tagging and frame handling work on switch ports, particularly with access ports and tagged frames?

Answer:

### Overview of VLANs and Switch Ports

Virtual Local Area Networks (VLANs) segment a physical network into logical broadcast domains. Switches use two main port types for VLAN handling:

- **Access ports**: Connect to end devices (e.g., PCs, printers) that do not understand VLAN tags. An access port belongs to **one single VLAN** (configured as the access VLAN).
- **Trunk ports**: Connect to other switches or VLAN-aware devices. They carry traffic for **multiple VLANs**, using 802.1Q tags to identify which VLAN each frame belongs to.

The IEEE 802.1Q standard defines VLAN tagging by inserting a 4-byte tag (including VLAN ID) into the Ethernet frame header.

### Frame Handling on Access Ports

**Ingress (incoming frames to the access port):**

- **Untagged frames** (normal from end devices): The switch internally assigns the frame to the configured access VLAN. No tag is added to the wire frame; tagging is handled internally for switching decisions.
- **Tagged frames**: Access ports expect only untagged traffic. Receiving a tagged frame is considered invalid.
  - In most modern Cisco switches (e.g., Catalyst 2960 and later), **all tagged frames are dropped**.
  - On some older models (e.g., 2950, 3550, Nexus in certain cases), if the tag matches the access VLAN ID, the tag is stripped and the frame is processed; otherwise, dropped.
  - Overall standard behavior (especially in exam contexts like CCNA/CCNP): **Drops all tagged frames** to maintain security and prevent VLAN hopping attacks.

**Egress (outgoing frames from the access port):**

- Frames destined for the connected device: The switch **removes any internal VLAN tag** and sends the frame untagged.

### Frame Handling on Trunk Ports

**Ingress:**

- **Tagged frames**: Processed if the VLAN ID is allowed on the trunk; otherwise dropped.
- **Untagged frames**: Assigned to the **native VLAN** (default VLAN 1). Note: Trunk ports can receive untagged frames for the native VLAN.

**Egress:**

- Frames for non-native VLANs: Sent with the 802.1Q tag added.
- Frames for the native VLAN: Sent untagged (unless "vlan dot1q tag native" is configured globally, which tags everything and drops untagged ingress).

### Overall Frame Flow Example (Host A in VLAN 10 → Host B in VLAN 10 via two switches)

1. Host A sends an **untagged** frame.
2. Switch1 access port receives it → internally assigns to VLAN 10.
3. Switch1 forwards internally → to trunk port → adds VLAN 10 tag → sends to Switch2.
4. Switch2 trunk port receives tagged frame → verifies VLAN 10 allowed → removes tag if forwarding to access port.
5. Switch2 access port sends **untagged** frame to Host B.

This ensures end devices see only untagged traffic, while switches use tags internally and on trunks for proper segmentation.

### Why Access Ports Drop Tagged Frames

- Security: Prevents malicious devices from injecting tagged traffic to access unauthorized VLANs (VLAN hopping).
- Design: End devices are not expected to send tags.

This behavior aligns with IEEE 802.1Q principles and Cisco best practices.

References:

- [Cisco Community: Tagged frames on access ports](https://community.cisco.com/t5/switching/tagged-frames-on-access-ports/td-p/1074967)
- [Network Engineering Stack Exchange: What happens with tagged traffic on access port of Cisco switch?](https://networkengineering.stackexchange.com/questions/28888/what-happens-with-tagged-traffic-on-access-port-of-cisco-switch)
- [NetworkLessons: VLANs - when a tagged frame arrives on an access port](https://notes.networklessons.com/vlans-when-a-tagged-frame-arrives-on-an-access-port)
- [Cisco: Understanding VLAN Tagging](https://www.cisco.com/c/en/us/support/docs/lan-switching/vlan/17056-741.html)
