---
audio: false
generated: true
image: false
lang: en
layout: post
title: PSU or CPU Fan Diagnosis
translated: false
type: note
---

**Question:** The fan flashes briefly then stops — how do we diagnose whether the ATX 12V pin problem is a PSU issue or a CPU issue?

---**Question:** The fan flashes briefly then stops — how can we tell if the ATX 12V issue is caused by the PSU or the CPU?

---

**Answer:**

The "fan flashes then dies" symptom is a classic sign of a **protection circuit triggering** — something is wrong and the board shuts itself down instantly. Here is how to systematically find out what.

---

### 🔍 Step-by-Step Diagnosis

**Step 1 — Check the obvious first: Is the ATX 12V 4-pin actually plugged in?**

A very common cause of this symptom is simply not having the 4-pin ATX 12V connector plugged into the motherboard near the CPU. Double-check it is firmly seated.

---

**Step 2 — Test if the PSU itself is the problem**

Use the **paperclip test** to test the PSU without any motherboard connected:

1. Unplug PSU from everything
2. Take a paperclip, bend it into a U-shape
3. Short the **green wire (PS_ON)** to any **black wire (GND)** on the 20-pin connector
4. Plug PSU into wall and switch it on
5. ✅ If PSU fan spins continuously → PSU is alive
6. ❌ If nothing happens → PSU is dead

---

**Step 3 — Strip down to bare minimum**

Remove everything except:

- CPU + heatsink/fan
- 1 stick of RAM
- Main 20-pin power
- ATX 12V 4-pin power

With only one stick of RAM and the CPU installed, if the CPU fan still spins for a couple of seconds and stops with no beeps, the fault points to either the motherboard or CPU.

---

**Step 4 — Key clue: remove the ATX 12V 4-pin and try**

If you disconnect the CPU 4-pin ATX 12V power, and the system stays on (but won't POST), this strongly suggests the CPU or its power delivery is the problem — not the PSU. If it shuts off even without the 4-pin connected, the motherboard may be shorted.

---

**Step 5 — Check the CPU heatsink**

One surprisingly common cause: the heatsink installed backwards or not making proper contact. The CPU's internal thermal sensor detects overheating instantly and shuts everything down. Reseat the heatsink and make sure the thermal paste is applied correctly.

---

### 🧭 Quick Diagnosis Summary Table

| Symptom | Most Likely Cause |
| --- | --- |
| Fan flashes, PSU paperclip test fails | **PSU is dead** |
| Fan flashes, paperclip test passes | **Motherboard or CPU** |
| Stays on without 4-pin, dies with 4-pin | **CPU or VRM on motherboard** |
| No beep at all with RAM installed | **Motherboard likely faulty** |
| Beeps heard | **RAM issue — try reseating** |

---

### ⚠️ Most Likely Culprit in Your Case

Given you have a **Huntkey 280W PSU** (old, low-wattage), the PSU is the first suspect. Old PSUs degrade over time and may not deliver stable 12V under load — if the PSU cannot handle the system's power demand, the fan spins for one second and then the system powers down.

---

**References:**

- [Fan spins half second then stops — Tom's Hardware](https://forums.tomshardware.com/threads/hit-power-buton-cpu-fan-spins-for-half-a-second-then-stops-spin-and-stop-forever-no-booting.3034486/)
- [No POST, fan spins and cuts out — AnandTech](https://forums.anandtech.com/threads/no-post-fan-spins-cuts-out-doesnt-cut-when-cpu-not-plugged-in.1277027/)
- [Power on, CPU fan spins 1 sec then shuts down — AnandTech](https://forums.anandtech.com/threads/power-on-cpu-fan-spins-for-1-sec-then-power-down.1608528/)
