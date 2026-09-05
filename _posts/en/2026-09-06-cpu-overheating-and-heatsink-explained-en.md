---
audio: false
generated: true
image: false
lang: en
layout: post
title: CPU Overheating and Heatsink Explained
translated: false
type: note
---

**Question:** How does the CPU know it is overheating, and what exactly is a heatsink?

---

**Answer:**

---

### 🧠 What is a Heatsink?A **heatsink** is a metal block (usually aluminum or copper) that sits **directly on top of the CPU**. Its job is to absorb heat from the CPU and spread it away into the air. It has fins on top to increase surface area, and usually a fan on top to blow air through those fins

```
      [ FAN ]
   ___________
  |  | | | |  |   ← metal fins
  |___________|
  |  flat base |   ← sits on CPU
       ↕
   [  CPU  ]
```

The **thermal paste** (grey/silver sticky compound) is applied between the CPU surface and the heatsink base to **fill microscopic air gaps** — because air is a poor heat conductor, and even metal surfaces are not perfectly flat.

------

### 🌡️ How Does the CPU "Know" It Is Overheating?

Modern CPUs have a built-in **digital temperature sensor** called a **TJ (Thermal Junction) sensor** or **DTS (Digital Thermal Sensor)** — it is a tiny circuit baked right into the CPU chip itself. It constantly measures temperature in real time.

Here is what happens step by step:

```
CPU gets hot
     ↓
Internal TJ sensor reads temperature
     ↓
Temperature reaches warning threshold (~90–100°C)
     ↓
CPU signals the motherboard via PROCHOT# pin
     ↓
Motherboard triggers immediate shutdown
     ↓
Fan flashes briefly → system dies
```

This safety mechanism is called **Thermal Throttling / Thermal Protection** — it exists to prevent the CPU from physically burning out.

---

### ⚡ Why Does It Happen So Fast (Within 1 Second)?

If the heatsink is:

- **Not making contact** with the CPU (installed backwards, or clips not locked)
- **Missing thermal paste** (air gap between CPU and heatsink)
- **Dry old thermal paste** (crumbled and not conducting heat)

Then the CPU gets **no cooling at all**. Even at idle, the CPU generates enough heat to reach dangerous temperatures **within less than one second** — the sensor fires immediately and shuts everything down before any damage occurs.

---

### 🔧 What You Should Check

| Check | What to Look For |
| --- | --- |
| Heatsink clips | All 4 push-pins must be fully locked down |
| Heatsink contact | Bottom of heatsink must be flat against CPU top |
| Thermal paste | Should be a thin even layer — not too much, not missing |
| Old dried paste | Grey/white crumbly residue = replace it |
| Fan connected | CPU fan header must be plugged into motherboard |

---

### 🧪 Simple Test

Remove the heatsink, clean off old thermal paste with isopropyl alcohol, apply a small **pea-sized drop** of fresh thermal paste in the center of the CPU, reseat the heatsink firmly, and try again.

---

**References:**

- [What is a CPU Heatsink? — computerhope.com](https://www.computerhope.com/jargon/h/heatsink.htm)
- [How CPU Thermal Protection Works — Intel ARK](https://www.intel.com/content/www/us/en/support/articles/000005597/processors.html)
- [How to Apply Thermal Paste — Tom's Hardware](https://www.tomshardware.com/how-to/how-to-apply-thermal-paste)
