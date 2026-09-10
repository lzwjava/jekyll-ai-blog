---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI B150M PRO-VH Power On Guide
translated: false
type: note
---

Question: **Where is the front-panel connector on the MSI B150M PRO-VH, and how do I power it on?**

Answer:

On the **MSI B150M PRO-VH**, the front-panel connector is called **JFP1**, not `P_FRONT_PANEL`. The manual confirms it has a 10-pin JFP1 header. ([ManualsLib][1])

The pinout is:

```text
JFP1
┌─────────────────┐
│ 2  4  6  8  10 │
│ 1  3  5  7  9  │
└─────────────────┘

1  HDD LED +
3  HDD LED -

2  Power LED +
4  Power LED -

5  RESET SW
7  RESET SW

6  POWER SW
8  POWER SW

9  Reserved
10 No Pin
```

For **just testing the motherboard**, you don't need the case's power button.

### Power it on with a screwdriver

With PSU connected:

```text
24-pin ATX  → motherboard
8-pin CPU   → motherboard
```

Then briefly touch a screwdriver across:

```text
JFP1 pin 6 ↔ pin 8
```

That's the **POWER SW** pair. MSI's manual explicitly identifies pins 6/8 as the power switch. ([manualzz.com][2])

**Only momentarily short them**—about 0.5–1 second. Don't hold the screwdriver there.

You don't need to connect:

```text
HDD LED
POWER LED
RESET SW
```

to get the board to start.

If you're physically unable to find **JFP1**, send me a photo of your B150M PRO-VH motherboard and I can point out the exact pins.

References:

* [MSI B150M PRO-VH manual listing](https://www.manualslib.com/products/Msi-B150m-Pro-Vh-13624495.html?utm_source=chatgpt.com)
* [MSI front-panel header pinout](https://mans.io/files/viewer/203929/6?utm_source=chatgpt.com)

[1]: https://www.manualslib.com/products/Msi-B150m-Pro-Vh-13624495.html?utm_source=chatgpt.com "Msi B150M PRO-VH Manuals | ManualsLib"
[2]: https://manualzz.com/doc/o/1guq12/msi-b150m-pro-vdh-motherboard-user-manual-overview-of-components?utm_source=chatgpt.com "Overview of Components. MSI B150M PRO-VDH, MS-7982v1.1 | Manualzz"
