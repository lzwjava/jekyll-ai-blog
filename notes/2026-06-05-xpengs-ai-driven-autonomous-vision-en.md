---
audio: false
generated: true
image: false
lang: en
layout: post
title: XPeng's AI-Driven Autonomous Vision
translated: false
type: note
---

**Question:** Provide a comprehensive description of Liu Xianming's vision and approach at XPeng based on the full interview.

**Answer:**

This interview reveals Liu Xianming's radical bet on simplification in autonomous driving, driven by a fundamental shift in thinking triggered by ChatGPT.

## The Catalyst: ChatGPT's Proof of Concept

In late 2022 at Cruise, Liu witnessed a 90-minute driverless robotaxi run in San Francisco with zero intervention. When Sam Altman visited for an internal talk, the team bragged about this achievement, but Altman was focused on something else: GPT, which would become ChatGPT months later. Liu was struck—he realized autonomous driving could follow the same path: simple architecture + massive scale + sufficient data and compute = emergent intelligence, without hand-coded rules or five lidars with street trees trimmed.

## VLA 2.0: Removing Language as Bottleneck

The core innovation: Instead of building on open-source language models with vision data (which creates a language bottleneck where the model converts visual input → language tokens → driving actions with latency bottlenecks), XPeng's second-gen VLA directly maps sensor input to driving actions without language translation.

This is not "no language," but removing it from the **inference pipeline**. Language still handles user intent and voice commands on input, but the core reasoning loop—what humans do instinctively when driving without verbalization—is purely visual-to-action.

**The Breakthrough Moment:** In May 2024, a small team "secretly" removed the language module from the first-gen VLA while keeping its name. They scaled up to the largest GPU cluster available and retrained with more data. After a few weeks, performance improved dramatically. The team initially distrusted this direction, so the experiment proved feasibility before full commitment.

## Extreme Simplicity as Engineering Principle

When asked what still needs to be removed, Liu responded: "Nothing, we're at bone-structure already." The philosophy is radical engineering extremism—the secret is "ultimate engineering rigor." AI's foundation is precisely that.

The architecture is deliberately minimal because complex models don't work well; everyone's current AI architectures are already extremely similar and simple. The competitive advantage is iteration speed, not fancy model structures. By iterating daily (theoretically 4 versions/day), they discover new problems faster and try new structures that other teams lack time to explore.

## The Data Strategy: Quality Over Quantity

XPeng maintains 50 PB of data, but Liu emphasizes that raw data volume is meaningless. Early on, 90%+ of data was straight-line highway driving, so adding a U-turn would break the model. Using 200 trained drivers vs. 1M drivers is entirely different—200 drivers can't cover enough scenarios, and professional-driver data often comes from artificial scenarios (staged maneuvers), not real-world distribution.

The key insight: Data collection must be like a dense, random sampler of the real world. Only then can the model achieve true generalization and handle previously unseen situations.

The hardest problem is data curation—identifying which data points are outliers worth learning from vs. "dirty data" to discard. Meta struggles with this too. The paradox: an anomaly is only recognizable because it's not in your training set, but if it's rare in small scale, it might be garbage. Solving this requires continuously expanding the data frontier with time.

## The "No Rules" Conviction

During testing, the model failed at tasks like hitting curbs or staying centered. The team faced pressure to add rule-based post-processing. Liu refused: "Once you add rules, the system's character changes and you can't remove them. Before the model ships, it must expose problems fully. Rules hide problems and kill the ability to discover them. It's like building a road that never leads to the future."

He refused navigation shortcuts: if the model makes wrong turns, adding lane-level navigation (e.g., force a right turn at 300m before exit) seems pragmatic, but it makes navigation a crutch. For global products like European markets without high-def maps, this crutch fails. Instead, the solution is reinforcement learning—teach the model through reward signals what to do at merges and red lights, without constraining the search space with rules.

## Scaling Beyond Data: System-Level Scaling

When Liu joined, GPU utilization was only 8% despite complaints about insufficient cards. He recognized the real constraint wasn't hardware but training efficiency. By optimizing to 40% utilization (5x improvement), he solved the bottleneck—then, resource decisions shifted from "add more cards" to "which business lines can wait, what can be cut, how to allocate across the portfolio".

Scaling is multidimensional: not just data scaling, but model scaling and infrastructure scaling as a system. Any bottleneck kills the entire strategy—you can't catch up in half a year. This requires the right people doing hard engineering (profiling, dashboards), unified team understanding, proper pacing (no rushing or complacency), and scientific methodology grounded in data, not slogans.

## The Test-Time Scaling Connection: CoT for Driving

In VLA's world model (which can predict future road states and vehicle behavior), Liu applies Chain-of-Thought scaling. Rather than scaling laws working only at training time, test-time scaling—consuming more compute at inference—also improves reasoning. Vision-CoT is test-time scaling: generate intermediate visual states (visualized as "inner monologues" called "mind theater"), predict the next action with multiple hypotheses (enabling reinforcement learning exploration), and return the best result.

## The Budget Reality

He is the biggest spender at XPeng. In early conversations with He Xiaopeng, he presented a vision requiring massive resources. He Xiaopeng asked, "Enough?" Liu said not quite. They rewrote it as the "grand vision version" with 2x budget—He approved immediately.

In 2025, XPeng's public AI R&D budget was 4.5 billion yuan. He Xiaopeng publicly said: "For over a dozen months, spending 300 million per month betting on this—I was panicking inside."

## The Crisis and He Xiaopeng's Faith

During VLA 2.0 testing, problems multiplied daily—hitting curbs, poor centering, countless edge cases. Morale was "devastating." Liu admits: "I didn't dare return home for a while. I was supposed to demo in May, but instead boarded a flight to the US without telling my boss until on the plane."

In January, with launch scheduled for February, He Xiaopeng called: "This isn't good. You're fixing the floor, but the ceiling is completely unreleased. Give me two more months—what can you do?" Liu replied: "Boss, I'll change the architecture." He Xiaopeng approved. The next day they restructured and retrained. By March, it shipped.

Liu reflects: "He's remarkably tolerant of research breakthroughs—not short-termist, not impatient. Yet brutal on principles: right is right, wrong is wrong. Many CEOs claim to believe in tech breakthroughs but can't tolerate 6 months of slow progress. That's what I most admire about him."

## The L2 → L4 Thesis

Critics argue L2 assistance cannot reach L4. Liu disagrees: scaling laws and foundational vision-language-action models enable the path. VLA 2.0's minimalist architecture—sensor input → trajectory output—scales across model, data, and compute. Imitation learning's ceiling breaks with scaling; world models and reinforcement learning enable the model to self-evolve and handle corner cases.

At Cruise, the old stack was pure rules: lidar point clouds → detection → rules execution → trajectory optimization. The car got stuck when tree branches covered the lidars; Cruise had to trim the entire street. The 2019 pivot introduced the "Continuous Learning Machine"—building generic, simple model frameworks.

## The Physical AI Vision

Liu positions autonomous driving as the start, not the endpoint. He doesn't believe the autonomous driving space has plateaued—he believes physical AI is just beginning. The core choice is: are you building autonomous driving algorithms (possibly near saturation) or physical AI?

**The Bet at XPeng:**

Liu signed a concrete wager with He Xiaopeng: by late August 2024, XPeng's VLA 2.0 must reach Tesla FSD V14's level in Silicon Valley, or Liu will run naked across the Golden Gate Bridge.

## Technical Lineage

Liu's philosophy traces to his PhD advisor Thomas Huang (黄煦涛), whose lifetime creed was simplicity—"simple things are beautiful." In 2012, when AlexNet arrived, Huang told the lab to abandon all work and pivot to neural networks. Most in industry rejected the shift; they didn't dare. Liu was among the early believers in data and model scaling.

---

**Key Takeaway:**

Liu's philosophy is: **eliminate every intermediary step** (language translation in driving), **scale relentlessly** across model, data, and infrastructure as a unified system, **refuse shortcuts** even when tempting, and **iterate at extreme speed** to discover problems and solutions. This is not Transformer-scale innovation—it's engineering extremism grounded in first principles.
