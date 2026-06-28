---
audio: false
generated: true
image: false
lang: en
layout: post
title: Prestige Follows the Bottleneck
translated: false
type: note
---

Question: In the future, will semiconductor/foundry companies (TSMC, Micron, SK Hynix) and their employees/scientists become as prominent and high-exposure in society and social networks as FAANG employees — even though they were quite low-profile from 2010 to 2022?

Answer:

This is a prediction, so treat it as reasoned speculation, not fact. But the directional thesis is sound, and the mechanism is worth making precise.

**The core dynamic: prestige follows the bottleneck.**

Social prominence of a profession tracks where the scarce, value-creating constraint sits at a given moment.

- **2010–2022:** the bottleneck was *software/distribution*. Compute was cheap and abundant. The marginal dollar of value came from building apps, ad networks, and social graphs on top of commodity hardware. So FAANG software engineers got the prestige, the comp, and the cultural visibility (Silicon Valley TV show, "learn to code", etc.). Hardware was a solved, invisible substrate — TSMC just quietly made the chips.

- **2022–present:** the bottleneck moved to *compute itself*. Training frontier models is gated by GPUs, GPUs are gated by advanced nodes (3nm/2nm), advanced nodes are gated by TSMC, TSMC is gated by ASML's EUV, and the whole thing is gated by HBM (SK Hynix dominant, Micron/Samsung following). The constraint is now physical and concentrated in a handful of fabs.

So your intuition is right: **whoever owns the binding constraint accrues the prestige.** Nvidia already crossed over — Jensen Huang is a genuine celebrity now, Nvidia hit $3T+, and that was unthinkable in 2015 when it was "the gaming GPU company." The question is whether the *upstream* players (foundry, memory, litho) follow.

**Why the upstream players are already rising:**

- TSMC became geopolitically central — the "silicon shield," CHIPS Act, Arizona fabs, the most strategically important company most people couldn't name in 2018.
- HBM became *the* memory bottleneck for AI. SK Hynix went from a cyclical commodity DRAM maker to a structurally critical supplier with pricing power. That's a prestige re-rating.
- Process engineers, device physicists, and packaging specialists (advanced packaging / CoWoS is now a named bottleneck) are suddenly scarce and recruited aggressively.

**But here's the asymmetry you should account for — it won't be symmetric with FAANG:**

1. **Hardware prestige concentrates at the top, not across the rank-and-file.** FAANG made *the median engineer* culturally visible — a random L4 at Google had status. Semiconductor prestige is more likely to concentrate in a thin layer: the Jensen Huangs, the Morris Changs, a few star device physicists. A line process engineer at a fab works grueling shifts in a cleanroom and is unlikely to become a social-network archetype the way a SWE did. The work is less legible to the public and less individually attributable.

2. **The field is harder to enter, so it stays smaller.** You can self-teach web dev in a year (you did adjacent things). You cannot self-teach semiconductor process integration — it requires fab access, PhD-level device physics, and tacit institutional knowledge. Smaller funnel → less mass cultural footprint, but *higher* per-person scarcity prestige. Think "scientist" prestige (rare, respected, somewhat distant) rather than "FAANG engineer" prestige (aspirational mass career).

3. **Cyclicality undercuts cultural permanence.** Memory (Micron, SK Hynix, Samsung) is brutally cyclical. FAANG's prestige was reinforced by a decade of near-monotonic stock-price ascent and cushy comp. Memory makers swing through gluts and shortages. HBM has temporarily broken them out of the cycle, but if AI capex normalizes, the cultural shine dims faster than software's did.

4. **The real cultural winner is the layer that's both scarce *and* legible.** That's AI researchers and frontier-lab engineers right now — they have FAANG-style mass aspiration *plus* scientist-style prestige. Semiconductor folks get the scarcity but lose on legibility. Karpathy is famous; the TSMC N2 yield-ramp lead, who is arguably more irreplaceable, is not.

**Net prediction:**

- TSMC / SK Hynix / Micron *the companies* → yes, much higher exposure, geopolitical and financial prominence. Already happening.
- *Star individuals* (CEOs, a few celebrated technologists) → yes, celebrity-tier.
- *Median employee* → more respected and better paid than 2015, but unlikely to reach the mass-cultural-archetype status the median FAANG SWE had. More like the status of an aerospace engineer at SpaceX: cool, respected, scarce — but not a TikTok lifestyle genre.

**The deeper rule, stated as a principle** (this is the part useful for your own trajectory): prestige and exposure flow to *whoever sits on the currently-binding, hard-to-replicate constraint, weighted by how legible their contribution is to outsiders.* You're betting your career on the AI/compute stack, which is exactly where the constraint sits now. The maximally-leveraged position is not deep in the fab (scarce but illegible) nor pure app-layer (legible but abundant) — it's the **legible layer closest to the compute bottleneck**: model training, inference optimization, agent systems, AI-native tooling. Which is precisely where you've already pointed yourself.

One caveat to hold: constraints move. Software prestige peaked then compressed as compute became the bottleneck. If, say, energy or chip *supply* fully de-bottlenecks and algorithmic efficiency becomes the constraint, the prestige migrates again. Position for the *next* bottleneck, not just the current one.
