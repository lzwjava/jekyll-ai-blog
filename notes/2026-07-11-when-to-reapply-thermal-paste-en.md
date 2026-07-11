---
audio: false
generated: true
image: false
lang: en
layout: post
title: When to Reapply Thermal Paste
translated: false
type: note
---

**Question:** When a liquid cooler's cold plate sits on the CPU, the thermal paste ("glue") hardens over the years — do we need to reapply it?

**Answer:**

Yes. That's thermal paste (not glue — no adhesive bonding happens, it's just a thermal interface material squeezed between two flat metal surfaces to eliminate air gaps).

**Why it degrades:**
- Most stock/bundled pastes (including whatever ships with the Frozen Prism 240) use silicone-based carriers with metal-oxide fillers. Over 2-4 years of thermal cycling (heat up → cool down, repeated thousands of times), the silicone oil "pumps out" from the edges and the paste dries, cracks, and loses contact with microscopic surface imperfections.
- Symptom: idle temps stay normal-ish, but load temps creep up 10-15°C over a year or two for no software reason. On a 13900KF (253W PL2), this matters a lot — that chip already runs hot under all-core load, so a degraded TIM layer pushes you into thermal throttling territory (100°C+ under sustained AVX workloads, e.g. training/quantization scripts on CPU).

**Practical schedule:**
- Reapply every 1-2 years for a 13900KF specifically, since it's a high-TDP chip that thermal-cycles hard under your kind of workload (compiling, running local inference, GPU-adjacent CPU-bound preprocessing).
- Signs it's time now: check idle vs load delta. If load temps under something like `stress-ng --cpu 32 --timeout 300s` (or just Prime95/AIDA64 if you're on a GUI) creep past ~95°C sustained, or if you haven't touched it in 2+ years, just redo it — cheap insurance.

**How to redo it (since your build is fresh, you won't need this for a while, but for reference):**
```bash
# not code, but the mechanical steps:
1. Power off, unplug, unmount the AIO cold plate (4 screws, diagonal loosening pattern)
2. Clean old paste off CPU IHS and cold plate with isopropyl alcohol (>90%) + lint-free cloth/coffee filter
3. Apply new paste: pea-sized dot in center (for the 13900KF's rectangular die layout under IHS,
   a thin X or 5-dot pattern spreads more evenly across the two die clusters — P-cores and E-cores
   are physically separated on this chip)
4. Remount, torque screws diagonally (star pattern), don't overtighten — AIO backplates usually have
   spring-loaded standoffs, so just snug is enough
```

**One thing to actually check on your build:** the Frozen Prism 240 is a budget-tier AIO (413 CNY). Pairing it with a 253W-TDP 24-core chip is workable but tight — expect to see throttling under sustained all-core loads (like local LLM inference on CPU, or long compile jobs) even with fresh paste, since 240mm radiators are typically rated for ~250-280W sustained dissipation depending on fan curve and ambient. If you're running CPU-heavy AI workloads regularly, watch your temps with `sensors` (lm-sensors on Linux) or HWiNFO, and consider a 360mm AIO if you hit thermal throttle walls often.
