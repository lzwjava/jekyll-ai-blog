---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Trunk Ports Explained
translated: false
type: note
---

Question: What is a trunk port in a switch?

Answer:

A **trunk port** on a network switch is a special type of port configured to carry traffic for **multiple Virtual Local Area Networks (VLANs)** over a single physical link. This is in contrast to an **access port**, which is dedicated to a single VLAN and typically connects to end devices like computers or printers.

### Key Characteristics of a Trunk Port:
- **Multi-VLAN Support**: It allows frames from different VLANs to travel across the link (e.g., between two switches or from a switch to a router).
- **VLAN Tagging**: To distinguish traffic from different VLANs, trunk ports use **tagging**. The most common standard is **IEEE 802.1Q**, which inserts a 4-byte tag into the Ethernet frame header containing the VLAN ID (VID). This ensures the receiving device knows which VLAN the frame belongs to.
- **Native VLAN**: Trunk ports often have a "native VLAN" (usually VLAN 1 by default on Cisco devices). Frames for the native VLAN are sent **untagged**, while others are tagged. This provides backward compatibility with devices that don't support tagging.
- **Common Uses**:
  - Connecting switches together to extend the same VLANs across multiple devices.
  - Linking a switch to a router (e.g., in "router-on-a-stick" setups for inter-VLAN routing).
  - Connecting to devices that understand VLAN tags, such as IP phones, servers with multiple virtual machines, or access points broadcasting multiple SSIDs.

### Trunk Port vs. Access Port:

| Feature              | Access Port                          | Trunk Port                              |
|----------------------|--------------------------------------|-----------------------------------------|
| VLANs Supported      | Single VLAN only                     | Multiple VLANs                          |
| Tagging              | Untagged frames (switch adds/removes tags internally) | Tagged frames (using 802.1Q or legacy ISL) |
| Typical Connection   | End devices (PCs, printers, etc.)    | Switches, routers, or tag-aware devices |
| Frame Handling       | Assigns all traffic to one VLAN      | Carries and separates traffic for many VLANs |
| Security Consideration | Simpler, isolates to one VLAN        | Higher risk (e.g., VLAN hopping if misconfigured); use pruning to restrict allowed VLANs |

Trunk ports make networks more efficient by reducing the need for multiple physical cables—one trunk link can replace many separate links for each VLAN. However, they require careful configuration to avoid security issues or misrouting.

References:

- [JumpCloud: What Is a Trunk Port?](https://jumpcloud.com/it-index/what-is-a-trunk-port)
- [N-able: VLAN Trunking Overview](https://www.n-able.com/blog/vlan-trunking)
- [GeeksforGeeks: Access and Trunk Ports](https://www.geeksforgeeks.org/computer-networks/access-trunk-ports/)
- [Network Engineering Stack Exchange: Purpose of Trunk Port](https://networkengineering.stackexchange.com/questions/40668/what-is-the-purpose-of-a-trunk-port-in-a-network-switch)
- [Cisco Press: Trunk Links](https://www.ciscopress.com/articles/article.asp?p=29803&seqNum=3)
