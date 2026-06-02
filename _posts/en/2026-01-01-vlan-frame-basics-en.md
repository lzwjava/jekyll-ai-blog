---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: VLAN Tagging and Network Frame Fundamentals
translated: false
type: note
---

Question: VLANs do not provide encryption; they only tag frames with VLAN IDs for segmentation. How are frames tagged, and when are they tagged? What are frames? Where do VLANs run? How do computers tag them? How does a computer know its frames will go to a VLAN?

Answer:

### What Are Frames?
In computer networking, particularly in Ethernet-based local area networks (LANs), data is transmitted in units called **frames**. An Ethernet frame is a structured packet of data that includes:
- **Preamble and Start Frame Delimiter (SFD)**: For synchronization.
- **Destination and Source MAC Addresses**: To identify the sender and receiver at the hardware level.
- **EtherType/Length Field**: Indicates the protocol or length of the data.
- **Payload/Data**: The actual information being sent (e.g., IP packets).
- **Frame Check Sequence (FCS)**: For error detection.

Frames operate at Layer 2 (Data Link Layer) of the OSI model. They are the basic units for switching and are encapsulated around higher-layer data like IP packets.

### What Are VLANs and Where Do They Run?
VLANs (Virtual Local Area Networks) are a technology used to logically segment a physical network into multiple isolated broadcast domains. They run primarily on **network switches** (Layer 2 devices), which are responsible for implementing VLAN configurations. VLANs are defined by the IEEE 802.1Q standard and operate at the Data Link Layer (Layer 2).

- **Where VLANs Run**:
  - On managed switches: Switches maintain VLAN databases and handle traffic segmentation.
  - Not on basic hubs or unmanaged switches, as they lack VLAN support.
  - Can extend to routers or Layer 3 switches for inter-VLAN routing.
  - VLANs do not run on end-user computers by default; computers connect to VLANs via switch ports configured for specific VLANs.

VLANs help in improving security, reducing broadcast traffic, and organizing networks (e.g., separating departments like HR and Finance on the same physical infrastructure).

### How Are Frames Tagged, and When Are They Tagged?
VLAN tagging adds a **VLAN ID (VID)** to Ethernet frames to identify which VLAN they belong to. This is done using the **IEEE 802.1Q protocol**, which inserts a 4-byte tag (called the 802.1Q tag or VLAN tag) into the frame header, right after the source MAC address.

- **How Frames Are Tagged**:
  - The tag includes:
    - **Tag Protocol Identifier (TPID)**: A 2-byte field set to 0x8100 to indicate it's an 802.1Q tag.
    - **Tag Control Information (TCI)**: A 2-byte field containing:
      - Priority Code Point (PCP): 3 bits for QoS priority (0-7).
      - Drop Eligible Indicator (DEI): 1 bit for congestion handling.
      - VLAN ID (VID): 12 bits, allowing for 4096 possible VLANs (0-4095, with 0 and 4095 reserved).
  - This increases the frame size from the standard 1518 bytes to up to 1522 bytes (jumbo frames can be larger if supported).
  - Tagging is optional for single-VLAN setups but essential for multi-VLAN environments.

- **When Frames Are Tagged**:
  - Tagging occurs when a frame needs to traverse a **trunk link** (a connection between switches or between a switch and a router that carries traffic from multiple VLANs).
  - On ingress (incoming): When an untagged frame enters an access port on a switch, the switch tags it with the port's configured VLAN ID before forwarding it internally or over a trunk.
  - On egress (outgoing): Over trunk ports, frames are sent tagged. On access ports, tags are removed before sending to end devices.
  - Tagging is not done on access ports for end devices unless the device explicitly supports and requests tagging (e.g., via 802.1Q-aware software).

### How Do Computers Tag Frames?
Computers (end hosts like PCs) typically do not tag frames themselves because most standard network interface cards (NICs) and operating systems handle untagged traffic. However, computers can tag frames if configured to do so:

- **Requirements for Computer Tagging**:
  - **VLAN-Aware NIC**: The hardware must support 802.1Q (most modern NICs do).
  - **Software Configuration**:
    - In Windows: Use Device Manager to enable VLAN tagging on the NIC properties, or use PowerShell/commands like `Set-NetAdapterBinding`.
    - In Linux: Use tools like `vconfig` (older) or `ip link` to create VLAN subinterfaces (e.g., `ip link add link eth0 name eth0.10 type vlan id 10`).
    - In macOS: Via System Preferences or `networksetup` command.
  - This is common in virtualized environments (e.g., VMware, Hyper-V) or for servers hosting multiple virtual machines on different VLANs.

- **Process**:
  - The computer's OS or application specifies the VLAN ID when sending data.
  - The NIC inserts the 802.1Q tag into the frame before transmitting it.
  - This is rare for standard desktops; it's more for advanced setups like VoIP phones or servers.

If a computer doesn't tag frames, the connected switch port (configured as an access port) will add the tag based on the port's default VLAN.

### How Does a Computer Know Its Frames Will Go to a VLAN?
Computers generally do not "know" about VLANs inherently because VLANs are a switch-level abstraction. Instead:

- **Switch Port Configuration Determines It**:
  - **Access Ports**: Assigned to a single VLAN. The computer sends untagged frames, and the switch tags them with the port's VLAN ID. The computer is unaware; it just sees a standard Ethernet connection.
  - **Trunk Ports**: Allow multiple VLANs. If the computer is connected to a trunk and supports tagging, it must tag its own frames with the correct VID; otherwise, frames may default to a native VLAN (untagged VLAN on the trunk).

- **How the Computer Learns or Configures**:
  - Via manual configuration: Administrators set VLAN subinterfaces on the computer.
  - Dynamic protocols: Like Dynamic Host Configuration Protocol (DHCP) with VLAN options, or protocols like Multiple VLAN Registration Protocol (MVRP), but these are advanced and not common for end hosts.
  - In virtual environments: Hypervisors assign VLANs to virtual NICs.
  - The computer doesn't need to "know" for basic operation; the network infrastructure enforces segmentation. If misconfigured, the computer's traffic might end up in the wrong VLAN or be dropped.

In summary, VLAN tagging enables segmentation without encryption, focusing on logical isolation. For security, combine VLANs with other measures like ACLs or encryption protocols (e.g., IPsec).
