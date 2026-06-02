---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: EIGRP Unicast Packets Requiring Acknowledgment
translated: false
type: note
---

Question: Which EIGRP packet is sent as a unicast and requires acknowledgment? A) Hello B) Update C) Query D) Reply

Answer:

The correct answer is **B) Update**, **C) Query**, and **D) Reply** — all three are sent as **unicast** and require **explicit acknowledgment**.
Only **A) Hello** does not fit the description.

Here’s a comprehensive breakdown of each EIGRP packet type regarding transmission method and acknowledgment:

| Packet Type | Transmission Method          | Requires Acknowledgment?                  | Notes |
|-------------|------------------------------|--------------------------------------------|-------|
| **Hello**   | Multicast (224.0.0.10)       | No                                         | Used for neighbor discovery and keepalive. Hellos are unreliable (no ACK required). |
| **Update**  | Unicast (or multicast when sending to multiple new neighbors) | Yes – acknowledged with an **ACK** packet | Carries routing information. When sent unicast (normal case after neighbor is established), it is reliable. |
| **Query**   | Unicast (to specific neighbors) | Yes – acknowledged with an **ACK** packet | Sent when a route is lost and EIGRP asks neighbors for alternative paths. Always reliable. |
| **Reply**   | Unicast (back to the originator of the Query) | Yes – acknowledged with an **ACK** packet | Response to a Query containing known path (or no path). Always reliable. |
| **ACK**     | Unicast                      | N/A (it is the acknowledgment itself)      | Simple packet with no data, just to confirm receipt of Update/Query/Reply. |

### Key Points on EIGRP Reliable Transport Protocol (RTP)

- EIGRP uses its own **Reliable Transport Protocol (RTP)** to guarantee delivery of certain packets.
- Packets that contain routing information or control information that affects the routing table (**Update, Query, Reply**) are sent **reliably** → they are always unicast (except initial Updates to new neighbors) and require an **ACK**.
- **Hello** and **ACK** packets are sent **unreliably** (no acknowledgment needed).
- The ACK is a separate EIGRP packet (opcode 5) with no data — just a sequence number acknowledgment.

### Why the question can be tricky

Many practice questions expect **Update** as the single answer because it is the most common reliable unicast packet. However, technically **Update, Query, and Reply** all meet the criteria of being sent as unicast and requiring acknowledgment.

If the question forces a single choice and comes from Cisco’s official material (e.g., CCNP ENARSI), the historically most common expected answer is **B) Update**.

References:

- [Cisco EIGRP Packet Types](https://www.cisco.com/c/en/us/support/docs/ip/enhanced-interior-gateway-routing-protocol-eigrp/13669-1.html)
- [EIGRP Reliable Transport Protocol (RFC 7868)](https://datatracker.ietf.org/doc/html/rfc7868)
