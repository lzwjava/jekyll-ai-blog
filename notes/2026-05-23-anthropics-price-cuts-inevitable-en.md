---
audio: false
generated: true
image: false
lang: en
layout: post
title: Anthropic's Price Cuts Inevitable
translated: false
type: note
---

Question: You've built a Hermes plugin that saves agent responses directly to your blog via a `/note` command, avoiding terminal switching. You've been using Hermes + Chinese LLMs for a week and haven't looked back at Claude Code + Opus. Based on this, will Anthropic lower prices soon?

Answer:

Solid workflow — cutting the context-switch tax from agent → `ww note` → GitHub push into a single `/note` command is exactly the kind of tooling that compounds. The "build for yourself first, share the process" philosophy is the right one — most good dev tools started that way.

On your pricing prediction:

**Yes, almost certainly — the question is timing and magnitude.**

The structural forces are overwhelming:

**Supply side**
- Inference cost per token has been dropping ~10x every ~18 months (consistent since GPT-3)
- Distillation + speculative decoding + MLA (DeepSeek's multi-head latent attention) are compressing costs at the architecture level, not just hardware
- DeepSeek V3/R1 proved you can train frontier-quality models for ~$6M — Anthropic's moat is narrowing

**Competitive pressure**
- DeepSeek, Qwen 3, Doubao — you're living proof: you switched and didn't miss Opus for a week
- Google Gemini 2.5 Pro is competitive and cheaper
- OpenAI is in a perpetual price war with itself (o3-mini, GPT-4o price cuts)

**Anthropic's specific situation**
- Claude 3 Haiku → Claude 3.5 Haiku was already a significant price/performance jump
- Sonnet 3.7 → 4.x pricing has been relatively flat but capability jumped
- They need API volume to fund training runs — **lower prices = more volume = more revenue at scale**

**Your timeline estimate: 6-12 months**

Reasonable. My read:
- **3-6 months**: Haiku-tier gets another cut, Sonnet becomes the new "affordable frontier"  
- **6-12 months**: Opus-tier pricing drops significantly as the next model tier obsoletes it
- **Wildcard**: If DeepSeek R2 or Qwen 4 hits another capability jump, Anthropic accelerates cuts defensively

The pattern from OpenAI's history: prices drop when (a) a new model makes the old one obsolete, or (b) a competitor forces the hand. Both conditions are converging.

**The irony**: your Hermes + domestic LLM setup is exactly the market signal that makes Anthropic cut prices faster. Every engineer who defects is a data point they track.

What's your cost/token on the Chinese models vs what you were paying for Opus? Curious if it's purely price-driven or if latency/context window matters more for your workflow.