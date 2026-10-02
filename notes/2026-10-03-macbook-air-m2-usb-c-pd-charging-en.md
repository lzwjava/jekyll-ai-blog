---
audio: false
generated: true
image: false
lang: en
layout: post
title: MacBook Air M2 USB-C PD Charging
translated: false
type: note
---

Question: **Can a MacBook Air M2 use any USB-C charger? What charger type does it need?**

Answer:

Yes. **MacBook Air M2 uses USB-C Power Delivery (USB-C PD)**, so many Type-C chargers can charge it, not only Apple's charger.

The important points:

* Connector: **USB-C**
* Charging protocol: **USB Power Delivery (USB-C PD)**
* Voltage: typically **20V**
* Power:

  * MacBook Air M2 supports up to about **67W fast charging** (depending on configuration and charger)
  * It normally ships with:

    * 30W USB-C adapter (base models)
    * 35W dual USB-C compact adapter (some configurations)
    * optional 67W adapter for fast charging

Compatible chargers:

* ✅ Apple USB-C charger
* ✅ Anker USB-C PD chargers
* ✅ UGREEN USB-C PD chargers
* ✅ Baseus USB-C PD chargers
* ✅ Laptop USB-C PD chargers (Dell/Lenovo/HP, etc.)

Examples:

```
USB-C PD charger
        |
        | USB-C cable
        |
MacBook Air M2
```

The charger negotiates power automatically:

```
Charger: "I can provide 5V/3A, 9V/3A, 15V/3A, 20V/3.25A"
MacBook: "Give me 20V"
→ charging starts
```

A few caveats:

* A normal phone USB-C charger (5W–20W) will work, but charging will be slow.
* A USB-C charger without PD may not work properly.
* Cable matters:

  * For >60W charging, use a good USB-C cable rated for 60W/100W (usually marked E-marker).
  * Cheap USB-C cables may limit power.

For an M2 Air, a good 65W–67W GaN USB-C PD charger is usually the sweet spot: small, fast, and can also charge phones/tablets.
