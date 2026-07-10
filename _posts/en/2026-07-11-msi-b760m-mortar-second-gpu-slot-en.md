---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI B760M Mortar Second GPU Slot
translated: false
type: note
---

Question: How to use the second GPU slot on MSI MAG B760M Mortar WiFi when the lower PCIe slot is blocked by an adapter/cable?

Answer:

Your motherboard technically has two PCIe slots, but the physical layout is the limitation.

MSI MAG B760M Mortar WiFi DDR5 layout:

```
CPU
 |
 |  PCIe x16 (top slot)
 |  =======================
 |        GPU (RTX 4070 / MI50)
 |
 |  M.2 / chipset area
 |
 |  PCIe x16 physical (bottom slot, x4 electrical)
 |  =======================
 |
 |  PCI cards / adapters
```

The problem is usually:

* Your first GPU is **2-3 slot thick**
* MI50 is a **server blower card**, often ~2 slots
* The lower PCIe slot is very close
* M.2 adapter / USB adapter / capture card / cable blocks airflow or physical insertion

This is a common mATX problem.

Solutions:

### Option 1 — PCIe riser cable (best solution)

Use a PCIe x16 riser:

```
Motherboard bottom PCIe slot
          |
          |
     PCIe riser cable
          |
          |
      GPU mounted vertically
```

Example:

```
[CPU]
 |
[RTX 4070]
 |
-----------------
bottom PCIe
 |
riser
 |
MI50 outside case
```

For AI workloads this is fine because the bottom slot is only PCIe 4.0 x4 anyway. You are not doing gaming SLI.

For LLM inference/training:

* GPU bandwidth matters less than VRAM capacity
* PCIe x4 is often acceptable

---

### Option 2 — Move the adapter

If the adapter is:

* WiFi card
* USB expansion
* sound card
* NVMe PCIe adapter

move it.

Your motherboard already has:

* WiFi 6E
* multiple USB ports
* M.2 slots

You may not need the PCIe adapter.

---

### Option 3 — Use a larger ATX motherboard

If your goal is:

```
RTX 4070
+
AMD MI50
+
maybe another GPU later
```

mATX is the wrong form factor.

A full ATX board gives:

```
GPU 1
(empty spacing)
GPU 2
(empty spacing)
GPU 3
```

Examples:

* Z790 ATX boards
* W790 workstation boards

---

### Option 4 — Remove the case slot limitation

Sometimes the motherboard has space but the case bracket prevents the second GPU.

Check:

* number of expansion slots on the case
* GPU thickness
* PSU shroud blocking the bottom area

---

For your specific setup:

```
i9-13900KF
MSI B760M Mortar WiFi
RTX 4070
AMD MI50
```

I would do:

```
Top PCIe x16:
RTX 4070

Bottom PCIe x4:
PCIe riser cable
        |
        MI50 outside/vertical mount
```

This is actually a very normal AI workstation setup. The MI50 does not need PCIe x16 for most LLM experiments; the **16GB HBM2 memory** is the valuable part.
