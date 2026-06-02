---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: EIGRP Reply Packet Characteristics
translated: false
type: note
---

Question: Which EIGRP packet is sent as a unicast and requires acknowledgment?
A) Hello
B) Update
C) Query
D) Reply

Answer:

**D) Reply**

In EIGRP, the Reply packet is always sent as a unicast to the router that originated the Query. Like Update and Query packets, Reply packets are transmitted reliably via EIGRP's Reliable Transport Protocol (RTP), which requires an explicit acknowledgment (ACK) from the recipient.

- **Hello** packets are multicast (or unicast in specific cases like static neighbors) and unreliable—no acknowledgment required.
- **Update** packets can be multicast or unicast but are reliable when sent.
- **Query** packets are typically multicast (retransmitted as unicast if needed) and reliable.
- Only **Reply** consistently matches both criteria: always unicast and always requires acknowledgment.

References:

- <https://www.computernetworkingnotes.com/ccna-study-guide/eigrp-packet-types-and-rtp-protocol.html>
- <https://www.geeksforgeeks.org/computer-networks/types-of-eigrp-packet-in-computer-network/>
- <https://ipcisco.com/lesson/eigrp-packet-types-and-neighbourship-ccnp/>
- <https://www.cisco.com/c/en/us/support/docs/ip/enhanced-interior-gateway-routing-protocol-eigrp/13669-1.html>
