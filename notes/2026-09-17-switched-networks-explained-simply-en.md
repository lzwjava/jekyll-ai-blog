---
audio: false
generated: true
image: false
lang: en
layout: post
title: Switched Networks Explained Simply
translated: false
type: note
---

Question: **What is 交换式网络 (switched network)?**

Answer: **交换式网络 = switched network**. It is a network where **network switches decide where to forward each packet/frame**, instead of every device sharing the same communication medium.

The simplest example is an Ethernet LAN:

```text
PC A ──┐
PC B ──┤
PC C ──┼── [Ethernet Switch] ── Server
PC D ──┘
```

The switch learns MAC addresses:

```text
MAC A → port 1
MAC B → port 2
MAC C → port 3
Server → port 4
```

When A sends an Ethernet frame to the Server:

```text
A
 │
 │ frame: dst MAC = Server
 ▼
[Switch]
 │
 └──────────────► Server
```

The switch looks up the destination MAC in its **MAC address table** and forwards the frame only toward the appropriate port.

### Why "交换式"?

"交换" means **switching**: the network infrastructure dynamically chooses the path/port for traffic.

Compare it with an old **shared Ethernet / hub** network:

```text
             ┌── PC A
             │
PC B ── [Hub] ┼── PC C
             │
             └── PC D
```

If A sends something, a hub essentially broadcasts the electrical signal to all ports:

```text
A ──► Hub ──► B
         ├──► C
         └──► D
```

With a switch:

```text
A ──► Switch ─────────► C
```

So switched Ethernet gives you:

* **Dedicated collision domains** — each switch port is its own collision domain.
* **Full duplex** — modern Ethernet normally allows sending and receiving simultaneously.
* **Much better scalability**.
* **MAC-based forwarding** at Layer 2.
* Switches can also perform **VLANs**, STP, link aggregation, etc.

### Layer perspective

A typical switched Ethernet network looks like:

```text
Application       HTTP / SSH / ...
       ↓
Transport         TCP / UDP
       ↓
Network           IP
       ↓
Data Link         Ethernet
       ↓
Physical          electrical / optical signals
```

The **Ethernet switch primarily operates at Layer 2**:

```text
Ethernet frame
┌──────────┬──────────┬───────┐
│ dst MAC  │ src MAC  │ data  │
└──────────┴──────────┴───────┘
      │
      ▼
   Switch
      │
      ▼
MAC table → output port
```

There is also **packet switching at Layer 3** using routers, so "交换式网络" is a broader concept than just Ethernet switches. But when you see it in basic networking/computer-networking material, it usually means a **switched Ethernet network**.

A useful mental model is:

> **Hub = repeat everything.**
> **Switch = learn addresses and forward selectively.**
> **Router = connect different IP networks and choose routes.**
