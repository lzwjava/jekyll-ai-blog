---
audio: false
generated: true
image: false
lang: en
layout: post
title: Testing a Huntkey PSU
translated: false
type: note
---

**Question:** I have a Huntkey 航嘉 睿智 300S PSU and I have the connector for power (24-pin ATX). How can I test whether this PSU is functional or not?

**Answer:**

The 睿智 300S is a budget ATX PSU (rated ~200W). Since you already have the connector, you can test it using the classic **Paperclip / Jumper Test**. Here's how:

---

### ⚠️ Safety First

- Never touch any exposed pins while the PSU is powered on.
- Don't leave a jumpered PSU running unattended.
- Always unplug the AC cord **before** inserting or removing the paperclip.

---

### Method 1 — Paperclip Test (Basic, Free)

This is the simplest way to check if the PSU can power on at all.---

### Method 2 — PSU Tester (More Thorough, ~$12–20)

A dedicated PSU tester automates the paperclip test and adds a quick readout of each rail's voltage on an LCD screen. Budget LCD models run around $12–$20. Just plug the 24-pin connector into the tester and power on — it checks all voltage rails (+12V, +5V, +3.3V) at once.

---

### Method 3 — Multimeter (Most Accurate)

If the fan spins but you still want to verify voltage output, use a multimeter set to DC voltage. Probe the output connectors (e.g., a Molex or SATA power plug) against ground (black wire). Expected values:

| Rail | Wire Color | Expected Voltage |
| ------ | ----------- | ----------------- |
| +12V | Yellow | 11.4V – 12.6V |
| +5V | Red | 4.75V – 5.25V |
| +3.3V | Orange | 3.14V – 3.47V |

---

### Quick Summary

| Test | Cost | What it tells you |
| ------ | ------ | ------------------ |
| Paperclip | Free | Can it power on at all? |
| PSU Tester | ~$15 | Are all voltage rails present? |
| Multimeter | ~$15–30 | Are voltages within spec? |

If none of the fans kick on after the paperclip test, the PSU is at fault. If the fan does spin, it's still possible the PSU is bad, but it's more likely another component in the system may have failed.

---

**References:**

- [NZXT: Testing your PSU (Paperclip Test)](https://support.nzxt.com/hc/en-us/articles/1260802863490-Testing-your-Power-Supply-Unit-Paperclip-Test)
- [Corsair: How to Test a PSU](https://www.corsair.com/us/en/explorer/diy-builder/power-supply-units/how-to-test-a-psu-power-supply-unit/)
- [Tech-Insider: How to Test a Power Supply (2026)](https://tech-insider.org/how-to-test-a-power-supply-2026/)
- [Huntkey 睿智 300S Product Page](https://www.huntkey.cn/product/product_id=452.html)
