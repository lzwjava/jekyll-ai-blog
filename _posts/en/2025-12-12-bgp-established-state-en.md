---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: BGP Established State Explanation
translated: false
type: note
---

Question: Which BGP neighbor state indicates that a TCP three-way handshake has been completed?
A) Idle
B) Connect
C) Active
D) Established

Answer:

The correct answer is **D) Established**.

### Comprehensive Explanation of BGP Neighbor States

BGP forms neighbor relationships (peering) over a reliable TCP connection (port 179). Before exchanging any BGP routing information, the two routers must first establish a TCP session. The BGP finite-state machine (FSM) tracks the progress of this neighbor relationship through six main states:

| State       | Description                                                                                              | TCP Session Status                          |
|-------------|----------------------------------------------------------------------------------------------------------|---------------------------------------------|
| **Idle**    | Initial state. BGP is waiting for a Start event (manual or automatic). No resources are allocated yet. | No TCP connection attempted                 |
| **Connect** | BGP is waiting for the TCP three-way handshake to complete. The local router has initiated a TCP connection to the neighbor. | TCP SYN sent, waiting for SYN-ACK           |
| **Active**  | TCP connection attempt failed (e.g., timed out in Connect state). BGP is actively trying to establish TCP by repeatedly initiating new connections. | Trying to establish TCP (re-sending SYN)    |
| **OpenSent**| TCP three-way handshake is complete. BGP has sent an OPEN message and is waiting for an OPEN from the peer. | TCP session fully established               |
| **OpenConfirm** | Received a valid OPEN message from the peer, sent a KEEPALIVE, and is waiting for a KEEPALIVE from the peer. | TCP session fully established               |
| **Established** | Received the peer’s KEEPALIVE. The BGP peering is fully up. UPDATE, KEEPALIVE, and NOTIFICATION messages can now be exchanged. | TCP session fully established               |

### Key Point

The TCP three-way handshake (SYN → SYN-ACK → ACK) must be successfully completed before BGP can move beyond the Connect/Active states. This happens when the FSM transitions into **OpenSent**. Therefore, from **OpenSent** onward (OpenSent → OpenConfirm → Established), the TCP session is already fully established.

However, the question specifically asks for the state that **indicates** the TCP three-way handshake has been completed and the BGP session is fully operational for routing exchange. That is the **Established** state—the only state where the BGP peering is considered “up” and routing information is actually being exchanged.

### Quick Summary

- **Idle → Connect → (possibly Active)**: Trying to complete the TCP handshake
- **OpenSent → OpenConfirm → Established**: TCP handshake already completed
- **Established** = BGP neighbor is fully up (TCP + BGP session successful)

Thus, **D) Established** is the definitive state confirming that the TCP three-way handshake has been completed and the BGP session is operational.

References:

- [RFC 4271 – A Border Gateway Protocol 4 (BGP-4)](https://www.rfc-editor.org/rfc/rfc4271.html)
- [Cisco BGP Finite State Machine](https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/13753-25.html)
