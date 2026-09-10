---
audio: false
generated: true
image: false
lang: en
layout: post
title: Free Diagnostics First Before Buying
translated: false
type: note
---

Question: Should you buy another DDR4 stick to continue diagnosing?

Answer: **Not yet.** There are still free diagnostics to exhaust first.

---

## Do These First (Cost $0)

### 1. Clear CMOS

```
Power off → unplug PSU → remove CMOS battery 60s → reinstall → POST
```

Rules out stale XMP / bad BIOS memory config entirely.

### 2. Inspect LGA1151 Socket Pins

- Remove CPU cooler + CPU
- Use phone camera **macro mode** under bright light
- Look for any pin leaning at a different angle than its neighbors

This costs nothing and could reveal the actual fault immediately.

### 3. Clean RAM Contacts

- Remove the GAMER II stick
- Gently erase the gold contacts with a **pencil eraser**
- Reseat firmly in each slot, one at a time

---

## When Buying a Test Stick Makes Sense

Only consider it **after** the above steps if:

| Condition | Verdict |
| --- | --- |
| CMOS clear changed nothing | Buy makes sense |
| Socket pins look clean and straight | Buy makes sense |
| You genuinely suspect the GAMER II stick | Buy makes sense |

A cheap used DDR4 stick (4GB, any speed) costs roughly **$5–10 USD** on eBay/Facebook Marketplace locally — it's a reasonable last diagnostic tool before concluding the board or CPU is damaged.

---

## Honest Assessment

The **CPU↔DRAM cycling in one slot + DRAM stall in another** is an unusual asymmetric pattern. That asymmetry is more consistent with:

- A **bent socket pin** affecting one memory channel
- A **slot trace fault** on the motherboard
- Less likely: the RAM stick itself (which would usually fail the same way in both slots)

**So inspect the socket first** — if a pin is visibly bent, buying RAM won't fix it.
