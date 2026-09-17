---
audio: false
generated: true
image: false
lang: en
layout: post
title: virtual-circuit service
translated: false
type: note
---

Question: What are **virtual-circuit service (虚电路服务)** and **datagram service (数据报服务)**, and what is the difference?

Answer:

They are two different ways a **packet-switched network** can provide communication.

### 1. Virtual-circuit service — 虚电路

Think of it like **making a phone call first, then talking**.

Before sending data:

```text
Host A                         Host B
  |                              |
  |--- setup virtual circuit --->|
  |<-- connection established ---|
  |                              |
  |====== packet 1 =============>|
  |====== packet 2 =============>|
  |====== packet 3 =============>|
  |                              |
  |-------- teardown ------------>|
```

The network first establishes a logical path:

```text
A → Router 1 → Router 2 → Router 3 → B
```

Each packet then follows that same virtual circuit.

Routers maintain **state** for the virtual circuit, typically something like:

```text
Incoming VC ID → outgoing VC ID
```

For example:

```text
Router 1:
VC 17 → port 3, VC 42
```

The packets don't necessarily contain the full destination address; they can carry a short **VC identifier**.

**Characteristics:**

* Connection setup required
* Network maintains connection state
* Packets normally follow the same logical path
* Packets arrive in order
* Can provide QoS/resource reservation more naturally
* Failure of the virtual circuit may require establishing another one

Examples historically include **X.25, Frame Relay, ATM**.

---

### 2. Datagram service — 数据报

Think of it like **sending independent letters through the postal system**.

No connection setup is required:

```text
A
├── packet 1 ──→ Router 1 → Router 2 → B
├── packet 2 ──→ Router 1 → Router 4 → B
└── packet 3 ──→ Router 5 → Router 4 → B
```

Every packet is treated independently.

A router essentially asks:

```text
"Where is the destination address?"
              ↓
        routing table
              ↓
"Which next hop should I use?"
```

So packet 1 and packet 2 **can potentially take different paths**.

The network itself generally doesn't maintain a per-connection circuit state.

**Characteristics:**

* No connection setup
* Each packet is independently routed
* Packets can take different paths
* Packets can arrive out of order
* Packets can be lost or duplicated
* Network is more flexible when topology changes

**IP is the classic example of a datagram network.**

---

### The key difference

|                   | Virtual circuit              | Datagram                |
| ----------------- | ---------------------------- | ----------------------- |
| Connection setup  | Yes                          | No                      |
| Network state     | Per-VC state                 | Mainly routing state    |
| Packet routing    | Same logical path            | Independently routed    |
| Packet order      | Usually preserved            | Not guaranteed          |
| Failure           | VC may need re-establishment | Packets can be rerouted |
| Address in packet | Often short VC ID            | Destination address     |
| Example           | ATM, X.25                    | IP                      |

The easiest mental model:

```text
Virtual circuit:

        ┌─────── same logical path ───────┐
A ──────R1────────R2────────R3─────────── B
       packet1     packet1     packet1
       packet2     packet2     packet2
       packet3     packet3     packet3


Datagram:

A ──packet1──→ R1 ──→ R2 ──→ B
 \
  ──packet2──→ R4 ──→ R3 ──→ B
 \
  ──packet3──→ R1 ──→ R5 ──→ B
```

### One subtle point

**Virtual circuit ≠ physical dedicated circuit.**

The "circuit" is **logical**, not a dedicated wire.

Multiple virtual circuits can share the same physical links:

```text
             ┌── VC A ──┐
A ── R1 ── R2 ── R3 ── B
             └── VC B ──┘
```

That's why it's called a **virtual** circuit.

Also, don't confuse this with **TCP**: TCP provides a connection-oriented transport service, but IP underneath is still a **datagram network**.

I can also show you how **virtual circuits vs datagrams map onto the OSI/network-layer concepts**, which makes this much easier to remember for networking exams.
