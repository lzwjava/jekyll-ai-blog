---
audio: false
generated: true
image: false
lang: en
layout: post
title: Scale Labs AI Leaderboards Overview
translated: false
type: note
---

Question: Provide an introduction to more leaderboards on https://labs.scale.com/leaderboard.

Answer: 

The page at **https://labs.scale.com/leaderboard** is the main **Scale Labs Leaderboards** hub by Scale AI. It serves as a central dashboard showcasing expert-driven benchmarks that test frontier AI models, agentic capabilities, reasoning, coding, tool use, safety, and more. The leaderboards evaluate over 100 models from major labs (OpenAI, Anthropic, Google, Meta, and open-source contributors) across 20+ rigorous, often real-world-oriented benchmarks.

Scale Labs focuses on challenging current AI limits with tasks that go beyond simple question-answering — emphasizing long-horizon agentic behavior, deep reasoning, honest/safe outputs, multimodal understanding, and professional-domain expertise.

### Key Highlighted Benchmarks (as of March 19, 2026)
Here are some of the prominent leaderboards available:

- **SWE Atlas - Codebase QnA**  
  Part of the **SWE Atlas** suite (next evolution of SWE-Bench Pro).  
  Focus: Deep code comprehension and reasoning in complex, real-world codebases.  
  Agents must explore repositories, run code in sandboxes, trace execution, and answer natural-language questions without modifying code.  
  Metric: Task Resolve Rate (% of tasks where the answer satisfies every expert rubric item perfectly).  
  Top models score only ~30–35%, showing this remains very hard.

- **MCP Atlas**  
  Evaluates real-world tool use via the **Model Context Protocol (MCP)**.  
  Involves 1,000 human-authored tasks (500 public), 36 real MCP servers, 220+ tools, and multi-step workflows (3–6 tool calls per task).  
  Tests realistic tool discovery, sequencing, cross-server composition, and conditional logic.  
  Top performance: ~62% pass rate (e.g., Claude Opus 4.5).

- **SWE-Bench Pro (Public Dataset)**  
  Long-horizon software engineering tasks (bug fixes, features) in public open-source repositories.  
  A foundational, widely respected benchmark for coding agents.

- **SWE-Bench Pro (Private Dataset)**  
  Similar tasks but in commercial-grade private/proprietary codebases — significantly harder.

- **Humanity's Last Exam** (and Text-Only variant)  
  Extremely difficult questions at the frontier of human knowledge.

- **SciPredict**  
  Forecasting outcomes of real scientific experiments.

- **Professional Reasoning Benchmark** (Finance and Legal)  
  Domain-specific professional reasoning tasks.

- **AudioMultiChallenge** (variants: Audio Output, Text Output)  
  Multi-turn spoken dialogue systems.

- **Remote Labor Index (RLI)**  
  Measures AI agents' ability to perform economically valuable remote work.

- **PropensityBench** / **MASK**  
  Safety & honesty benchmarks (simulating pressure to choose harmful behavior or lie).

- **VisualToolBench (VTB)** / **VISTA**  
  Multimodal: reasoning about and interacting with visual information.

- **MultiChallenge** / **MultiNRC**  
  Diverse, interdisciplinary, and multilingual reasoning challenges.

- **EnigmaEval**  
  Complex multi-step reasoning.

- **Fortress**  
  Frontier risk evaluation for national security and public safety (CBRNE, terrorism domains).

Many leaderboards use **percentage pass rates** or resolve rates with confidence intervals/standard deviations, and rankings often incorporate statistical significance (e.g., Rank Upper Bound).

The page includes direct links to individual leaderboards, model rankings (with top performers like gpt-5 variants, Claude Opus 4.x, etc.), and often links to datasets (Hugging Face), papers, or announcements. It reflects Scale AI's push toward more realistic, outcome-focused evaluations of agentic AI.

For the latest rankings and full details, visit the main page directly, as scores evolve with new model releases.

References:  

- [Scale Labs Leaderboards Main Page](https://labs.scale.com/leaderboard)
- [SWE Atlas - Codebase QnA Leaderboard](https://labs.scale.com/leaderboard/sweatlas-qna)
- [Scale AI Blog: Can Coding Agents Become Engineers? We're Finding Out.](https://scale.com/blog/swe-atlas)
- [MCP Atlas Leaderboard](https://labs.scale.com/leaderboard/mcp_atlas)