---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Quadro 410 VRM MOSFET与电感
translated: true
type: note
---

很好——所有三个标记现已识别。以下是答案：

---

**问题：** NVIDIA Quadro 410 上标有 **B09 / N03** 和 **CFD0036** 的组件是什么？

**答案：**

---

**B09 / N03 → EMB09N03 的 SMD 标记——N-Channel Power MOSFET**

两行标记 **B09**（顶部）/ **N03**（底部）是 **EMB09N03** 系列的 SMD 封装代码，由 **Excelliance MOS Corp.** 制造。

完整型号为 **EMB09N03V**，SMD 标记代码为 **B09N03**。它是一个 **N-Channel Logic Level Enhancement Mode MOSFET**，具有以下参数：

- Max Drain-Source Voltage (Vds)：**30V**
- Max Drain Current (Id)：**20A**
- Max Power Dissipation：**21W**
- On-State Resistance (RDSon)：**9 mΩ**
- Package：**EDFN 3×3**（小型 SMD QFN 式）

在 Quadro 410 上，该 MOSFET 在 VRM（Voltage Regulator Module）中用作 **power switching transistor**，与您之前识别的 APM8720 PWM 控制器协同工作。

---

**CFD0036 — Power Inductor / Choke（功率电感）**

"CFD0036" 是 **SMD 功率电感（choke coil）的零件编号**，常用于 GPU 供电级。"CFD" 前缀是制造商系列代码（由 Bourns、Coilcraft 等厂商使用）。在 Quadro 410 上，它位于 buck converter 输出滤波器中——与之前讨论的 **R47 电感** 的角色完全相同，将 PWM 开关电压平滑为干净的稳压直流电，供 GPU 或 VRAM 使用。

在该确切代码下未找到公开数据表，这很常见——GPU 板载电感通常使用定制或私有标签零件编号。其值通常在 **sub-µH 到低 µH 范围**（例如 0.33–1.0 µH），额定连续电流 10A 以上。

---

**总结——所有 5 个组件如何协同工作：**

| 组件 | 类型 | 作用 |
| --- | --- | --- |
| APM8720 | PWM Controller IC | VRM 的大脑，控制开关 |
| VP57F | N-Channel MOSFET | Buck converter 中的高/低侧开关 |
| **B09N03 (EMB09N03)** | **N-Channel MOSFET** | **VRM 中的额外功率开关** |
| R47 | Power Inductor (0.47 µH) | 储能 / 输出滤波器 |
| **CFD0036** | **Power Inductor** | **VRM 级输出滤波扼流电感** |

它们共同构成 Quadro 410 GPU 核心或内存电压的 **完整 VRM 供电电路**。

**参考链接：**

- [EMB09N03V Datasheet — alltransistors.com](https://alltransistors.com/mosfet/transistor.php?transistor=49932)
- [B09N03 Datasheet — Alldatasheet](https://www.alldatasheet.com/view.jsp?Searchword=B09N03)
- [B09N03 — Excelliance MOS, datasheet4u](https://datasheet4u.com/datasheet-pdf/ExcellianceMOS/B09N03/pdf.php?id=1254749)
