---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI Debug LED Alternating CPU RAM
translated: false
type: note
---

Question: **The MSI B150M PRO Debug LED alternates between the CPU and RAM indicators. What does that mean?**

Answer: That is actually **useful diagnostic information**. It means the board is getting far enough into its POST sequence to check the CPU and memory, but it is **not successfully completing memory initialization**.

Try this order:

1. **Power off completely.**
2. Remove all RAM.
3. Install **one DDR4 DIMM only**.
4. Try the recommended DIMM slot first; if no POST, try the other slot(s).
5. Reseat the RAM firmly until both latches engage.
6. Clear CMOS.
7. Boot with only:

   ```text
   i5-6500
   1× DDR4
   PSU 24-pin
   PSU CPU 8-pin
   motherboard video output
   ```

   Disconnect HDD and discrete GPU.

### Pay attention to the LED

If it does:

```text
CPU → RAM → CPU → RAM → ...
```

that's different from simply staying permanently on **CPU** or **DRAM**.

A repeating CPU/DRAM sequence can indicate the board is repeatedly failing/retrying initialization, with **RAM/socket/CPU memory-controller/contact issues** being high on the list.

For an i5-6500, the memory controller is **inside the CPU**, so don't assume "RAM LED = bad RAM." Possible causes include:

```text
DDR4 DIMM
   ↓
DIMM slot / traces
   ↓
CPU socket LGA1151 contacts
   ↓
i5-6500 integrated memory controller
   ↓
BIOS / motherboard
```

**The LGA1151 socket is particularly worth inspecting** if multiple known-good DDR4 sticks behave the same way. One bent socket pin can cause memory-channel problems.

If you upload a photo of the **Debug LED area + RAM slots + CPU socket**, I can help you identify exactly which LED sequence you're seeing and what to test next.