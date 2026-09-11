---
audio: false
generated: true
image: false
lang: en
layout: post
title: MOSFET Overview
translated: false
type: note
---

Question: What is a MOSFET?

Answer: A **MOSFET** (Metal-Oxide-Semiconductor Field-Effect Transistor) is a type of semiconductor device widely used for switching and amplifying electronic signals in modern electronic circuits. It is the most common building block of microprocessors, memory chips, and power supply controllers.

---

**Key Terminals**

* **Gate (G):** The control terminal. Applying voltage here creates an electric field that regulates current flow.
* **Drain (D):** The terminal where electric current enters/leaves the channel.
* **Source (S):** The terminal where charge carriers enter the channel.
* **Body/Substrate (B):** The base semiconductor material (often internally connected to the Source).

**How It Works**
A MOSFET acts like an electronic switch. An insulating oxide layer (typically silicon dioxide) sits directly below the Gate terminal, preventing direct electrical contact with the semiconductor channel below. When a sufficient voltage is applied to the Gate relative to the Source, an electric field forms across the oxide layer. This field creates a conductive channel between the Source and Drain, allowing current to flow.

**Primary Types**

1. **N-Channel (NMOS):** Conduction occurs via electrons. Turns ON when a positive voltage is applied to the Gate.
2. **P-Channel (PMOS):** Conduction occurs via electron holes. Turns ON when a negative voltage relative to the Source is applied to the Gate.
3. **Enhancement Mode (Most Common):** Normally OFF; requires a Gate voltage to turn ON.
4. **Depletion Mode:** Normally ON; requires a Gate voltage to turn OFF.

**Main Applications**

* **Digital Logic:** Integrated into CMOS (Complementary MOS) configurations to form computer processors (CPUs, GPUs) and memory (RAM, Flash).
* **Power Electronics:** Used as efficient high-speed electronic switches in motor drives, switched-mode power supplies (SMPS), and battery control units.
* **Analog Circuits:** Functions as an amplifier in radio frequency (RF) equipment and audio amplifiers.
