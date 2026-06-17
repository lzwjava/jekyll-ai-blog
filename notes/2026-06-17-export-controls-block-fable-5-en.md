---
audio: false
generated: true
image: false
lang: en
layout: post
title: Export Controls Block Fable 5
translated: false
type: note
---

**Question:** Why is Claude Fable 5 currently unavailable in Claude Code?

**Answer:**

This is a US government export-control situation, not a bug or server outage.

**Timeline:**

- **June 9, 2026** — Anthropic launched Claude Fable 5, their most capable publicly released model, built for long-horizon agentic work. It shipped across the Claude API, AWS, Microsoft Foundry, and others the same day.

- **June 12, 2026** — Anthropic received a US government directive issued under national-security export-control authority, ordering it to suspend access to Fable 5 and its larger sibling, Mythos 5. The directive covered any foreign national — whether inside or outside the United States, including Anthropic's own foreign-national employees. Because Anthropic can't filter access by nationality in real time across customer contracts, employees, and cloud delivery paths, it chose to suspend both models for all customers everywhere rather than risk non-compliance.

**What Fable 5 actually was:**

Fable 5 is the public, guardrailed sibling of Mythos 5 — they share the same underlying model and published specs. Both carry a 1M token context window by default, up to 128K output tokens per request, priced at $10/M input and $50/M output tokens.

**Current status:**

Fable 5 and Mythos 5 are temporarily unavailable to all users worldwide. Opus 4.8, Sonnet 4.6, and Haiku 4.5 are operating normally. No restoration date has been announced.

**For Claude Code specifically** — the API returns a 404 `not_found_error` with the message: "Claude Fable 5 is not available. Please use Opus 4.8."

**What to do:** Switch to `claude-opus-4-8` or `claude-sonnet-4-6` in your Claude Code config. Both are fully operational.

**References:**

- [Anthropic statement on Fable/Mythos access](https://www.anthropic.com/news/fable-mythos-access)
- [InfoQ: Anthropic Releases and Temporarily Suspends Claude Fable 5](https://www.infoq.com/news/2026/06/claude-5-release/)
- [Claude Code GitHub Issue #68121](https://github.com/anthropics/claude-code/issues/68121)
