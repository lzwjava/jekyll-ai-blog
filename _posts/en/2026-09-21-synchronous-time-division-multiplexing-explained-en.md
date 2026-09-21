---
audio: false
generated: true
image: false
lang: en
layout: post
title: Synchronous Time-Division Multiplexing Explained
translated: false
type: note
---

Question: What is **同步时分多路复用**?

Answer:

**同步时分多路复用 = Synchronous Time-Division Multiplexing (Synchronous TDM)**.

The core idea is extremely simple:

> **Multiple data streams share one physical link by taking turns in fixed, pre-assigned time slots.**

Think of it as:

```text
A ──┐
B ──┼──> [ MUX ] ──> one physical link ──> [ DEMUX ] ──> A
C ──┘                                                   ├─> B
                                                        └─> C
```

Suppose each input generates 1 byte per cycle:

```text
Time:    | t0 | t1 | t2 | t3 | t4 | t5 | ...
         +----+----+----+----+----+----+
Channel: | A  | B  | C  | A  | B  | C  |
         +----+----+----+----+----+----+
```

The multiplexer sends:

```text
A0 B0 C0 A1 B1 C1 A2 B2 C2 ...
```

The receiver already knows:

```text
slot 0 → A
slot 1 → B
slot 2 → C
```

so it can demultiplex the stream.

### Why "同步"?

Because the **time slots are fixed and synchronized**.

Even if B has nothing to send:

```text
A0 B0 C0 A1 B1 C1
   ↑
   B's slot still exists
```

B's slot is simply empty/idle.

That's the key distinction from **统计时分多路复用 (Statistical TDM)**:

```text
Synchronous TDM:

A B C A B C A B C
| | | | | | | | |
fixed slots


Statistical TDM:

A C A A C B C
| | | | | | |
dynamic slots
```

Statistical TDM gives slots to whoever currently has data, so it uses bandwidth more efficiently when traffic is bursty.

### A concrete telecom example

Imagine 4 voice channels, each requiring 64 kbps:

```text
Channel A: 64 kbps
Channel B: 64 kbps
Channel C: 64 kbps
Channel D: 64 kbps
-------------------
             256 kbps
```

With synchronous TDM, you could create a frame:

```text
┌───────┬───────┬───────┬───────┐
│   A   │   B   │   C   │   D   │
└───────┴───────┴───────┴───────┘
    1       2       3       4
```

Every frame contains one slot for each channel.

So the physical link carries:

```text
[A][B][C][D] [A][B][C][D] [A][B][C][D] ...
```

The receiver doesn't need an address in every slot. **Position itself identifies the channel.**

That's why synchronization is fundamental: if the receiver loses frame/slot alignment, it could interpret:

```text
A B C D
```

as:

```text
B C D A
```

and every channel gets garbage.

### One-line mental model

> **Synchronous TDM = "I reserve a fixed seat for every stream in every frame, whether that stream has data or not."**

This is fundamentally different from packet multiplexing, where each packet carries enough information to determine where it should go.
