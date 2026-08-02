---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Flattens Middle Management
translated: false
type: note
---

Question: Will GMs/middle managers get squeezed out in the AI era while strong ICs rise?

Answer: Yes, directionally — but it's more specific than "managers bad, engineers good." The data backs the core thesis, and the mechanism matters more than the conclusion.

**What's actually happening (2024–2026 data):**
- Amazon: Jassy mandated a 15%+ IC-to-manager ratio increase by Q1 2025, hit it by March, mostly through merging teams rather than mass layoffs.Amazon offers the sharpest recent example: CEO Andy Jassy told employees the company would increase the ratio of individual contributors to managers by at least 15 percent by the end of the first quarter of 2025, writing that having fewer managers would remove layers and flatten the organization.
- Gartner: through 2026, one in five organizations will use AI to flatten their organizational structure, eliminating more than half of current middle management positions.
- Meta went from "20+ direct reports, 20% coding time" mandate to full flattening by 2026.Engineering managers were told they needed 20 or more direct reports and to spend at least 20% of their time coding. Thousands were given a choice: move to an individual contributor role, or leave.

**Why this hits GM/middle layer specifically, not senior engineers:**
The work that gets automated is *coordination*, not judgment. The logic is that AI can automate scheduling, reporting, and performance monitoring, the administrative core of many management jobs, so each remaining leader can supervise a far larger team. That's exactly the job description of a GM who translates between eng, product, and business — synthesize, status-report, escalate. An agent can draft the status report and summarize the standup. It can't debug your distributed system at 2am or make the call on a technical tradeoff nobody else understands deeply enough to arbitrate.

This maps to your own experience: you went from 30K-user Fun Live founder to running an AI company that trains models and builds CLI agents. That's the "player-coach with 10x leverage" pattern winning over "coordinator of 8 people who coordinate 8 people."

**The counter-risk, and it's real:** Middle managers are absorbing increased AI-related workloads without added support, potentially eliminating crucial development pathways for future leaders. Flattening now means fewer people learn org-scale judgment later. So "good engineers rise" only holds if those engineers actually develop the judgment/mentorship/architecture-level thinking that used to get trained into managers. If they just become bigger ICs who ship more code with Claude/Codex but never learn to make the hard calls, you get a different failure mode in 5 years — no one left who can run a 200-person org.

**Bottom line for someone in your position:** the moat isn't "IC vs manager," it's "can you make judgment calls an LLM can't and can't be trusted with." Training GPT-2 760M on MI300X and shipping agent CLIs (ww/iclaw/zz) — that's exactly the kind of irreducible, first-principles work that survives flattening. Pure coordination roles don't.

References:
- [The Middle Manager Isn't Dead, But the Job Is Changing Fast](https://www.metaintro.com/blog/middle-manager-role-changing-ai-flattening-2026)
- [Management Cuts Today Are Shaping A Leadership Shortage](https://www.forbes.com/sites/cindyrodriguezconstable/2026/06/30/management-cuts-today-are-shaping-a-leadership-shortage/)
- [Flattening org charts: Bayer, Amazon, Meta](https://www.heypinnacle.com/blog/end-of-middle-managers-2026)