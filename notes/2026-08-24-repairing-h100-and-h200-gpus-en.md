---
audio: false
generated: true
image: false
lang: en
layout: post
title: Repairing H100 and H200 GPUs
translated: false
type: note
---

**Question:** How do datacenter technicians repair H100, H200, and similar high-end GPU cards?

**Answer:**

Repairing these cards in a datacenter involves a layered approach — most real repair happens through diagnostics and component swap-outs, not board-level soldering. Here's how it works in practice:

---

### 1. Diagnostics First

Before touching hardware, techs run software tools to confirm the fault:

- NVIDIA provides `nvidia-healthmon`, which outputs a troubleshooting report addressing common problems and suggests possible solutions, listed from most to least likely. If no software or configuration issue is found, the **NVIDIA Field Diagnostic** is run — a comprehensive Linux-based tool that confirms GPU numerical engine integrity, data transfer integrity, and full memory address space coverage.

---

### 2. Field-Replaceable Units (FRUs) — The Primary Repair Method

Datacenters don't do chip-level repair. The standard model is:

- A **Field-Replaceable Unit (FRU)** is a circuit board or component that can be removed and replaced by a technician on-site without sending the whole system to a repair facility. The defective unit is found through standard troubleshooting, removed, and either discarded or shipped back to the factory. The FRU scheme is typically the most cost-effective approach for maintaining complex systems.

- NVIDIA's own RMA checklist instructs techs to first **reseat** the FRU module, then **swap it with a known-good FRU** to isolate whether the fault is in the module or the slot itself.

---

### 3. Physical Replacement — What It Actually Involves

For systems like the DGX H100/H200:

- GPU and heatsink removal must be executed by a **trained technician**. The procedure requires two people and a lifting device capable of supporting up to 400 lb (181 kg). Technicians must inspect all connectors and sockets — GPUs with damaged connectors or debris in sockets should not be reused.

- When removing the GPU baseboard, technicians unfasten Torx T15 screws in a specific sequence using a **torque screwdriver set to 0.6 newton-meters (5.3 inch-pounds)**, carefully remove GPUs onto a flat, static-protective surface, and keep handles attached if the unit is being shipped for RMA.

- For network card replacements, the procedure involves labeling all cables, sliding out the motherboard tray, replacing the card, sliding it back in, reconnecting all cables by label, powering up, testing — and then shipping the failed unit back to NVIDIA Enterprise Support.

---

### 4. RMA — What Happens When a Card Is Truly Dead

When a component needs repair beyond field replacement, technicians contact **NVIDIA Enterprise Support** to obtain an RMA number. Only NVIDIA-supplied replacement components are used. The failed unit is returned to NVIDIA for analysis.

---

### 5. The Edge Case: Independent Board-Level Repair

Some third-party technicians do go deeper. A notable real example:

- A repair technician fixed a dead $30,000 H200 with a damaged 12VHPWR connector by cutting and trimming replacement pins and **soldering** them onto the H200's power connector. When a PCB short prevented power-on, they bypassed the sense pins entirely by **disconnecting the resistor** connecting the sense pins to the card — restoring function.

This kind of component-level PCB work is rare in datacenters (it voids warranties and requires expertise) but it does happen in the independent repair ecosystem.

---

### Summary

| Repair Level | Who Does It | Method |
|---|---|---|
| Software/config issue | In-house ops | nvidia-healthmon, driver reinstall |
| Component swap (FRU) | Trained DC tech | Hot/cold swap, torque tools, ESD precautions |
| Full card failure | NVIDIA via RMA | Return & replace |
| Board-level repair | Specialist repair shops | Soldering, resistor bypass (rare, voids warranty) |

---

**References:**
- [NVIDIA DGX H100/H200 Service Manual](https://docs.nvidia.com/dgx/dgxh100-service-manual/introduction.html)
- [NVIDIA RMA Process Guide](https://docs.nvidia.com/deploy/rma-process/index.html)
- [NVIDIA RMA Checklist](https://network.nvidia.com/support/rma-checklist/)
- [Lenovo H100/H200 GPU Removal Docs](https://pubs.lenovo.com/sr780a-v3/remove_the_h100_gpu_baseboard)
- [Tom's Hardware — H200 Board-Level Repair](https://www.tomshardware.com/pc-components/gpus/busted-12vhpwr-connector-sidelines-usd30-000-h200-hopper-gpu-repair-technician-saves-the-data-center-day-by-fixing-power-port)
- [Field-Replaceable Unit — TechTarget](https://www.techtarget.com/searchdatacenter/definition/field-replaceable-unit)