---
audio: false
generated: true
image: false
lang: en
layout: post
title: Lenovo L-IG41M3 USB Boot Setup
translated: false
type: note
---

Question: Lenovo L-IG41M3: how to access the BIOS and set it to boot from a USB drive?

Answer:
Here is how to enter the BIOS and configure your Lenovo L-IG41M3 motherboard (LGA 775 Intel G41 chipset) to boot from a USB drive.

### Method 1: Use the One-Time Boot Menu (Quickest Method)

1. Insert your bootable USB flash drive into a USB port on your computer before turning it on.
2. Power on or restart the system.
3. As soon as the computer starts, repeatedly tap the **F12** key (or **F11** on some OEM BIOS revisions).
4. The **Boot Device Options / Startup Menu** will appear.
5. Use the arrow keys to select your USB drive (often listed as **USB-HDD**, **USB Storage**, or the drive brand name) and press **Enter**.

---

### Method 2: Change Boot Order in BIOS Setup (Permanent Setup)

1. Insert your bootable USB flash drive.
2. Power on the computer and immediately tap the **F1** or **Delete** key repeatedly until the BIOS Setup Utility screen appears.
3. Use the keyboard arrow keys to navigate to the **Startup** or **Boot** tab.
4. Locate **Primary Boot Sequence** (or **Boot Priority / Boot Device Priority**).
5. Highlight your USB drive or the **USB-HDD** option.
6. Use the **+** / **-** keys (or **Page Up / Page Down**) to move the USB device to the top position (Priority 1).
7. Navigate to the **Save & Exit** tab, select **Save Changes and Exit** (or press **F10**), and hit **Enter**.
8. The computer will restart and boot automatically from your USB drive.
