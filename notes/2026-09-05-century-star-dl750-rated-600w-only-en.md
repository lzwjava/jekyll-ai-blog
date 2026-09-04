---
audio: false
generated: true
image: false
lang: en
layout: post
title: Century Star DL750 rated 600W only
translated: false
type: note
---

Question: Is the **世纪之星 DL750** a good PSU compared with the previous two?

Answer: **I would rank this below the SAMA and Segotep options**, especially for your GPU repair/testing work.

The listing says:

* **Brand:** 世纪之星 (Century Star)
* **Model:** DL750
* **Rated:** **600W**
* **Maximum/peak:** **750W**
* **CPU:** 8+8-pin EPS
* **GPU:** 2 × 6+2-pin PCIe
* **Mainboard:** 24-pin
* **SATA:** available
* **Non-modular:** cables are included
* **Used:** pulled from a machine
* Seller claims no repair/no hidden problems

### The important part

**“额定600W，最大750W” means this is basically a 600W PSU, not a 750W PSU.**

I would interpret it as:

```text
DL750
  │
  ├── Continuous/rated: 600 W  ← what matters
  └── Maximum:            750 W  ← don't design around this
```

So despite **DL750** being in the model name, you should compare it against the **SAMA 600W**, not a real 750W PSU.

### For your use

| PSU            | Real rated power | My choice |
| -------------- | ---------------: | --------- |
| **鑫谷 SN750W**  |            750W* | 🥇        |
| **先马 战旗750**   |             600W | 🥈        |
| **世纪之星 DL750** |             600W | 🥉        |

*Assuming the SN750W label really confirms 750W continuous output.

The DL750's **double 6+2 PCIe** is enough for many ordinary GPUs, but that's not particularly impressive for a PSU intended for your **GPU repair/test bench**.

Also, **“拆机下来的”** is a negative compared with a genuinely lightly-used retail PSU: you don't know how many years it spent running or what load it saw.

### My buying rule

For your bench, I'd rather spend a little more for:

**750–850W genuine continuous-rated PSU + strong 12V rail + 2–4 independent PCIe cables + known OEM/platform.**

And if you're going to test **4090/5090-class cards**, I'd skip all three of these and get a **quality 1000W+ PSU**.

If you show me the **DL750's label**, I can check the actual **12V amperage, OEM/platform, rails, and protections**.
