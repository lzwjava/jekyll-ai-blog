---
audio: false
generated: true
image: false
lang: en
layout: post
title: GDPval-AA v2 Agentic Eval
translated: false
type: note
---

Question: What is GDPval-AA v2 in LLM evaluation?

Answer: It's Artificial Analysis' second-gen harness built on top of OpenAI's original GDPval dataset.

**Base dataset (OpenAI, Oct 2025):** 220 tasks constructed from the representative work of industry professionals with an average of 14 years of experience, covering the majority of U.S. Bureau of Labor Statistics Work Activities for 44 occupations across the top 9 sectors contributing to U.S. GDP.

**What AA added (v2):** They don't just score against a rubric — models get shell access and web browsing in an agentic loop (via their "Stirrup" harness) to solve tasks, producing real deliverables — documents, slides, diagrams, spreadsheets. Scoring is blind pairwise: two model outputs get anonymized, an LLM judge picks a winner, and results aggregate into an Elo rating — same idea as LMArena/Chatbot Arena Elo but for agentic knowledge-work output instead of chat turns.

Key mechanics:
- Elo is anchored so **human-expert baseline ≈ 1000**
- It's a moving leaderboard — new model entries shift everyone's Elo since it's relative
- At v2 launch (mid-June 2026), Claude Fable 5 / Opus 4.8 / GPT-5.5 were top-ranked; current top per the datalearner scrape shows Kimi K3 and Gemini 3.6 Flash in the mix — the board moves fast, check the live link below rather than trust any snapshot.

Why it matters more than MMLU-style benches for your use case: it's grading **file-based agentic output** (spreadsheets, decks, memos) under tool use, which is a lot closer to what your CLI agents (ww/iclaw/zz) actually need to be good at than a multiple-choice eval is.

References:
- [GDPval-AA v2 Leaderboard — Artificial Analysis](https://artificialanalysis.ai/evaluations/gdpval-aa)
- [GDPval original paper (OpenAI, arXiv)](https://arxiv.org/abs/2510.04374)
- [GDPval-AA v2 benchmark writeup](https://systems-analysis.ru/eng/GDPval-AA_v2)