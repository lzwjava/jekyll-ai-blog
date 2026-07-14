---
audio: false
generated: true
image: false
lang: en
layout: post
title: Best mATX Case for MI50 AI Build
translated: false
type: note
---

Question: What chassis fits this build (MI50 16GB + R5 5600 + B550M mATX + 750W PSU)?

Answer:

Case choice here is driven by three constraints from what you've already picked, not by aesthetics:

1. **GPU length + shroud clearance** — MI50 stock length is ~267mm, but once you bolt on a fan shroud (from the last step), plan for 300-320mm of clearance minimum
2. **Airflow, not just fan count** — the MI50's cooling depends entirely on case intake feeding its shroud fan; a case that's mostly solid panels with weak front mesh starves it regardless of how good your shroud fan is
3. **mATX board = don't overpay for ATX-sized case** — but don't go too small either, since sustained inference load (not gaming bursts) means thermals compound over hours, not seconds

**Two real options depending on how you'll actually run this:**

**Option A — Standard closed case, mATX mid-tower with mesh front.** Best if this sits in a room with you, needs to look normal, occasional noise matters.

- Look for: full mesh front panel (not just vents), supports 3x120mm or 2x140mm front intake, GPU clearance ≥320mm, CPU cooler height clearance ≥165mm (matches the Peerless Assassin 120 SE recommended earlier), PSU shroud with enough depth for a standard ATX unit
- Candidates on JD: Deepcool CK560 mATX / MATREXX 55 Mesh, Segotep Kratos/Hall series mATX, Jonsbo D31 mesh — all sub-¥400, mesh-heavy, decent airflow for this exact use case

**Option B — Open-air/mining-style frame.** Better if this is a dedicated inference box in a closet/rack, noise doesn't matter, you want zero airflow restriction and easy access for the fan shroud mod / future GPU swaps.

- No case walls means the shroud fan and CPU cooler get unrestricted ambient air — genuinely better thermals for sustained load than any closed case
- Downsides: dust exposed, not presentable in a living space, need a flat surface/shelf
- Candidates: generic 6-8 slot open mining frames (~¥100-150 on Taobao), just confirm mATX board mounting holes are supported

**My actual recommendation for you:** given you're running this as an AI company inference/training box likely near a desk, not in a server closet — go **Option A, mesh-front mATX mid-tower**. It balances thermals for the passive-turned-active-cooled MI50 with something you can actually keep in your workspace.

**Concrete pick:** Deepcool CK560 mATX (mesh front, ~¥300-350, GPU clearance 380mm+, supports up to 165mm CPU cooler) or Jonsbo D31 mesh if you want tempered glass side + mesh front hybrid.

One thing to verify before buying: your PSU listing says "14CM" (compact length) — that's good, it means it'll fit even in shorter mATX cases without competing with the GPU for depth, so you have more case options than a build with a longer 750W unit would.
