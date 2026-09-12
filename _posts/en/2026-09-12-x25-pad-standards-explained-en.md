---
audio: false
generated: true
image: false
lang: en
layout: post
title: X.25 PAD Standards Explained
translated: false
type: note
---

Question: What do **CCITT, X.3, X.28, and X.29** mean?

Answer: These are **ITU-T standards related to packet-switched data networks**, especially **X.25** networks.

| Standard  | Meaning / Role                                                                                                                                                              |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **CCITT** | Former name of **ITU-T** — *International Telegraph and Telephone Consultative Committee*. It published telecommunications standards before 1993.                           |
| **X.3**   | Defines the **Packet Assembler/Disassembler (PAD) parameters**. It specifies how a PAD behaves when connecting ordinary character-mode terminals to an X.25 packet network. |
| **X.28**  | Defines the **DTE–PAD interface** for an **asynchronous character-mode terminal**. In practice, it specifies how a terminal talks to the PAD.                               |
| **X.29**  | Defines the **DTE–PAD interface for PAD control/information**, especially how a remote host/DTE can communicate with and control a PAD.                                     |

### The easiest way to remember them

Think of an old terminal connected to an X.25 network:

```text
Character terminal
       │
       │ X.28
       ▼
     ┌─────┐
     │ PAD │
     └─────┘
       │
       │ X.25
       ▼
Packet-switched network
       │
       ▼
     Host/DTE
       ▲
       │
      X.29
```

And **X.3** describes the **configuration/behavior parameters inside the PAD**.

So:

> **X.3 = PAD parameters**
> **X.28 = terminal ↔ PAD**
> **X.29 = host/DTE ↔ PAD**
> **X.25 = packet network protocol**

**CCITT** is the organization that originally standardized these; today, you'd generally see **ITU-T** instead.

I can also explain **PAD + X.25 with a concrete Telnet-like login example**, which makes X.3/X.28/X.29 much easier to understand.
