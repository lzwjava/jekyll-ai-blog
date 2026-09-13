---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dual 8-Pin GPU Power Connector Guide
translated: false
type: note
---

**Question:** What is a dual 8-pin GPU power connector, and how do you properly use it?

**Answer:**

A "dual 8-pin" (双8针) power setup means your GPU has **two 8-pin PCIe power sockets** that both need to be connected to your PSU (power supply). Here's everything you need to know:

---

### Why Two 8-Pin Connectors?

Each 8-pin PCIe connector is rated to supply up to **150W**. So a GPU with two 8-pin connectors has a power requirement roughly in the **151–300W** range. Mid-to-high-end GPUs like RTX 3070/3080 series commonly use this configuration.

---

### How to Connect Them

You have two main options:

**Option A — Two separate cables (recommended for high-power GPUs)**

- Run **one cable per 8-pin socket** from your PSU.
- Plug each cable into a separate PCIe port on the PSU.
- This is not only safe but ideal — there have been documented issues with high-power GPUs (like the RX 5700 XT) experiencing power delivery problems when using a single pigtail cable for both connectors.

**Option B — One pigtail (Y-split) cable**

- A single cable from the PSU splits into **two 8-pin heads** at the GPU end.
- If your GPU's power requirement is in the 151–300W range, a single pigtail cable is sufficient and you won't need two individual cables.
- Not ideal for very power-hungry cards (e.g., 300W+), since both connectors share one cable run.

---

### Important Warnings

- Don't use random third-party PCIe cables — there is no universal pinout standard across PSU brands. Using the wrong cable for your PSU can cause an electrical short. Always use cables made for your specific PSU model.
- Make sure the connector **clicks and fully seats** into the GPU. Partially seated 8-pin connectors have caused melted connectors on high-draw cards.
- CPU 8-pin and PCIe 8-pin connectors **look almost identical** but are wired differently — never use a CPU cable on a GPU slot.

---

### Quick Visual Guide

```
PSU PCIe port 1 ──→ [8-pin cable] ──→ GPU socket 1
PSU PCIe port 2 ──→ [8-pin cable] ──→ GPU socket 2
```

Or with pigtail:

```
PSU PCIe port 1 ──→ [Y-split cable] ──┬──→ GPU socket 1
                                       └──→ GPU socket 2
```

**References:**

- [Tom's Hardware – Dual 8-pin connection discussion](https://forums.tomshardware.com/threads/connecting-a-gpu-with-dual-8-pin-connectors-to-psu.2648670/)
- [Corsair – Individual 8-pin vs Pigtail Connectors](https://www.corsair.com/us/en/explorer/diy-builder/power-supply-units/individual-8-pin-vs-pigtail-connectors-for-gpus/)
- [GPU Mag – GPU Power Connectors Explained](https://www.gpumag.com/gpu-power-connectors-explained/)
