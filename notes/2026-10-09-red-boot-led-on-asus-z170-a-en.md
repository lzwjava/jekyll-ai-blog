---
audio: false
generated: true
image: false
lang: en
layout: post
title: Red BOOT LED on ASUS Z170-A
translated: false
type: note
---

**Question:** Why is the red "BOOT DEVICE LED" light on my ASUS Z170-A motherboard lit up?

**Answer:**

The red LED near the **"BOOT DEVICE LED"** label on your ASUS Z170-A indicates that the system **cannot detect a bootable device**. This is one of the POST (Power-On Self-Test) debug LEDs.

Common causes:

1. **No storage device connected** — No SSD/HDD is plugged into the SATA or M.2 ports.
2. **Boot drive not detected** — The drive is connected but not being recognized (loose cable, dead drive, or wrong SATA port).
3. **No OS installed** — The drive is blank with no bootable operating system.
4. **Wrong boot order in BIOS** — The BIOS is trying to boot from the wrong device.
5. **M.2 slot conflict** — On the Z170-A, using certain M.2 modes can disable specific SATA ports, causing the connected drive to disappear.
6. **SATA mode mismatch** — Drive formatted for AHCI but BIOS is set to IDE (or vice versa).

**Steps to try:**
- Enter BIOS (press **Del** at startup) and check if your boot drive appears under Storage/Boot.
- Re-seat SATA cables and make sure they're plugged into the correct ports.
- Check the Boot Priority order in BIOS.
- If using M.2, verify it isn't disabling your SATA ports.

---

**References:**
- [ASUS Z170-A Manual & POST LED guide](https://www.asus.com/motherboards-components/motherboards/all-series/z170-a/)
- [ASUS POST LED troubleshooting](https://www.asus.com/support/FAQ/1045839/)
