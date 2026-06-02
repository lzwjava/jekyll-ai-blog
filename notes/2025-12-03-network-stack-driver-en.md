---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Network Stack and Driver Responsibilities
translated: false
type: note
---

Question: What do network interface card (NIC) drivers and the kernel's network stack typically handle (beyond just ARP packets)?

Answer:

The NIC driver and the kernel's network stack are responsible for the lowest layers of network processing (mostly Layer 1 and Layer 2, and the entry point to Layer 3). Beyond ARP, they typically handle the following tasks for **all** incoming and outgoing traffic:

### Incoming Packets (Receive Path)

1. **Physical layer signaling** – The NIC converts electrical/optical signals into raw bits/bytes.
2. **Frame reception and DMA** – The NIC driver sets up DMA rings; the card writes received Ethernet frames (or Wi-Fi, etc.) directly into kernel memory.
3. **Basic frame validation** – CRC/checksum offloading, VLAN tag stripping (if configured), minimum/maximum size checks.
4. **Link-layer demultiplexing** – Based on the Ethernet Type field (or equivalent):
   - 0x0800 → IPv4
   - 0x86DD → IPv6
   - 0x0806 → ARP (already mentioned)
   - 0x888E → 802.1X/EAPOL
   - 0x8917 → 802.1X PAE
   - 0x88E5 → MACsec
   - 0x8100 → VLAN-tagged frames
   - Others (LLDP, PTP, FCoE, etc.)
5. **Hardware offloading** (often done in NIC before driver sees the frame):
   - Checksum validation (IP header, TCP/UDP/ICMP)
   - Large Receive Offload (LRO)/Generic Receive Offload (GRO)
   - RSS (Receive Side Scaling) – distributing packets to multiple CPU cores
   - TCP Segmentation Offload receive side (rare)
6. **Passing the packet up** – The driver calls `netif_rx()` or NAPI (`napi_gro_receive()`) → packet enters the stack as an `sk_buff`.

### Early Kernel Network Stack Processing (before netfilter/iptables/nftables)

Once the packet is in the stack (still in softIRQ context):

- GRO (Generic Receive Offload) – coalescing packets
- Early demux for certain protocols (e.g., high-priority control traffic)
- **netfilter PREROUTING hook** (NF_INET_PRE_ROUTING) – this is the very first point where iptables/nftables rules can see/drop packets
- IP stack processing (if it’s IP): IP header validation, TTL decrement, fragmentation reassembly, routing lookup, local delivery or forwarding
- Further netfilter hooks (LOCAL_IN, FORWARD, etc.)

### Outgoing Packets (Transmit Path)

- The stack builds the IP packet → calls neighbor resolution (ARP/ND if needed) → builds Ethernet header
- Checksum offload, TSO (TCP Segmentation Offload), GSO (Generic Segmentation Offload)
- Driver queues the frame to the NIC’s TX ring → NIC transmits

### Summary Table of Common Protocols Handled at Driver/Early Stack Level

| EtherType / Protocol       | Handled by NIC driver / early kernel stack? | Notes |
|----------------------------|---------------------------------------------|-------|
| ARP (0x0806)               | Yes                                         | Always before firewall |
| IPv4 (0x0800)              | Yes                                         | All IPv4 packets |
| IPv6 (0x86DD)              | Yes                                         | All IPv6 packets |
| 802.1X/EAPOL (0x888E)      | Yes                                         | Authentication, often before IP |
| LLDP (0x88CC)              | Yes                                         | Link Layer Discovery |
| PTP (0x88F7)               | Yes                                         | Precision Time Protocol |
| Wake-on-LAN                | Yes (often in hardware)                     | Magic packet |
| Neighbor Discovery (ICMPv6)| Yes                                         | Handled in kernel before firewall |
| Any other valid Ethernet frame | Yes                                     | Even unknown types reach stack |

**Key point**: Essentially **every single Ethernet frame** that passes basic hardware checks is processed by the NIC driver and enters the kernel network stack **before** any firewall (netfilter) rules are applied. Firewall rules start at the netfilter hooks (PREROUTING being the earliest), which come **after** the driver and very early stack processing.

So, beyond ARP, the NIC driver and early kernel stack handle **all link-layer traffic** — normal IP traffic, ICMP, TCP, UDP, VLANs, control protocols, etc. — everything that arrives on the wire.
