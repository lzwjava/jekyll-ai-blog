---
audio: false
generated: true
image: false
lang: en
layout: post
title: Freebuff vs Codebuff Explained
translated: false
type: note
---

**Question:** What is the relationship between freebuff.ai and Codebuff?

**Answer:**

**Freebuff is the free, ad-supported tier of Codebuff** — same company, same codebase, different monetization model.

Here's the full picture:

**Codebuff** (`codebuff.com`) is a paid terminal coding agent built by [CodebuffAI](https://github.com/CodebuffAI/codebuff). It supports any model on OpenRouter (Claude, GPT, DeepSeek, Qwen, etc.) and uses TypeScript generators for custom agentic workflows where agents can spawn subagents, branch on conditions, and run multi-step processes. Pricing starts at $49/mo, going up to $249/mo.

**Freebuff** (`freebuff.com` / `npm i -g freebuff`) is the free variant of Codebuff — no subscription, no credits, no configuration. It's supported by ads shown in the CLI and claims 3–5× tokens per second compared to Claude, with built-in web research and browser use.

Key technical details about Freebuff:
- Default models are DeepSeek V4 Pro (smartest, but its API collects data for training) or DeepSeek V4 Flash as the main coding agent.
- Supports `@filename` for file references, `@AgentName` for specialized agents, `!command` or `/bash` for terminal commands, and `knowledge.md` for project-level context.
- Uses GitHub OAuth to authenticate users and manage daily usage quotas.

**Founder context:** Founded by James Grugett, who previously built Manifold Markets (150K users, millions of views/month). The strategy is to make consumer agent products completely free using the best open-source models, funded by ads — with Freebuff as the entry point and Codebuff as the paid upsell.

**TL;DR for your workflow:** Freebuff = Claude Code competitor, free, DeepSeek-powered, ad-supported CLI agent. Worth trying given you're already deep in DeepSeek V4 Flash/Pro. The data-training caveat on DeepSeek V4 Pro is worth noting if you're running it on bank code.

**References:**

- [CodebuffAI/codebuff GitHub](https://github.com/CodebuffAI/codebuff)
- [freebuff README](https://github.com/CodebuffAI/codebuff/blob/main/freebuff/README.md)
- [freebuff on npm](https://www.npmjs.com/package/freebuff)
- [Freebuff on YC](https://www.ycombinator.com/companies/freebuff)
