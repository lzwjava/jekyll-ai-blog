---
audio: false
generated: true
image: false
lang: en
layout: post
title: Clean and Apply CPU Thermal Paste
translated: false
type: note
---

**Question:** How do you clean off old thermal paste and apply new thermal paste to a CPU?

**Answer:**

Here's a complete step-by-step guide:

---

**What You'll Need**
- Isopropyl alcohol (90%+ concentration, 99% preferred)
- Lint-free cloth or coffee filters (avoid paper towels — they leave fibers)
- Plastic card or scraper (optional)
- New thermal paste (e.g., Arctic MX-6, Noctua NT-H1, Thermal Grizzly Kryonaut)
- Anti-static wrist strap (recommended)

---

**Step 1 — Power Down & Disassemble**
Shut down your PC, unplug the power cable, and press the power button once to discharge residual electricity. Remove the CPU cooler by unscrewing it carefully. Set it aside on a clean surface.

**Step 2 — Remove Old Thermal Paste from the CPU**
Use a dry lint-free cloth to wipe off the bulk of the old paste first. Then apply a small amount of 90%+ isopropyl alcohol to a clean cloth or coffee filter and gently rub the CPU heat spreader in circular motions. Repeat until no residue remains. Let it dry completely (30–60 seconds).

**Step 3 — Clean the Cooler Contact Plate**
Do the same for the bottom of the cooler (the part that touches the CPU) — wipe off old paste with a dry cloth first, then clean with isopropyl alcohol until it's shiny and residue-free.

**Step 4 — Apply New Thermal Paste**
There are a few common methods — the **pea/dot method** is most recommended for most CPUs:

| Method | Best For |
|---|---|
| Pea/dot (rice-grain sized dot in center) | Most CPUs (Intel, AMD) |
| X pattern | Larger IHS (e.g., Threadripper, HEDT) |
| Thin spread (with card) | Flat, uniform coverage preferred |

Place a pea-sized dot (~3–4mm) in the **center** of the CPU. You don't need to spread it — the cooler's pressure will do this when mounted.

**Step 5 — Remount the Cooler**
Lower the cooler straight down onto the CPU without sliding it around (sliding spreads paste unevenly). Tighten screws in a **diagonal/cross pattern** (e.g., top-left → bottom-right → top-right → bottom-left) to ensure even pressure. Don't overtighten.

**Step 6 — Test**
Boot up and check CPU temperatures using a tool like **HWMonitor** or **Core Temp**. Idle temps should be reasonable (30–50°C for most systems). Run a stress test (Prime95, Cinebench) to confirm cooling is working properly.

---

**Tips**
- Less paste is better than more — excess paste can spill onto the motherboard socket.
- Never use rubbing alcohol below 90% — the water content can damage components.
- Allow the system to run a few heat cycles before judging final temperatures, as some pastes need a "burn-in" period.

---

**References:**
- [How to Apply Thermal Paste — Arctic](https://www.arctic.de/en/learn/thermal-paste-application)
- [Thermal Paste Application Methods Compared — Linus Tech Tips](https://www.youtube.com/watch?v=ZEP0OK8RLQE)
- [Best Thermal Pastes 2024 — Tom's Hardware](https://www.tomshardware.com/best-picks/best-thermal-paste)
