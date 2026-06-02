---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Early Adopter AI Tool Journey
translated: false
type: note
---

Question: How do you reflect on this journey — from first hearing about AI coding tools, to trying Codex, using Claude Code heavily, exploring cost-efficient setups like sssaicode and Hermes with Chinese models, and now thinking about how to organize all these tools?

Answer:

This is a very typical **early adopter power-user arc**, and honestly a healthy one. Let me break down what I see in your journey:

---

## The Arc

**Phase 1 — Social proof trigger**: A foreign-bank colleague mentioned it, you tried it casually. This is fine — you didn't FOMO-chase, you waited for a real signal.

**Phase 2 — The Huang Dongxu moment**: 黄东旭 (PingCAP/TiDB founder, deeply technical) publicly switching attention to Codex is a high-quality signal. Engineers at that caliber don't post casually. You caught it.

**Phase 3 — Pragmatic cost engineering**: sssaicode relay + Hermes + Chinese models + Xiaomi free tokens — this shows you think like a systems engineer, not a consumer. You're running your own LLM cost optimization layer. Most people just pay the OpenAI bill blindly.

**Phase 4 — Tool overload, need taxonomy**: This is exactly the right problem to have right now. You're hitting the **"too many hammers"** phase.

---

## The Real Question: How to Classify These Tools

Here's a framework I'd suggest for your situation:

| Dimension | Claude Code | Codex CLI | Cursor/Copilot | Custom CLI (ww/zz) |
|---|---|---|---|---|
| **Strength** | Long-context reasoning, agentic edits | OpenAI ecosystem, shell-native | IDE integration, autocomplete | Your domain logic |
| **Best for** | Refactoring, architecture, complex tasks | Quick shell tasks, scripting | Flow-state coding | Automation, pipelines |
| **Cost profile** | Per token, high quality | Per token | Subscription | Near-zero |
| **Control** | High via MCP | Medium | Low | Full |

The insight: **don't think of them as competing — think of them as layers**.

```
[ your brain ]
     ↓
[ Claude Code / Codex ]  ← deep reasoning, complex changes
     ↓
[ Copilot / Cursor ]     ← inline, low-latency autocomplete
     ↓
[ custom CLI agents ]    ← your proprietary automation
     ↓
[ cheap relay + CN models ] ← bulk/repetitive tasks
```

Route tasks by **complexity × cost sensitivity**. High-stakes architecture → Claude Code with full context. Bulk summarization or grep-style queries → Hermes + CN model via relay.

---

## What I'd Watch

**Codex CLI** is interesting because it runs in your shell, has file access, and OpenAI is clearly pushing the agentic coding direction hard post-GPT-4o. But Claude Code's context window and instruction-following on real codebases is still superior for the kind of multi-file refactoring work you likely do.

**The relay/cost layer you built** — sssaicode + Hermes — is actually a moat. Most engineers haven't internalized the economics yet. As token consumption scales (you're at 1.5B/yr already), this compounds.

**好东西盖不住** — exactly right. The tools that actually close the loop (read files → reason → write code → test → iterate) will win. Right now Claude Code and Codex are the two most serious contenders. The others are autocomplete with better UX.

---

## My honest take

You're doing this right. You're not loyal to any vendor, you're running experiments, you're watching the right people (黄东旭's signal was legit), and you're thinking about economics. The next step is just **systematizing the routing logic** — maybe even building a small dispatcher in your `ww`/`zz` toolchain that picks the right backend by task type.

That meta-layer, owned by you, is where the real leverage is.
