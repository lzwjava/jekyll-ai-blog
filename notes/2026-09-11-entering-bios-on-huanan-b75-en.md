---
audio: false
generated: true
image: false
lang: en
layout: post
title: Entering BIOS on Huanan B75
translated: false
type: note
---

Question: How do I enter BIOS on a Huanan B75 motherboard?

Answer:

For most **Huanan B75** boards:

1. Power on / restart the PC.
2. Immediately **repeatedly press `Delete` (`Del`)**.
3. You should enter the BIOS/UEFI setup.

If `Del` doesn't work, try:

```text
Del   ← first choice
F2
F12
Esc
```

### If you're troubleshooting a GPU/PC build

For a B75 + Xeon/i5 setup, I would do:

```text
Power OFF
↓
Connect keyboard directly to rear USB 2.0
↓
Power ON
↓
Immediately tap Del repeatedly
↓
BIOS
```

**Important:** don't hold the key continuously; tap it rapidly from the moment you press the power button.

If you get **no display at all**, BIOS entry is not the first problem—you need to determine whether POST is completing. A photo of your exact Huanan B75 board would let me identify the BIOS key and relevant jumpers/connectors precisely.

I can also walk you through **B75 BIOS settings specifically for GPU testing/repair**, including PCIe primary display, CSM, Secure Boot, and boot order.
