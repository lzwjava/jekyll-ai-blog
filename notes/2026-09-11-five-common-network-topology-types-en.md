---
audio: false
generated: true
image: false
lang: en
layout: post
title: Five Common Network Topology Types
translated: false
type: note
---

Question: What is a network topology, and what are the five common types?

Answer:

**Network topology** = the **structure/layout of a computer network** — how devices (nodes) are connected to each other.

There are **5 classic topology types**:

| Type     | Structure                              | Main idea                                 |
| -------- | -------------------------------------- | ----------------------------------------- |
| **Bus**  | `A — B — C — D`                        | All devices share one backbone cable      |
| **Star** | `A ↘`<br>`B → Hub/Switch ← C`<br>`D ↗` | Every device connects to a central device |
| **Ring** | `A → B → C → D → A`                    | Devices form a closed loop                |
| **Mesh** | `A ↔ B`<br>`↕ ╲ ↗`<br>`C ↔ D`          | Devices have multiple interconnections    |
| **Tree** | `Root`<br>`↙ ↓ ↘`<br>`A B C`<br>`↙ ↘`  | Hierarchical combination of stars         |

### 1. Bus topology

```text
A    B    C    D
|    |    |    |
================
    backbone
```

One shared communication medium.

* Cheap and simple
* One cable failure can affect the whole network
* Collisions were a major issue with old Ethernet

### 2. Star topology

```text
       A
       |
B ---- SW ---- C
       |
       D
```

Modern Ethernet LANs are typically physically **star-shaped** around a switch.

* Easy to manage
* One endpoint cable fails → usually only that device is affected
* Central switch becomes an important failure point

### 3. Ring topology

```text
A → B
↑   ↓
D ← C
```

Each device connects to two neighbors.

* Predictable path
* A break can disrupt the ring unless there is redundancy
* Historically used in technologies such as Token Ring

### 4. Mesh topology

```text
A -------- B
|\        /|
| \      / |
|  \    /  |
|   \  /   |
C -------- D
```

Nodes have multiple paths to other nodes.

* Excellent redundancy
* More expensive/complex
* Common conceptually in **WANs, routing networks, wireless mesh networks**

A **full mesh** with `n` nodes has:

$$
E = \frac{n(n-1)}{2}
$$

links.

For 5 nodes:

$$
E = \frac{5(4)}2 = 10
$$

### 5. Tree topology

```text
             Core
          /    |    \
        SW1   SW2   SW3
       /  \   / \   /  \
      A    B C   D E    F
```

It's hierarchical: **root → branches → devices**.

This is very common in enterprise networks because it scales much better than a giant flat network.

### The key distinction

Don't confuse **physical topology** with **logical topology**.

For example, an Ethernet network can be physically:

```text
PC ─┐
PC ─┼─ Switch
PC ─┘
```

which is **star topology**, while the logical behavior is determined by Ethernet switching and routing.

For your networking exam, the easy mnemonic is:

> **Bus, Star, Ring, Mesh, Tree**

I can also show you **how these five topologies map to real Ethernet/Wi-Fi networks and what failure happens when one cable/device dies**.