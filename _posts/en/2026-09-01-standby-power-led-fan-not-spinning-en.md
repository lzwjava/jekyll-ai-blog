---
audio: false
generated: true
image: false
lang: en
layout: post
title: Standby Power LED, Fan Not Spinning
translated: false
type: note
---

**Question:** When a Huntkey Super 500N PSU is connected to an ASUS H81M-K motherboard and the SB_PWR LED lights up but the PSU fan doesn't spin — what does that mean? And why does the paperclip test show the fan working fine?

---

**Answer:**

### What SB_PWR Lighting Up Means

The SB_PWR LED on the ASUS H81M-K is the **Standby Power LED**. It lights up to indicate that the system is receiving standby power — meaning the PSU is delivering the 5VSB (5-volt standby) rail to the motherboard. This happens even when the system hasn't been turned on yet. So SB_PWR glowing is actually a **good sign** — it confirms the PSU is plugged in, switched on, and delivering standby voltage to the board.

---

### Why the PSU Fan Doesn't Spin

The fan not spinning is the real problem. The PSU fan only spins when the PSU is **fully switched on** (the main rails activate), which requires the motherboard to assert the PS_ON signal. If the fan stays off, the system never got past the standby state. Possible causes:

1. **Short circuit on the motherboard or components** — this is a very common scenario: the PSU passes the paperclip test fine on its own, but when connected to the motherboard, nothing happens — pointing to a short somewhere in the system.

2. **Power button (PWR_SW) not connected or faulty** — if the front panel power button header isn't properly connected, pressing the power button sends no signal, so the PSU never turns on fully.

3. **Missing or loose CPU power connector (4-pin/8-pin EPS)** — if your motherboard has an 8-pin CPU power port and it's not connected (or only a 4-pin is used), the system may fail to start.

4. **Standoff short** — a standoff (motherboard mount) that is misaligned or missing can cause a short between the board and the case. Try testing the motherboard outside the case on a non-conductive surface.

5. **PSU passes paperclip test but is still weak** — the paperclip test only proves the PSU *can* start, not that it is healthy. It says nothing about whether the +12V, +5V, and +3.3V rails hold correct voltage under load. A unit that passes the paperclip test can still be the fault.

---

### Why Paperclip Test Works But Board Doesn't

Bridging the green PS_ON pin to a black ground pin (the paperclip trick) forces the PSU into running outside the system. A spinning fan means it powers on, but this is not a representative test under real load. When connected to the motherboard, the PSU must receive the PS_ON signal *from the board* after the power button is pressed. If anything prevents that signal — a short, missing connector, or faulty power switch — the PSU stays in standby mode and the fan never spins.

---

### Recommended Troubleshooting Steps

1. Confirm the **24-pin ATX** and **4-pin CPU** power connectors are fully seated
2. Check the **PWR_SW header** is correctly connected on the F_PANEL connector
3. Try **shorting the PWR_SW pins directly** on the motherboard header with a screwdriver to bypass the case button
4. **Breadboard test** — remove the motherboard from the case and test it on a non-conductive surface to rule out a standoff short
5. Strip down to **bare minimum** (CPU + 1 RAM stick, no GPU, no drives) and try to boot
6. Use a **multimeter or PSU tester** to verify voltages on the main rails under load

---

**References:**

- [ASUS H81M-K User Manual – SB_PWR LED (ManualsLib)](https://www.manualslib.com/manual/565354/Asus-H81m-K.html?page=28)
- [PSU fan not spinning when plugged into motherboard (BleepingComputer)](https://www.bleepingcomputer.com/forums/t/735132/psu-fan-not-spinning-when-plugged-into-motherboard/)
- [Motherboard No Power: How to Diagnose a Dead Board (TheCoreITech)](https://www.thecoreitech.com/troubleshooting/fix-motherboard-no-power/)
- [PSU passed paperclip test but fan barely spinning (Tom's Hardware)](https://forums.tomshardware.com/threads/psu-passed-paperclip-test-but-the-fan-is-barely-spinning.2688075/)
