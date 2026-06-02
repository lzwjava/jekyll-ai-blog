---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Circuit Switching vs Packet Switching
translated: false
type: note
---

Question: How do traditional telephone networks work, and why couldn't the internet be built directly on top of that infrastructure using its switching method?

Answer:

### How Traditional Telephone Networks Work

Traditional telephone networks, known as the **Public Switched Telephone Network (PSTN)** or Plain Old Telephone Service (POTS), operate using **circuit switching**.

- When a call is initiated, the network establishes a **dedicated physical path** (circuit) between the caller and recipient through a series of centralized **switching centers** (also called central offices or exchanges).
- This path is reserved exclusively for the duration of the call, even during silences, ensuring constant bandwidth and low latency for real-time voice transmission.
- The infrastructure primarily consists of copper wires, fiber optics, trunk lines, and switching nodes that route the analog (or later digital) voice signals.
- Once the call ends, the circuit is released.

This design made the network reliable for voice but vulnerable: destroying key switching centers could isolate large areas or cripple the system, as there was no automatic rerouting around failures.

### Why the Internet Couldn't Be Built Directly on Top of Circuit-Switched Telephone Networks

The internet was designed for **data communication** (not real-time voice), requiring different priorities: efficiency, resilience, scalability, and support for bursty traffic (e.g., file transfers, emails). Building it on circuit switching would have been impractical for several reasons:

1. **Inefficiency for Data Traffic**:
   - Data transmission is often "bursty" — large amounts sent intermittently, with long idle periods.
   - Circuit switching wastes bandwidth by holding a dedicated path open during idle times, making it costly and inefficient for non-continuous data.

2. **Lack of Resilience**:
   - Circuit-switched networks rely on centralized switches; failure of a key node disrupts connections with no automatic recovery.
   - Early internet designers (influenced by Cold War needs via ARPANET) prioritized survivability: the network had to route around damage (e.g., nuclear attack). Packet switching allows this naturally.

3. **Poor Scalability and Resource Sharing**:
   - Dedicated circuits limit simultaneous connections and don't allow multiple users to efficiently share bandwidth.
   - Data networks need to connect diverse computers with varying speeds and protocols, which circuit switching couldn't handle flexibly.

Instead, the internet uses **packet switching** (pioneered in ARPANET, 1969):

- Data is broken into small **packets**, each with header information (source, destination, sequence).
- Packets travel independently over shared links, routed dynamically by routers.
- They can take different paths, be reassembled at the destination, and rerouted if links fail.
- This enables efficient bandwidth use, fault tolerance, and scalability.

**Historical Context**: ARPANET chose packet switching over circuit switching for resource sharing among computers, cost-effectiveness, and robustness (ideas from Paul Baran, Donald Davies, and others). While dial-up modems later used phone lines for access (tunneling data over circuits), the core internet protocol (TCP/IP) is packet-based, not circuit-based.

In summary, circuit switching excels at constant-bit-rate voice but is rigid and wasteful for data. Packet switching's flexibility made the modern internet possible.

References:

- https://en.wikipedia.org/wiki/Public_switched_telephone_network
- https://en.wikipedia.org/wiki/Packet_switching
- https://en.wikipedia.org/wiki/ARPANET
- https://www.nextiva.com/blog/what-is-pstn.html
- https://ethw.org/Packet_Switching
- https://en.wikipedia.org/wiki/Dial-up_Internet_access
