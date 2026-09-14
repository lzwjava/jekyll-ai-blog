---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dual-Head PCIe to CPU Cable
translated: false
type: note
---

Question: What does "双头pcie转cpu线" mean?

Answer: "双头pcie转cpu线" literally translates to a **dual-head PCIe to CPU power cable** — more specifically, it refers to a **PCIe power adapter cable** that has:

- **双头 (dual-head)** — two connectors on one end (typically two 6-pin or 8-pin PCIe plugs)
- **转 (convert/to)** — adapting/converting
- **CPU线 (CPU cable)** — the other end uses a CPU/EPS 12V connector (the 8-pin or 4+4-pin connector normally used to power the CPU on a motherboard)

In practice, this is a cable that **takes power from your PSU's CPU/EPS 12V output and converts it into PCIe power**, used to feed power to graphics or compute cards like the Tesla P100 — since the P100 is a **data center card** that doesn't have a standard PCIe power plug but requires external power delivery through an adapter.

> **Side note:** The Tesla P100 is a professional compute card designed for AI/deep learning workloads. It has no display output and no gaming drivers, so unfortunately it **cannot be used for gaming** regardless of its raw compute power.
