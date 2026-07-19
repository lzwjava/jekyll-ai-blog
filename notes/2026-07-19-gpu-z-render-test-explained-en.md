---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU-Z Render Test Explained
translated: false
type: note
---

Question: what's 1. GPU-Z test ?

Answer: A "GPU-Z test" typically refers to the **PCI-Express Render Test**, which is a built-in feature of the free graphics utility **TechPowerUp GPU-Z**.

Modern graphics cards use power-saving features that automatically drop their connection speed and PCIe lanes (e.g., dialing down from PCIe x16 4.0 to PCIe x4 1.1) when sitting idle on your desktop. Because of this, looking at GPU-Z while doing nothing might show incorrect specs.

The GPU-Z render test solves this by forcing a small, lightweight 3D window to render on your screen. This puts a minor load on the graphics card, forcing it to instantly kick up to its maximum performance state so you can verify if your card is running at its correct, full bus width and speed.

### How to Use It

1. Open **GPU-Z**.
2. Look at the **Bus Interface** box on the main "Graphics Card" tab.
3. Click the small **question mark (?)** icon right next to the Bus Interface box.
4. Click **Start Render Test**. A window with a moving render will appear, and you can watch the Bus Interface value update to reflect your true maximum speeds.

*Note: The GPU-Z render test is only meant to wake up the card to check bandwidth and basic lane routing. It is not a heavy stress test or stability benchmark. For actual thermal, hardware stability, or performance stress testing, tools like FurMark or 3DMark are used instead.*

References:

* [TechPowerUp GPU-Z Main Page](https://www.techpowerup.com/gpuz/)
