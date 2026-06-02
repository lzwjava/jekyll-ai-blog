---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Understanding IEEE 802.1Q VLAN Tagging Mechanisms
translated: false
type: note
---

Question: Explain VLAN tagging in detail

Answer:

### What is VLAN Tagging?
VLAN tagging is a mechanism defined by the IEEE 802.1Q standard to identify which Virtual Local Area Network (VLAN) an Ethernet frame belongs to when traversing links that carry traffic from multiple VLANs. It allows switches to segment broadcast domains logically while sharing physical links (trunk ports) between switches or other devices.

Without tagging, standard Ethernet frames have no field to indicate VLAN membership, making it impossible to distinguish traffic from different VLANs on shared links.

### The 802.1Q Tag Format
The 802.1Q protocol inserts a **4-byte (32-bit) tag** into the Ethernet frame header, between the Source MAC Address and the EtherType/Length field.

The tag consists of two main parts:

- **Tag Protocol Identifier (TPID)**: 16 bits, fixed value **0x8100**. This indicates the frame is 802.1Q-tagged.
- **Tag Control Information (TCI)**: 16 bits, broken down as:
  - **Priority Code Point (PCP)**: 3 bits (values 0–7) for Class of Service (CoS) or Quality of Service (QoS) prioritization (IEEE 802.1p).
  - **Drop Eligible Indicator (DEI)**: 1 bit (formerly Canonical Format Indicator or CFI), used to mark frames that can be dropped during congestion.
  - **VLAN Identifier (VID)**: 12 bits, specifying the VLAN ID (1–4094). VID 0 is for priority-tagged frames only (no VLAN ID), and VID 4095 is reserved.

This increases the maximum Ethernet frame size from 1518 bytes to 1522 bytes, and the Frame Check Sequence (FCS) is recalculated after tagging.

### How VLAN Tagging Works on Switches
- **Access Ports** (Untagged Ports): Connect to end devices (e.g., PCs). Frames are sent/received **untagged**. The switch associates the port with a single VLAN (Port VLAN ID or PVID). Incoming untagged frames are assigned to this VLAN; outgoing frames to that VLAN are stripped of any internal tag.
- **Trunk Ports** (Tagged Ports): Connect switches or VLAN-aware devices. They carry multiple VLANs.
  - **Ingress (Incoming Frames)**:
    - Tagged frames: The switch reads the VID and forwards based on it (if the VLAN is allowed).
    - Untagged frames: Assigned to the **Native VLAN** (default VLAN 1).
  - **Egress (Outgoing Frames)**:
    - For non-native VLANs: The switch **adds** the 802.1Q tag with the appropriate VID.
    - For the native VLAN: Frames are sent **untagged** (tag is stripped if present internally).
    - Many switches (e.g., Cisco) drop incoming tagged frames matching the native VLAN VID to prevent inconsistencies or attacks.

End devices typically do not understand tags, so tags are added/removed by switches at the edges.

### Native VLAN
The native VLAN handles **untagged traffic** on trunk ports:
- Untagged incoming frames are placed in the native VLAN.
- Outgoing frames for the native VLAN are sent untagged.
- It must match on both ends of a trunk to avoid mismatches (which can cause issues like CDP warnings or dropped frames).
- Best practice: Change from default VLAN 1 for security (to mitigate VLAN hopping attacks).

### Benefits and Use Cases
- Enables VLAN extension across switches without dedicated links per VLAN.
- Supports QoS via PCP.
- Maintains backward compatibility with untagged devices.

### Potential Issues
- Native VLAN mismatches can lead to unexpected forwarding or security risks.
- Double tagging (QinQ, 802.1ad) extends for provider networks but adds complexity.

VLAN tagging is essential for efficient, secure multi-VLAN networks in enterprise environments.

References:

- [IEEE 802.1Q - Wikipedia](https://en.wikipedia.org/wiki/IEEE_802.1Q)
- [Fundamentals of 802.1Q VLAN Tagging - Cisco Meraki Documentation](https://documentation.meraki.com/Platform_Management/Dashboard_Administration/Design_and_Configure/Configuration_Guides/Routing_and_Firewall/Fundamentals_of_802.1Q_VLAN_Tagging)
- [802.1Q Encapsulation Explained - NetworkLessons](https://networklessons.com/switching/802-1q-encapsulation-explained)
- [Tagged, Untagged, and Native VLANs - Network Direction](https://networkdirection.net/articles/network-theory/taggeduntaggedandnativevlans/)
