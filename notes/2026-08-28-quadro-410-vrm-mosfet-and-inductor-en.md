---
audio: false
generated: true
image: false
lang: en
layout: post
title: Quadro 410 VRM MOSFET and Inductor
translated: false
type: note
---

Great — all three markings are now identified. Here's the answer:

---

**Question:** What are the components marked **B09 / N03** and **CFD0036** on the NVIDIA Quadro 410?

**Answer:**

---

**B09 / N03 → SMD marking for EMB09N03 — N-Channel Power MOSFET**

The two-line marking **B09** (top) / **N03** (bottom) is the SMD package code for the **EMB09N03** series, manufactured by **Excelliance MOS Corp.**

The full part designation is **EMB09N03V**, with the SMD marking code **B09N03**. It is an **N-Channel Logic Level Enhancement Mode MOSFET** with:
- Max Drain-Source Voltage (Vds): **30V**
- Max Drain Current (Id): **20A**
- Max Power Dissipation: **21W**
- On-State Resistance (RDSon): **9 mΩ**
- Package: **EDFN 3×3** (small SMD QFN-style)

On the Quadro 410, this MOSFET serves as a **power switching transistor** in the VRM (Voltage Regulator Module) — working alongside the APM8720 PWM controller you identified earlier.

---

**CFD0036 — Power Inductor / Choke**

"CFD0036" is a **part number for an SMD power inductor (choke coil)**, commonly used in GPU power delivery stages. The "CFD" prefix is a manufacturer series code (used by makers like Bourns, Coilcraft, or similar). On the Quadro 410, this sits in the buck converter output filter — exactly the same role as the **R47 inductor** discussed earlier, smoothing the PWM-switched voltage into clean regulated DC for the GPU or VRAM.

No public datasheet was found under that exact code, which is common — GPU board inductors often use custom or private-labeled part numbers. The value is typically in the **sub-µH to low µH range** (e.g., 0.33–1.0 µH) rated for 10A+ continuous current.

---

**Summary — how all 5 components fit together:**

| Component | Type | Role |
|---|---|---|
| APM8720 | PWM Controller IC | Brain of the VRM, controls switching |
| VP57F | N-Channel MOSFET | High/low side switch in buck converter |
| **B09N03 (EMB09N03)** | **N-Channel MOSFET** | **Additional power switch in VRM** |
| R47 | Power Inductor (0.47 µH) | Energy storage / output filter |
| **CFD0036** | **Power Inductor** | **Output filter choke in VRM stage** |

Together they form the **complete VRM power delivery circuit** for the Quadro 410's GPU core or memory voltage.

**References:**
- [EMB09N03V Datasheet — alltransistors.com](https://alltransistors.com/mosfet/transistor.php?transistor=49932)
- [B09N03 Datasheet — Alldatasheet](https://www.alldatasheet.com/view.jsp?Searchword=B09N03)
- [B09N03 — Excelliance MOS, datasheet4u](https://datasheet4u.com/datasheet-pdf/ExcellianceMOS/B09N03/pdf.php?id=1254749)
