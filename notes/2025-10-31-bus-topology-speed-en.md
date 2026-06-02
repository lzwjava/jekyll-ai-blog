---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Bus Topology Speed Limitations Explained
translated: false
type: note
---

### Bus Topology Limitations

You're spot on about the key features: bus topology uses a single shared cable (like coaxial in classic Ethernet setups) that's simple and cheap but vulnerable to collisions. When multiple devices try to transmit at the same time, signals overlap, causing "crashes" that require retransmission via protocols like CSMA/CD (Carrier Sense Multiple Access with Collision Detection).

#### Why ~100 Mbps Feels Like a Practical Limit (Even If the Cable Can Do More)

Cables themselves—whether copper (e.g., twisted-pair or coax) or optical/fiber—aren't the bottleneck here. Fiber optics can easily handle gigabits per second (or terabits in modern setups) over long distances with minimal loss. The real limits come from the **shared medium nature of the bus** and the physics/protocol overhead. Here's what caps speeds around 10–100 Mbps in traditional bus designs:

1. **Propagation Delay and Collision Detection**:
   - Signals take time to travel down the cable (e.g., ~5 ns/meter in coax or ~5 ns/km in fiber).
   - In a bus, every device must "listen" for collisions across the *entire network length*. The protocol defines a "slot time" (minimum time to detect a collision), which must be longer than the round-trip propagation delay (RTT) for the worst-case scenario (signal from one end to the other and back).
   - For 10 Mbps Ethernet (classic bus), max segment length was ~500m to keep RTT under 51.2 μs (512-bit slot time).
   - At 100 Mbps, the slot time shrinks proportionally (to ~5.12 μs), forcing max lengths down to ~100m. Beyond that, collisions go undetected, leading to endless errors.
   - Push to 1 Gbps? Slot time drops to ~0.512 μs, limiting segments to ~10–20m—impractical for a "bus" connecting multiple devices.

2. **Collision Overhead and Efficiency**:
   - CSMA/CD adds retries: a collision wastes bandwidth (up to 50% efficiency loss under heavy load).
   - Higher speeds amplify this—more frequent collisions mean more wasted cycles, reducing effective throughput.
   - Shared medium means total bandwidth is divided among all devices; no per-port dedication.

3. **Signal Integrity and Noise**:
   - While fiber resists electromagnetic interference (EMI) better than copper, bus setups still need precise timing for carrier sensing.
   - At high speeds, reflections, attenuation, or crosstalk on a shared line degrade signals faster, requiring more repeaters (which add delay and cost).

#### Why Switch Away from Bus for Faster Speeds?

This is why Ethernet evolved: after 100 Mbps (Fast Ethernet), they ditched pure bus for **star topology with switches** (e.g., 1 Gbps+). Switches create full-duplex point-to-point links—no collisions, full bandwidth per device, and longer runs. Bus is now rare outside niche/industrial uses.

If you're thinking of a specific setup (e.g., CAN bus in cars or old 10BASE-T), the principles are similar: protocol + physics > cable capability.

For deeper dives:
[Ethernet Bus Topology Basics](https://en.wikipedia.org/wiki/Bus_network)
[CSMA/CD Limitations](https://www.cisco.com/c/en/us/support/docs/lan-switching/ethernet/10561-3.html)
