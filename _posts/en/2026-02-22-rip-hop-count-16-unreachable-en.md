---
audio: false
generated: true
image: false
lang: en
layout: post
title: RIP Hop Count 16 Means Unreachable
translated: false
type: note
---

Question: In the RIP protocol, what does a hop count of 16 indicate?

Answer:

In the **Routing Information Protocol (RIP)**, a hop count of **16** indicates that the destination network is **unreachable**.

### Explanation:
- RIP is a distance-vector routing protocol that uses **hop count** as its metric to determine the best path to a destination.
- The maximum valid hop count in RIP is **15**. This means any destination that is 15 hops away or fewer is considered reachable.
- A hop count of **16** is defined as **infinity** in RIP terminology. When a router receives or calculates a route with a metric of 16, it treats that route as invalid or unreachable.
- This mechanism helps prevent routing loops and limits the size of the network that RIP can support (diameters larger than 15 hops are not supported).

Therefore, when a RIP router advertises a route with a metric of 16, it is effectively saying, "I do not have a valid path to this network."

References:

- [RFC 1058 - Routing Information Protocol](https://datatracker.ietf.org/doc/html/rfc1058)
- [Cisco Documentation on RIP Metrics](https://www.cisco.com/c/en/us/support/docs/ip/routing-information-protocol-rip/13730-3.html)
