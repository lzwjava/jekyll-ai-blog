---
audio: false
generated: true
image: false
lang: en
layout: post
title: 20-pin to 24-pin Power Connection
translated: false
type: note
---

**Question:** I have a Huntkey 280W PSU with a 20-pin connector, but the Lenovo L-IG41M3 motherboard has a 24-pin main power connector. How do I connect them?

---

**Answer:**

You have **two options**:

---

### ✅ Option 1: Plug the 20-pin directly into the 24-pin slot (simplest)

You can plug a 20-pin cable directly into a 24-pin motherboard slot — it will physically fit on one side, leaving 4 pins empty. This works as long as the motherboard's power draw is low enough. If the board draws too much current through only 20 pins, it can overheat those pins over time.

The **L-IG41M3** is an older Intel G41 board designed for low-power LGA775 CPUs — it draws very little power, so this is generally safe **if**:

- You are using **integrated graphics** (no discrete GPU)
- You have a **low-power CPU** (Core 2 Duo / Celeron)

**How to align it:** The 20-pin connector plugs into the **first 20 pins** of the 24-pin slot. Match the latch/clip side. The 4 empty pins will be on one end — that is normal.

---

### ✅ Option 2: Use a 20-pin to 24-pin adapter cable (recommended)

A 20-pin to 24-pin ATX adapter cable lets the 20-pin PSU work properly on a 24-pin motherboard, using standard 18AWG copper wire rated at 300V for stable and safe use.

These adapters cost around **$8–$20** and are widely available. Simply:

1. Plug the adapter's 20-pin female end into your Huntkey PSU cable
2. Plug the adapter's 24-pin male end into the motherboard

---

### ⚠️ Important Caution

The extra 4 pins were added to ATX24 to provide additional current-carrying capacity, particularly for PCIe. If you add a discrete GPU, the 20-pin connection may not be sufficient and could overheat.

Also, a 280W PSU is already quite limited — avoid adding a dedicated graphics card.

---

**References:**

- [PSU 20-pin to 24-pin adapter — Tom's Hardware Forum](https://forums.tomshardware.com/threads/psu-20-pin-to-24-pin-adapter-how-well-do-they-work.2851575/)
- [ATX 20-pin to 24-pin Connection Guide — smps.us](https://www.smps.us/20-to-24pin-atx.html)
- [20-pin to 24-pin adapter cable — Newegg](https://www.newegg.com/p/1EF-023W-004X3)
