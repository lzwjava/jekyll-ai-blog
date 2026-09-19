---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Fan Header Solutions for B85
translated: false
type: note
---

Question: How to connect the GPU fan's 4-pin connector to the SOYO SY-B85N motherboard when the only CPU fan header is already occupied?

Answer:

The SOYO SY-B85N is a Mini-ITX board — it's extremely common for these small boards to have **only 1 fan header** (CPU_FAN), with no SYS_FAN header at all. You have a few practical workarounds:

---

### Option 1: Fan Hub / Splitter (Recommended)
Use a **4-pin PWM fan splitter** — it plugs into the single CPU_FAN header and gives you 2 outputs.
- The motherboard controls both fans together
- Works fine since neither the CPU cooler nor the GPU fan draws much power
- Cost: ¥5–15 on Taobao

---

### Option 2: Molex / SATA Power Adapter
Run the GPU fan directly from the **PSU** using a:
- **3-pin/4-pin fan → SATA power adapter**, or
- **3-pin/4-pin fan → Molex adapter**

⚠️ Downside: Fan runs at **full speed always** (no PWM speed control), which may be loud.

---

### Option 3: USB Fan Controller
Use a cheap **fan speed controller** (旋钮调速器) inline with the fan cable. Manual control, no header needed.

---

### Option 4: Verify the Board Has No Hidden Header
Double-check your specific board revision — look for an unpopulated 4-pin footprint labeled **SYS_FAN** or **CHA_FAN** near board edges. Some budget boards omit the connector but keep the pads. You could solder a header on if comfortable.

---

### Recommendation
The **PWM splitter on the CPU_FAN header** is the cleanest solution for your setup. Since the Tesla M40's fan is already doing its job (keeping it under 80°C at 3K RPM per the listing), you just need a reliable connection — not precise independent control.

References:
- [SOYO SY-B85N 产品页 – 板载接口说明](https://www.soyo.com.cn)
- [4-pin PWM Fan Splitter Guide](https://www.google.com/search?q=4+pin+PWM+fan+splitter+CPU_FAN+header)