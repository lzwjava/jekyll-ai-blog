---
audio: false
generated: true
image: false
lang: en
layout: post
title: Buzzing after swapping server GPU
translated: false
type: note
---

Question: I recently bought a used AMD Instinct MI50 GPU to replace my RTX 4070. After installing the MI50 in my system (Intel i9-13900KF, MSI MAG B760M MORTAR WIFI, Corsair CX650F/750W PSU), the PC wouldn't turn on and made a buzzing noise. I swapped the RTX 4070 back in, but the issue persists. When testing the power supply with only the 24-pin ATX cable connected, the system won't boot, and using a stethoscope, I can hear a clear buzzing/sizzling sound coming from the motherboard right around the SATA 5 and 6 ports. What happened, and how can I fix this?

Answer:
Based on the symptoms and the specific hardware involved, your motherboard has likely suffered a severe electrical short circuit. The buzzing sound near the SATA ports is a critical indicator of hardware damage. Here is a breakdown of exactly what likely happened and why.

## The Probable Cause: The Server GPU Power Trap

The most likely culprit is the power delivery to the AMD Instinct MI50.

Unlike consumer graphics cards (like your RTX 4070), the AMD Instinct MI50 is a data center/server GPU. Many server GPUs do **not** use standard PCIe 8-pin power connectors. Instead, they often use **EPS12V 8-pin connectors** (the same cables used to power the CPU).

1. **Reverse Polarity Short:** The physical shape of PCIe 8-pin and EPS 8-pin connectors is very similar, but their electrical layouts are completely reversed. If you plugged a standard PCIe 8-pin power cable from your Corsair PSU into a server card that requires an EPS connection (or vice versa), it immediately sends 12V directly into the ground pins.
2. **Immediate Damage:** This creates a massive short circuit. While a good power supply has Short Circuit Protection (SCP), the sudden surge before the PSU shuts off can send a catastrophic voltage spike back through the motherboard's PCIe slot and power delivery systems.
3. **Dead Card:** Because you bought the MI50 used, there is also a high chance the card was already dead or shorted from a previous mining or server farm environment, which immediately passed a short to your motherboard.

## Why the Motherboard is Buzzing Near SATA 5/6

The buzzing or sizzling sound ("滋滋响") you hear is electrical arcing, a blown capacitor, or a damaged voltage regulator struggling to hold a charge.

On the MSI MAG B760M MORTAR, SATA ports 5 and 6 are located at the bottom right of the board. This specific area is directly adjacent to the **B760 Chipset (PCH)**.

* The chipset controls the SATA ports, USB headers, and some PCIe lanes.
* If a massive short circuit occurred on the motherboard (via the PCIe slot or a 5V/3.3V rail), it likely damaged the power delivery components that feed the chipset.
* Because the buzzing happens even when *only* the 24-pin ATX cable is connected, the damage is on the motherboard's standby power circuitry (5VSB) or main ATX power traces, meaning the board is continually trying to draw power into a dead short.

## Hardware Incompatibility Notes

Even if the power cables were correct, your setup faced a few extreme bottlenecks for an MI50:

* **Power Supply Limits:** The i9-13900KF can draw over 250W+, and the MI50 draws 300W. A 650W or 750W PSU is pushed to its absolute limits with this combination, making transient power spikes very dangerous.
* **Cooling Limitations:** The MI50 has no built-in fan. It relies on massive, high-speed server chassis fans forcing air through it. Putting it in a standard desktop PC without a custom 3D-printed fan shroud will cause it to overheat and shut down in minutes.
* **No Display Output:** The MI50 has no HDMI or DisplayPort outputs. You would have had to run the display through your motherboard using Intel integrated graphics (but your CPU is a "KF" model, meaning it has **no integrated graphics**).

## Next Steps

**Stop trying to turn the PC on.** Continuing to supply power to a short-circuiting motherboard can cause a fire hazard and may destroy your CPU, RAM, or storage drives.

1. **Remove all components:** Take out the RAM, CPU, SSDs, and both GPUs.
2. **Inspect the motherboard:** Shine a flashlight near the SATA 5 and 6 ports, the chipset heatsink, and the PCIe slots. Look for black scorch marks, melted plastic, or ruptured capacitors (small cylinders that have popped at the top).
3. **Test the PSU independently:** Disconnect the PSU entirely from the motherboard. Re-do the paperclip test you mentioned (jumping pins 4 and 5 on the 24-pin cable) with a case fan plugged into the PSU. If the PSU fan spins and there is no clicking or burning smell, the PSU might have survived, but it should still be treated with suspicion.
4. **Replace the Motherboard:** Unfortunately, a constant buzzing sound from the chipset area with only the 24-pin connected means the motherboard is completely dead and requires professional board-level repair or replacement.

When rebuilding, stick to your RTX 4070. Server GPUs require highly specialized modifications to run in a consumer desktop safely.
