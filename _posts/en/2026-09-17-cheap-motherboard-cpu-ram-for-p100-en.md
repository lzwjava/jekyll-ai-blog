---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cheap Motherboard CPU RAM for P100
translated: false
type: note
---

**Question:** What cheap motherboard, CPU, and RAM do you recommend to run the Nvidia P100, especially given the "PCI OUT OF RESOURCES" BIOS error?

**Answer:**

The P100 is a data-center passive-cooled GPU with a 250 W TDP and a full-size dual-slot PCIe Gen 3 x16 card. The "PCI OUT OF RESOURCES" error is specifically a BIOS/UEFI resource-map problem, so your platform **must** support **Above 4G Decoding** in BIOS. Consumer boards from ~2018 onward almost universally have it. Below are two budget paths — one AMD, one used-server Intel — both proven to work with data-center GPUs.

---

### Path A — AMD AM4 (Best bang-for-buck new/used, ~$150–250 total platform)

**Motherboard**

Most AM5/AM4 boards like the MSI MAG B550 Tomahawk and the ASRock B550 Steel Legend support Above 4G Decoding and even unbuffered ECC memory — a significant advantage for budget AI workstations. For the P100 specifically, the B550 chipset is the sweet spot:

| Board | Why it fits | Approx. used price |
|---|---|---|
| **ASRock B550 Steel Legend** | PCIe 4.0 x16 slot, Above 4G Decoding in BIOS, solid VRM | ~$80–100 used |
| **MSI MAG B550 Tomahawk** | Excellent VRM stability for long GPU compute runs, BIOS well-documented | ~$80–110 used |
| **Gigabyte X570 Aorus Elite** | Full X570 chipset, PCIe 4.0, more PCIe lanes if you add NVMe | ~$100–130 used |

**CPU**

For a single GPU setup, 12–16 cores is more than sufficient; clock speed matters for preprocessing and OS responsiveness. AMD wins on the consumer side due to the AM5/AM4 platform's longevity and Zen efficiency.

- **AMD Ryzen 5 5600X** — 6 cores / 12 threads, 4.6 GHz boost, 65 W TDP. ~$100 new, ~$70 used. Best single-thread performance in budget AM4.
- **AMD Ryzen 5 5600** — Slightly slower, runs cooler, ~$80 new. Also excellent.

**RAM**

A good rule of thumb is system memory = 4× GPU memory size. For the P100 16 GB, 64 GB (4 × 16 GB) DDR4 is a solid starting point for deep learning tasks.

- **32 GB DDR4-3200 (2 × 16 GB)** — minimum workable (~$35–50 used)
- **64 GB DDR4-3200 (2 × 32 GB)** — recommended for larger models (~$60–90 used)

---

### Path B — Used Intel X99 / LGA2011-v3 (Ultra-budget, ~$80–120 total platform)

An E5-2680 v4 + compatible used X99 motherboard starts at roughly $79, delivering 14 cores and 28 threads — ideal for multitasking and data-preprocessing-heavy workflows.

The Xeon E5-2680 v4 is widely considered the king of budget server CPUs, with 14 cores, 28 threads, and a 2.4 GHz base clock, offering multi-threaded performance competitive with modern mid-range chips at a fraction of the cost.

| Component | Choice | Approx. used price |
|---|---|---|
| **Motherboard** | Huananzhi X99-F8D / Kllisre X99 (both have Above 4G Decoding in BIOS) | ~$40–60 |
| **CPU** | Intel Xeon E5-2680 v4 (14C/28T) or E5-2678 v3 (12C/24T) | ~$20–35 |
| **RAM** | 32–64 GB DDR4 ECC RDIMM (required for X99 Xeon) | ~$20–40 |

> ⚠️ **X99 board caveat:** These Chinese OEM boards are very capable but require a BIOS update out of the box, and you must manually verify that "Above 4G Decoding" is present in the BIOS menu before inserting the P100.

---

### Critical P100-specific checklist for any board

The P100 uses a passive heatsink design and requires adequate system airflow for cooling — it cannot cool itself. Whatever case/platform you pick:

```
✅ Above 4G Decoding = Enabled  (fixes your PCI OUT OF RESOURCES error)
✅ Re-Size BAR = Disabled        (P100 is Pascal-gen; ReBAR can cause issues)
✅ PSU ≥ 500 W                   (P100 draws up to 250 W alone)
✅ Case with strong front-to-back airflow (P100 has no fans)
✅ PCIe x16 Gen 3 slot           (P100 spec requirement)
✅ No extra PCIe cards at first  (minimize resource conflicts while diagnosing)
```

---

**References:**
- [CPU and Memory Requirements for Tesla P100 — NVIDIA Forums](https://forums.developer.nvidia.com/t/cpu-and-memory-requirements-for-tesla-p100-pcie/50711)
- [Best Motherboard for Budget AI Workstations — PCTest/CameraEgg](https://www.cameraegg.org/test/best-motherboard-for-budget-ai-workstations/)
- [Best CPU for AI and Deep Learning Workloads 2026 — TensorRigs](https://tensorrigs.com/blog/best-cpu-for-ai-workstation/)
- [Cheap AI HomeLab on a Budget: V100s, Custom Boards — Angry Sysadmins](https://angrysysadmins.tech/2026/03/grassyloki/cheapish-ai-homelab-on-a-budget-v100s-custom-boards-and-nvlink/)
- [Best Xeon CPU Guide 2026 — WhoIsMcAfee](https://whoismcafee.com/best-xeon-cpu/)
