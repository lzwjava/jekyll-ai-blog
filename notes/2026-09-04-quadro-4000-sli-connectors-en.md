---
audio: false
generated: true
image: false
lang: en
layout: post
title: Quadro 4000 SLI Connectors
translated: false
type: note
---

Question: What are the two connectors on the top edge of this Quadro 4000?

Answer: Those are **not display outputs**. They are **SLI connectors**.

On the **Quadro 4000 (Fermi, GF100)**:

* **Top-edge connector(s)** → **SLI / Quadro SLI interface**, used to connect two professional GPUs for multi-GPU workloads.
* **Rear bracket** → the actual display outputs:

  * **2 × DisplayPort**
  * **1 × DVI-I**

The connector you see in your photo is the **SLI connector**, carrying high-speed GPU-to-GPU communication. It isn't something you connect to the motherboard's PCIe slot.

One interesting detail: **Quadro cards can use SLI differently from GeForce cards**, particularly for professional visualization and synchronized/multi-display workflows.

If you want, I can also map **every connector and major component on this Quadro 4000 PCB** for GPU-repair learning.
