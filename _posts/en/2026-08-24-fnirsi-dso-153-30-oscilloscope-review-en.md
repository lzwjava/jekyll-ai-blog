---
audio: false
generated: true
image: false
lang: en
layout: post
title: "FNIRSI DSO-153: $30 Oscilloscope Review"
translated: false
type: note
---

**Question:** How good is the FNIRSI 2-in-1 mini digital oscilloscope + signal generator with 1MHz bandwidth, given its low price of ¥219 CNY (~$30 USD)?

---

**Answer:**

This is almost certainly the **FNIRSI DSO-153**, and for the price, it's a surprisingly capable little tool — but with some important limitations to be aware of.

### ✅ What it does well

It offers a real-time sampling rate of **5 MS/s**, **1 MHz bandwidth**, and supports voltages up to **±400V** — plus full trigger modes (Auto/Normal/Single), making it usable for both periodic analog and non-periodic digital signals.

The built-in DDS signal generator can output **14 different waveforms** (sine, square, sawtooth, noise, exponential, etc.), with a maximum output frequency of up to **10 kHz**.

It has a **2.8-inch 320×240 LCD**, a **1000 mAh battery** good for about **4 hours**, and charges via **Type-C** USB. It supports **8 languages** including English and Chinese, and features a one-click AUTO mode to display waveforms without manual fiddling.

The real value lies in having two essential tools in one compact, battery-powered package under 200 grams — useful if you need to verify signal integrity or stimulate circuits without carrying multiple devices.

---

### ⚠️ Limitations to keep in mind

- **1 MHz bandwidth is very narrow.** It's fine for audio signals, low-speed serial (UART/I2C/SPI at low baud rates), power supply ripple, and sensor outputs — but completely useless for anything RF, high-speed digital, or above ~500 kHz in practice (bandwidth rule of thumb: 5× the signal frequency for clean waveforms).
- **5 MS/s sampling rate** is modest. Higher-frequency signals will show aliasing or poor waveform fidelity.
- **Signal generator tops out at 10 kHz** — this is a big constraint if you need to generate test signals beyond audio frequencies.
- It's described as "highly practical and cost-effective" — but the implied audience is hobbyists and learners, not professionals.

---

### 🎯 Bottom Line

At ¥219 (~$30 USD), it's **excellent value for its target audience**: electronics students, hobbyists, and technicians doing basic automotive or appliance diagnostics. Don't expect it to replace a proper bench oscilloscope. If you need more bandwidth (even 10–50 MHz), FNIRSI's own lineup has better options like the DSO-510 (10 MHz) or 2C23T (10 MHz with multimeter) for a bit more money.

---

**References:**

- [FNIRSI DSO-153 Official Product Page](https://www.fnirsi.com/products/dso-153)
- [DSO-153 on Martview – Full Specs](https://www.martview.com/fnirsi-dso-153-2-in-1-portable-1mhz-bandwidth-digital-oscilloscope-signal-generator.html)
- [DSO153 on Amazon](https://www.amazon.com/FNIRSI-DSO153-Oscilloscope-Generator-Automotive/dp/B0D2TGM82J)
- [DSO153 Review – AliExpress Wiki](https://www.aliexpress.com/s/wiki-ssr/article/fnirsi-dso153-oscilloscope-signal-generator-oscope-meter-products-info-and-review)
