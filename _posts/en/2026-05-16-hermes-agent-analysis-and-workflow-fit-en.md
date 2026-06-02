---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Agent Analysis and Workflow Fit
translated: false
type: note
---

Question: What are your thoughts on Hermes Agent — its features, philosophy, comparison with Claude Code (CC), the plagiarism controversy with the Chinese team EvoMap, and how it fits into a personal workflow that favors open-source, HuggingFace, Chinese models (like GLM), and custom CLI tooling?

Answer:

## Hermes Agent — A Comprehensive Assessment

### What Hermes Agent Actually Is

Hermes Agent is an open-source autonomous AI agent built by Nous Research, released in February 2026. It is not a coding copilot tethered to an IDE or a chatbot wrapper around a single API — Hermes lives on your server, remembers what it learns, and gets more capable the longer it runs.

It supports any model you want — Nous Portal, OpenRouter (200+ models), z.ai/GLM, Kimi/Moonshot, MiniMax, Hugging Face, OpenAI, or your own endpoint. You can switch with `hermes model` — no code changes, no lock-in. This multi-model openness is one of its strongest practical advantages for your GLM + HuggingFace-first workflow.

---

### Key Features Worth Noting

- **Subagents**: Spawn isolated subagents for parallel workstreams. Programmatic Tool Calling via `execute_code` collapses multi-step pipelines into single inference calls.
- **Persistent memory + self-improving skills**: Agent-curated memory with periodic nudges; autonomous skill creation after complex tasks; skills self-improve during use.
- **Platform reach**: Lives where you do — CLI, Telegram, Discord, Slack, WhatsApp, Signal, Matrix, DingTalk, Feishu, WeCom, and more — 20+ platforms from one gateway.
- **`/goal` command**: recently added, analogous to CC's goal-setting flow.
- **Export/copy features**: useful for your use case of uploading AI responses to a blog — these were added in recent updates.
- **Harness / trajectory mode**: batch trajectory generation and trajectory compression for training the next generation of tool-calling models — research-ready from day one. This is a differentiating feature for your fine-tuning interests.

---

### Hermes vs. Claude Code (CC) — Key Differences

| Dimension | Hermes Agent | Claude Code |
|---|---|---|
| License | Fully open source | Proprietary (partially leaked) |
| Model lock-in | Any OpenAI-compatible endpoint | Claude models only |
| Cost | Self-hosted, nearly free | Priced per token via relay/API |
| Memory | Persistent, session-spanning | Resets per session |
| Skills system | Open standard (agentskills.io), auto-generated | Via CLAUDE.md / manual config |
| Maturity | ~3 months old (Feb 2026) | ~1 year of battle-testing |
| Subagents | Yes, built-in | Yes, but newer |

Hermes is more aggressive and innovative in its update cadence — weekly releases, community PRs. CC is still more reliable for pure coding tasks where you need maximum context and tool precision.

---

### The Plagiarism Controversy (EvoMap / Evolver)

This is real and worth understanding clearly. EvoMap, a Shenzhen-based startup, accused Hermes Agent of heavily replicating its self-evolving engine Evolver's code structure without credit. The self-evolving architecture and module structure bore a striking resemblance to Evolver, according to EvoMap, and Hermes had not cited or credited Evolver anywhere in its source code or public channels.

The evidence cited includes: a 10-step main loop that corresponds one-to-one between the two projects, a systematic replacement of 12 sets of core terminology, and zero attribution in seven public materials.

Nous Research's official account initially responded: "Our repo was created in July 2025. We are pioneers of fundamental technology... Delete your account." This response quickly sparked public outcry, and was later deleted.

The article also acknowledges facts favorable to Hermes: the Hermes Agent repository was created in July 2025 — six months before Evolver — but remained private until late February 2026. Hermes' self-evolution module uses the academic framework GEPA from Stanford/Berkeley (ICLR 2026 Oral), unrelated to Evolver's framework. The two projects use different languages (JavaScript vs. Python), and no code-level copying has been found. EvoMap's argument rests on probabilistic reasoning — that the simultaneous alignment across more than ten dimensions exceeds coincidence. This argument is compelling but not conclusive.

One commentator raised the possibility that the copying may not have been deliberate, but the work of AI — AI-assisted coding tools used by developers may draw on open-source projects to generate code that looks entirely new, with variable names and file structures changed, while leaving the core design intact.

**Bottom line on this**: the architectural similarity is real and documented. Whether it was deliberate plagiarism, AI-assisted convergence, or independent parallel development remains unresolved. Nous Research's dismissive initial response ("delete your account") damaged their credibility even among neutral observers. As a user, it's fair to be aware of this while still using the tool — it does not make Hermes dysfunctional, but it reflects poorly on the project's ethics at that moment.

---

### Your Workflow Fit Assessment

Your instinct to use Hermes as a complement rather than replacement for CC makes sense:

- **GLM + OpenRouter via Hermes**: ideal. The model-switching is seamless and this is exactly what Hermes was designed for.
- **Blog export / copy feature**: good practical fit for your publishing workflow.
- **Harness / trajectory mode**: this is the most underrated feature for you specifically. If fine-tuning is a priority, generating high-quality trajectories from your own agent sessions is valuable training data.
- **Custom CLI skills (~100 commands `ww` tool)**: your approach of writing 200–300 line skill scripts yourself is more maintainable and personalized than relying on Hermes's auto-generated skills. But the two are not mutually exclusive — Hermes's skills can complement your CLI, especially for tasks you want the agent to handle autonomously.
- **CamouFox browser issue**: that was likely related to early Hermes WebUI / PTY compatibility. As of recent updates, native terminal and WebUI have been significantly stabilized.

---

### Summary Judgment

Hermes Agent is genuinely innovative — not just incrementally better than existing tools, but architecturally different in its "grow with you" philosophy. The multi-model support, subagent delegation, trajectory export, and persistent memory make it a strong fit for your open-source, HuggingFace-centric, fine-tuning-oriented workflow. The plagiarism controversy is a real shadow over the project, though technically unresolved. Use it pragmatically: its capabilities are real regardless of the controversy.

References:

- [Hermes Agent GitHub (NousResearch)](https://github.com/nousresearch/hermes-agent)
- [Hermes Agent Official Docs](https://hermes-agent.nousresearch.com/docs/)
- [Hermes Agent Homepage](https://hermes-agent.org/)
- [EvoMap plagiarism accusation — Yicai Global](https://www.yicaiglobal.com/news/chinese-ai-team-evomap-changes-ai-agents-license-after-accusing-silicon-valley-ai-lab-of-copying-code)
- [Technical comparison analysis — KuCoin News](https://www.kucoin.com/news/flash/evomap-accuses-hermes-agent-of-architectural-copying-nous-research-rebuts-73500)
- [36kr English coverage](https://eu.36kr.com/en/p/3767967755371011)
