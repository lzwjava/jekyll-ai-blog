---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gigabyte 6900 XT Black Screen Repair
translated: false
type: note
---

Question: What is the content and repair process explained in the YouTube video "Gigabyte 6900 XT Graphics Card Repair - Black Screen"?

Answer:
This video from **NorthridgeFix** demonstrates the diagnosis and repair of a **Gigabyte Radeon RX 6900 XT** graphics card that turns on but fails to display an image (black screen issue).

### Key Steps in the Repair Process

1. **Initial Power Rail & Short Inspection:**
* The technician measures the 12V power input lines and 3.3V line for short circuits using diode mode (voltage drop test) [[01:08](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvzsPSHN6uCo%26t%3D68)].
* All power lines measure around ~0.45V - 0.47V drop, confirming there are no short circuits on the main power rails [[01:32](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvzsPSHN6uCo%26t%3D92)].


2. **Visual Inspection under Microscope:**
* Performs a thorough visual check of both sides of the PCB for burnt components, liquid damage, or physical damage [[02:15](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvzsPSHN6uCo%26t%3D135)].
* Minor surface corrosion is cleaned off using isopropyl alcohol and an anti-static wire brush [[05:08](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvzsPSHN6uCo%26t%3D308)].


3. **Identifying the Root Cause:**
* Inspecting the PCIe interface edge near the bottom slot, a small surface-mount coupling capacitor along one of the PCIe data lines is found physically damaged/torn loose from its pads [[09:00](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvzsPSHN6uCo%26t%3D540)].
* Missing or broken data line capacitors prevent proper communication with the motherboard, causing a black screen output [[09:23](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvzsPSHN6uCo%26t%3D563)].


4. **Component Repair & PCB Masking:**
* Flux and fresh solder are applied to resolder the loose capacitor back to its copper trace pads [[10:06](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvzsPSHN6uCo%26t%3D606)].
* Continuity is confirmed using a multimeter from the capacitor to the PCIe slot contact [[11:04](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvzsPSHN6uCo%26t%3D664)].
* UV solder mask (cured with a UV lamp) is applied around the component to secure the fragile/weak pads and prevent future tearing [[13:15](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvzsPSHN6uCo%26t%3D795)].


5. **Testing and Verification:**
* The graphics card is installed in a test bench system with 12V PCIe power and HDMI connected [[15:02](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvzsPSHN6uCo%26t%3D902)].
* Upon powering on, the card successfully posts and outputs a working display signal to the monitor [[15:52](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvzsPSHN6uCo%26t%3D952)].



References:

* [Gigabyte 6900 XT Graphics Card Repair - Black Screen](http://www.youtube.com/watch?v=vzsPSHN6uCo)
