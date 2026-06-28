---
audio: false
generated: true
image: false
lang: en
layout: post
title: How Lisa Su Saved AMD
translated: false
type: note
---

Question: How did Lisa Su save AMD?

Answer:

Lisa Su took over as CEO in October 2014 when AMD was near death — stock around $2-3, roughly $1B in debt, and shrinking against Intel and Nvidia. Here's the actual turnaround mechanics.

**1. Bet everything on one architecture: Zen.** Before Zen, AMD's Bulldozer architecture was a disaster — high core counts but terrible IPC (instructions per cycle), losing badly to Intel's Core lineup. Su redirected scarce R&D money into a clean-sheet design led by Jim Keller. Zen (2017) delivered ~52% IPC improvement over the prior generation, which was an enormous single-generation jump. This is the single most important technical decision of the turnaround.

**2. Chiplets — the structural insight.** This is the part worth understanding deeply. Instead of building one large monolithic die, AMD split the CPU into small chiplets (CCDs) connected by Infinity Fabric, with a separate I/O die. Why this matters economically:

- Yield scales badly with die area. Defects per wafer are roughly Poisson-distributed, so a big die has a much higher chance of containing a killer defect. Smaller chiplets → dramatically better yield → lower cost per working chip.
- You can mix process nodes — compute chiplets on cutting-edge TSMC nodes, cheap I/O die on an older node.
- One chiplet design scales from desktop (Ryzen) to server (EPYC) to threadripper just by changing how many you package. Massive design-cost amortization.

This let a cash-starved company out-economize Intel, whose monolithic dies on a stuck 10nm process were hemorrhaging yield. AMD essentially won on packaging strategy, not just transistors.

**3. Outsource fabrication to TSMC.** Su leaned fully into being fabless, riding TSMC's process leadership (7nm, then 5nm) while Intel's own fabs stalled at 14nm/10nm for years. This decoupled AMD's competitiveness from its own manufacturing — a structural advantage during exactly the window Intel stumbled.

**4. EPYC and datacenter margins.** Consumer Ryzen rebuilt the brand, but the profit came from EPYC server chips. Chiplets gave AMD up to 64 cores per socket when Intel was stuck far lower, and datacenter carries the high margins that funded everything else. AMD went from ~2% server share to a major player.

**5. Discipline and focus.** She killed distractions, paid down debt, and kept the company executing on a tight multi-year roadmap that it actually hit on time — rare in semiconductors.

Result: stock from ~$2 (2014) to well over $100, market cap crossing Intel's at points, and now AMD is the credible #2 in AI accelerators with MI300X/MI300A — the exact hardware you're training GPT-2 on. Given you're running workloads on an MI300X (192GB HBM3), you're directly downstream of this turnaround: AMD only has a serious datacenter GPU business because the Zen/chiplet/TSMC strategy generated the cash and credibility to fund Instinct.

The meta-lesson for a builder: AMD didn't win by beating Intel at Intel's game (monolithic dies, in-house fabs). It changed the axis of competition — chiplets and fabless leverage — where its constraints became advantages. That's a first-principles re-architecture move, not an incremental one.
