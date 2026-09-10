---
audio: false
generated: true
image: false
lang: en
layout: post
title: JUSB3 Internal USB 2.0 Header
translated: false
type: note
---

Question: **What is JUSB3 on the MSI B150M PRO?**

Answer: **JUSB3 is an internal USB 2.0 header** on the motherboard.

Typically it is a **9-pin (2×5 with one pin missing)** connector used for front-panel USB 2.0 ports:

```text
JUSB3
┌─────────┐
│ • • • • •│
│ • • • •  │
└─────────┘
     ↑
   USB 2.0
```

You connect things such as:

* Front-case USB 2.0 ports
* Some internal USB 2.0 devices
* Certain AIO/controller devices

It is **not related to CPU/RAM POST**. For your current no-display debugging, you can leave **JUSB3 completely disconnected**.

If you upload a photo of the board, I can identify **JUSB3 and the other headers around it** on your exact B150M PRO.
