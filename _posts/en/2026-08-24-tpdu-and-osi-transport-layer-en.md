---
audio: false
generated: true
image: false
lang: en
layout: post
title: TPDU and OSI Transport Layer
translated: false
type: note
---

Question: What is TPDU, and what is the broader context of what we are discussing?

Answer:

## TPDU = Transport Protocol Data Unit

It is the **packet/message unit** used at the **Transport Layer (Layer 4)** of the **OSI model**.

### Big Picture: Where Does This Fit?

```
OSI Model
─────────────────────────────
Layer 7 │ Application
Layer 6 │ Presentation
Layer 5 │ Session
Layer 4 │ TRANSPORT  ← We are here
Layer 3 │ Network
Layer 2 │ Data Link
Layer 1 │ Physical
─────────────────────────────
```

### What is a "PDU"?

Every OSI layer has its own name for its data unit:

| Layer | PDU Name |
| --- | --- |
| Transport (L4) | **TPDU** (Transport Protocol Data Unit) |
| Network (L3) | Packet |
| Data Link (L2) | Frame |
| Physical (L1) | Bit |

So **TPDU** is simply what a **Transport Layer packet is called** in the OSI world.

---

### What Were We Actually Discussing?

Specifically, we were looking at the **header structure of a TPDU** defined by **ISO 8073 / ITU-T X.224** (the OSI connection-oriented transport protocol), and one particular header field:

| Field | Role |
|---|---|
| **LI** (Length Indicator) | Tells the receiver **how long the TPDU header is**, in bytes |

The question was: given `LI = 11111100₂ = 252`, what is the total header length? → **254 bytes**, because `LI_value + 2 = 254`.

---

### Is This Related to TCP?

Not directly. This is the **OSI transport protocol**, which is a **different standard** from TCP/IP. In practice, TCP/IP "won" the internet — but OSI transport concepts (including TPDU) are still taught in **computer networking courses** as foundational theory.

---

References:

- [OSI Model – Cloudflare Learning](https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/)
- [ITU-T X.224 – Transport Protocol Specification](https://www.itu.int/rec/T-REC-X.224/en)
