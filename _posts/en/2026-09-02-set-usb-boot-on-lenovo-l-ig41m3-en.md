---
audio: false
generated: true
image: false
lang: en
layout: post
title: Set USB Boot on Lenovo L-IG41M3
translated: false
type: note
---

Question: How to confirm BIOS access and boot from a USB drive on the Lenovo L-IG41M3 motherboard?

Answer:
Great to hear that pressing **F1** successfully opened the BIOS Setup Utility! Now that you are inside the BIOS, follow these exact steps to set your USB drive as the primary boot device:

1. **Plug in the USB:** Make sure your bootable USB flash drive is connected before powering on or restarting, so the BIOS detects it properly.
2. **Navigate to the Boot Menu:** Use the arrow keys to select the **Startup** or **Boot** tab at the top.
3. **Select Primary Boot Sequence:** Highlight **Primary Boot Sequence** (or **Boot Device Priority**) and press **Enter**.
4. **Move USB to the Top:** Find your USB drive (it may be named **USB-HDD**, **USB Storage**, or the drive's brand name). Use the **+** and **-** keys (or **Page Up / Page Down**) to move the USB option to position **1**.
5. **Save and Exit:** Press **F10**, select **Yes** to save changes, and hit **Enter**.

Your system will restart and boot directly from your USB drive.
