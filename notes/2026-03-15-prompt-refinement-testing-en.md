---
audio: false
generated: true
image: false
lang: en
layout: post
title: Prompt Refinement Through Empirical Testing
translated: false
type: note
---

Question: How does the Claude Code team develop and refine its system prompts and skills — do they use methods like adding/removing prompt sections and running interference tests to compare whether a prompt has any measurable effect?

Answer:

Yes, your intuition is essentially correct. The Claude Code team uses a rigorous, iterative, empirical methodology to develop and refine system prompts and skills — and the process goes well beyond simple guessing. Here is a comprehensive breakdown of how it works:

---

## 1. Early-Stage: Fast Feedback Iteration

Claude Code started with fast iteration based on feedback from Anthropic employees and external users. In this early phase, the team would add or change prompt content, deploy it internally (a process called "dogfooding"), and observe qualitative differences in behavior — exactly the informal "add/remove a prompt and see if it matters" method you described.

---

## 2. Adding Formal Evals (Evaluations)

Later, they added evals — first for narrow areas like concision and file edits, and then for more complex behaviors like over-engineering. These evals helped identify issues, guide improvements, and focus research-product collaborations.

Evals are essentially automated test suites that measure whether the model behaves as intended. Automated evaluations can be run against an agent in thousands of tasks without deploying to production or affecting real users.

---

## 3. A/B Testing and Production Monitoring

Combined with production monitoring, A/B tests, user research, and more, evals provide signals to continue improving Claude Code as it scales.

This is the "interference test" concept you mentioned: two versions of a prompt run in parallel, and the team compares outcomes to determine whether a particular prompt clause has a real measurable effect or is just noise.

---

## 4. The Modular System Prompt Architecture

Rather than one giant monolithic system prompt, Claude Code's system prompts are highly modular. They include individual prompt sections like "Doing tasks (avoid over-engineering)," "Doing tasks (no premature abstractions)," "Doing tasks (no compatibility hacks)," and "Doing tasks (no time estimates)" — each independently scoped and token-counted.

This modular design enables the team to isolate individual prompt sections and test whether removing, adding, or rewording them affects model behavior — which is essentially controlled ablation testing.

---

## 5. Skills: The "Skill Creator" and Evals Pipeline

For skills (modular SKILL.md files that extend Claude Code's capabilities), Anthropic formalized the development methodology further with **Claude Code Skills 2.0** (updated March 3, 2026).

The updated framework includes: developing test cases and benchmarks to measure a skill's impact on task performance; iteratively refining skill descriptions to improve triggering accuracy and reliability; and using training and testing datasets to make precise adjustments.

The updated skill-creator now operates with four composable sub-agents working in parallel: an executor that runs skills against eval prompts; a grader that evaluates outputs against defined expectations; a comparator that performs blind A/B comparisons between skill versions; and an analyzer that surfaces patterns that aggregate stats might hide.

---

## 6. Benchmark Mode: "Does This Skill/Prompt Actually Help?"

Benchmark mode runs a standardized evaluation across the entire eval set and records metrics. The benchmark compares performance with the skill active vs. without the skill (baseline), displayed side by side, giving objective data to answer the fundamental question: "Does this skill actually improve things?"

There is also a concept called **outgrowth detection**: if the base model passes the evals even without the skill loaded, the system tells you "Drop the skill; the model has become good enough on its own." This prevents dead prompt weight from accumulating over time.

---

## 7. Prompt Optimization via Iteration Algorithm

Prompt optimization meaningfully improves even top-tier coding agents — optimizing only Claude Code's system prompt yielded 5%+ gains in general coding performance, and even larger gains when specialized to a single repository. The process uses train/test splits of benchmark tasks (such as SWE-Bench) to verify that prompt changes generalize rather than just overfit.

---

## Summary

| Method | Description |
| --- | --- |
| Fast feedback / dogfooding | Internal use and user feedback in early stages |
| Eval-driven development | Automated test suites for specific behaviors |
| A/B testing | Side-by-side prompt version comparison in production |
| Ablation / modular prompts | Isolate and test individual prompt sections |
| Benchmark mode | Active vs. baseline comparison with metrics |
| Outgrowth detection | Identify and remove prompts the model no longer needs |

So yes — your description is accurate. The team does add and remove prompt clauses and run "interference"-style comparisons, but at scale and with formal evaluation infrastructure to make the results statistically meaningful rather than anecdotal.

References:

- [Anthropic: Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [Piebald-AI: Claude Code System Prompts (GitHub)](https://github.com/Piebald-AI/claude-code-system-prompts)
- [Claude Code Skills 2.0: Evals, Benchmarks and A/B Testing](https://www.pasqualepillitteri.it/en/news/341/claude-code-skills-2-0-evals-benchmarks-guide)
- [Tessl: Anthropic Brings Evals to Skill-Creator](https://tessl.io/blog/anthropic-brings-evals-to-skill-creator-heres-why-thats-a-big-deal/)
- [Arize: CLAUDE.md Best Practices from Prompt Learning](https://arize.com/blog/claude-md-best-practices-learned-from-optimizing-claude-code-with-prompt-learning/)
- [Geeky Gadgets: Claude Code Skills 2.0](https://www.geeky-gadgets.com/anthropic-skill-creator/)
