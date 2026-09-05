---
audio: false
generated: true
image: false
lang: en
layout: post
title: WD SATA Drive 8-Pin Jumper
translated: false
type: note
---

**Question:** On a WD SATA hard drive, there are three connectors — one going to the PSU, one is SATA data. What is the third 8-pin connector?

**Answer:**

That 8-pin connector is a **jumper pin block** — it's not meant to be plugged into anything during normal use.

They are jumper pins. You can enable particular settings by placing a small jumper shunt onto specific pairs of pins, creating an electrical circuit between them. The settings these jumpers enable are hard-coded onto the drive's printed circuit board.

On Western Digital SATA drives specifically, the pin pairs do the following:

- **Pins 1 & 2** — Disables the drive's spread-spectrum clocking (SSC) feature, which helps manage electromagnetic interference.
- **Pins 5 & 6** — Limits data transfer speed to 150 MB/s (SATA I speed), useful for older controllers.
- **Pins 3 & 4** — Enables PM2 mode on drives that support it.

On desktop drives, these 8 pins are for factory firmware or jumper-enabled settings like "Power-Up In Standby" (PUIS), rather than for user data.

**In short: you don't need to connect anything to it.** You don't need to connect anything to the 8-pin — leave it without a jumper for the default behavior. It's a legacy feature carried over from the IDE era, mainly useful in specific enterprise or compatibility scenarios.

---

**References:**

- [What is this 8 pin connector on my hard drive? – PCPartPicker](https://pcpartpicker.com/forums/topic/359090-what-is-this-8-pin-connector-on-my-hard-drive)
- [How to Use Jumpers on a SATA Hard Drive – Chron](https://smallbusiness.chron.com/use-jumpers-sata-hard-drive-69047.html)
- [What are the 8 pins for on this SATA hard drive? – Tom's Hardware](https://forums.tomshardware.com/threads/what-are-the-8-pins-for-on-this-1tb-sata-hard-drive.2094318/)
