---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fans Spin No Display Troubleshooting
translated: false
type: note
---

Question: **Your i5-6500 + MSI B150M PRO boots fans, but gives no video and seems completely unresponsive. Debian is already installed on the HDD. What should you test?**

Answer: **The HDD/Debian is probably not the first thing to investigate.** If you get absolutely no POST/video, first establish whether the motherboard is actually POSTing.

For this setup:

```text
i5-6500
   │
   ├── HD Graphics 530
   │
MSI B150M PRO
   │
   ├── RAM
   ├── PSU
   ├── HDD (Debian)
   └── motherboard video output
```

### 1. Remove the HDD completely

You don't need Debian to get the BIOS screen.

Disconnect the SATA HDD and try:

```text
CPU + cooler
1 stick DDR4
PSU 24-pin + 8-pin CPU
keyboard
monitor → motherboard video output
```

You should still get **MSI logo / BIOS**.

### 2. Make sure the monitor is connected to the motherboard

Since the i5-6500 has **HD Graphics 530**, connect:

```text
monitor
   ↓
MSI B150M PRO HDMI/DVI/VGA output
```

**not** to a nonexistent/disconnected discrete GPU.

### 3. Check RAM

This is one of the first things I'd test.

Try:

```text
1 DIMM
→ boot

same DIMM in another slot
→ boot

different DIMM
→ boot
```

A bad/poorly seated DIMM can give you fans but no display.

### 4. Clear CMOS

Power off PSU, unplug it, then clear CMOS using the motherboard's CMOS jumper/battery procedure.

Then retry the minimal configuration.

### 5. Check whether it is actually POSTing

The really useful distinction is:

**A. Fans spin + no display + keyboard doesn't respond**

→ suspect POST/power/CPU/RAM/motherboard.

**B. Fans spin + no display + keyboard LEDs respond / Debian eventually boots**

→ system may actually be booting; video path becomes much more likely.

For example, after waiting 30–60 seconds, try:

```text
Caps Lock
Num Lock
```

If the keyboard LED changes when you press the key, that's evidence that the machine may have progressed substantially through boot.

### 6. Your oscilloscope can actually help here

Since you're experimenting with the DSO153, you can probe motherboard power rails.

Black probe:

```text
PSU GND
```

Red probe:

```text
12V
5V
3.3V
```

and then look at the CPU/RAM power-regulator outputs.

**But don't randomly probe tiny motherboard pins with the scope yet.** Start with known power rails and ground.

If you can send me a **photo of your exact MSI B150M PRO board and how you've connected the PSU/RAM/monitor**, I can point out what to test first.
