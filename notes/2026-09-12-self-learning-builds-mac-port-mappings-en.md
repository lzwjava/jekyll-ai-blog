---
audio: false
generated: true
image: false
lang: en
layout: post
title: Self-learning builds MAC-port mappings
translated: false
type: note
---

Question: **How does an Ethernet switch use a self-learning algorithm to construct a network map?**

Answer: The key distinction is: **a normal L2 switch does not actually construct a full topology map.** Its self-learning algorithm constructs a **MAC address → switch port mapping**, usually called the **MAC/CAM table**.

### 1. The core algorithm

Suppose we have:

```text
        Switch
      /    |    \
    Port1 Port2 Port3
     PC-A  PC-B  PC-C
```

Initially:

```text
MAC table = {}
```

When `PC-A` sends a frame:

```text
src = AA:AA:AA
dst = BB:BB:BB
```

the switch receives it on `Port1`.

The learning rule is essentially:

```python
mac_table[src_mac] = ingress_port
```

So:

```text
AA:AA:AA -> Port1
```

Then the switch looks up the destination:

```python
if dst_mac in mac_table:
    forward(dst_mac, mac_table[dst_mac])
else:
    flood_to_all_ports_except_ingress()
```

So after some traffic:

```text
MAC Table
----------------
AA:AA:AA -> Port1
BB:BB:BB -> Port2
CC:CC:CC -> Port3
```

That's the "self-learning" part.

---

### 2. Why does this work?

Because Ethernet frames contain both:

```text
+----------------+----------------+---------+
| Destination MAC| Source MAC     | Payload |
+----------------+----------------+---------+
```

Every frame gives the switch one piece of information:

> **"I saw MAC X coming from port Y."**

The switch doesn't need configuration.

Mathematically, you can think of it as learning a function:

$$
f: MAC \rightarrow Port
$$

with observations:

$$
(MAC_i, Port_j)
$$

and updating:

$$
f(MAC_i) \leftarrow Port_j
$$

If a machine moves from one port to another, the next frame updates the mapping:

```text
AA:AA:AA -> Port1

# machine moves

AA:AA:AA -> Port4
```

The old entry is replaced.

There is usually also an **aging timer**, so inactive MAC entries eventually disappear.

---

### 3. But this isn't a network topology map

Consider:

```text
       Switch A
       /       \
     PC        Switch B
                /   \
              PC    Switch C
```

Switch A might learn:

```text
AA:AA:AA -> Port1     # PC
BB:BB:BB -> Port2     # Switch B / devices behind it
```

But it doesn't inherently know:

```text
Switch A
   |
Switch B
   |
Switch C
```

because from A's perspective, multiple downstream devices can simply appear behind **Port2**.

So MAC learning gives you:

```text
MAC → local ingress port
```

not:

```text
Switch → Switch → Switch → Host
```

---

### 4. How do network systems actually construct a topology map?

They combine several protocols.

**LLDP** is particularly important.

A switch periodically sends something like:

```text
Switch A, Port 3
        ↓
      LLDP
        ↓
Switch B, Port 17
```

Switch B receives the LLDP packet and learns:

```text
neighbor:
    local_port = 17
    remote_device = Switch A
    remote_port = 3
```

Now a controller can construct:

```text
Switch A:3 ───── Switch B:17
```

Do this across every switch and you get a graph:

```text
             ┌─────────────┐
             │   Switch A  │
             └──────┬──────┘
                    │
              A:3 ──┴── B:17
                    │
             ┌──────┴──────┐
             │   Switch B  │
             └───┬─────┬───┘
                 │       │
                PC      Switch C
```

So conceptually:

```text
MAC learning
     ↓
MAC → Port information

LLDP
     ↓
Port → Neighbor information

STP
     ↓
Layer-2 topology / loop prevention

ARP / DHCP / routing information
     ↓
IP → MAC → interface relationships

     ↓
Network controller
     ↓
Graph / topology map
```

---

### 5. The interesting part: the switch is doing online learning

This is actually a very simple **online algorithm**, not "AI/ML".

Pseudo-code for a simplified switch:

```python
table = {}

def receive(frame, ingress_port):
    src = frame.src
    dst = frame.dst

    # self-learning
    table[src] = ingress_port

    # forwarding
    if dst in table:
        egress_port = table[dst]

        if egress_port != ingress_port:
            send(frame, egress_port)
    else:
        flood(frame, except_port=ingress_port)
```

You can view the sequence as:

```text
t0:
{}

t1:
AA -> P1

t2:
AA -> P1
BB -> P2

t3:
AA -> P1
BB -> P2
CC -> P3
```

No centralized knowledge is required.

This is one of the beautiful things about Ethernet: **the network discovers reachability from traffic itself.**

One important caveat: if by "self-learning" you mean **how systems like Google Maps/Internet backbone monitoring automatically infer the entire network topology**, that's a different problem—closer to **distributed graph reconstruction from LLDP/CDP, routing protocols, traceroute, SNMP, flow data, and probabilistic inference**. I can walk through that algorithmically too, including how you'd build the topology graph from raw packets.
