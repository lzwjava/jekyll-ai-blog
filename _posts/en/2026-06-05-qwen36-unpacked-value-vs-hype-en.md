---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Qwen3.6 Unpacked: Value vs. Hype"
translated: false
type: note
---

Question: **Qwen3.6-35B-A3B Uncensored — is this actually a major breakthrough, or marketing?**

---

## Answer

**TL;DR**: Solid inference engineering, oversold marketing. The real value is **quantization + llama.cpp**, not model capability. The "uncensored" framing obscures what's actually happening.

### What's Technically Real

**MoE + GGUF quantization is genuinely useful:**
- 35B params / 3B activation (MoE sparsity) is real and borrowed from DeepSeek architecture
- GGUF quantization at Q4_K_M gets you ~90-95% model quality at 60-65% VRAM
- Running on 6-8GB is achievable with IQ2_M (6GB) or Q4_K_M (10-12GB)
- llama.cpp's inference speed **is faster/more stable** than ollama/LM Studio by a wide margin—this part isn't hype

**Multimodal support is real:**
- Qwen 3.6 base has vision, and llama.cpp now handles multimodal properly with `--mmproj`
- This is legitimately useful for local vision workflows

### What's Marketing Fluff

**"Uncensored" ≠ "smarter"**

What they actually did: removed safety fine-tuning layers. This doesn't make the model more capable—it just removes refusals on certain prompts. Technical reality:
- Safety fine-tuning typically costs 1-3% benchmark performance (negligible)
- The "aggressiveness" is achieved via system prompts + LoRA or post-training, not model structure
- You're not getting new reasoning ability—you're just bypassing guardrails

**Benchmark claims need verification:**

The blog claims "first tier among 40B models" on Artificial Analysis. I'd check this directly on their leaderboard before taking it at face value. Marketing blogs often cherry-pick metrics or test conditions.

### The Real Play Here

If you deploy this locally on your workstation (RTX 4070 + 12GB VRAM), what you're actually getting:

```bash
# This is the real win:
llama-server \
  -m qwen3.6-35b-q4_k_m.gguf \
  -ngl 999 \
  -c 131072 \
  --host 127.0.0.1 --port 8080
```

**Actual benefits:**
- **Zero latency, zero token costs** (local inference)
- **No API quotas**—vibe code with unlimited context windows
- **Vision + text** in one model locally
- **Agent integration** (Hermes/OpenClaw) without API overhead

This is legitimately valuable for your workflow if you're building CLI agents or automated systems that need reasoning + vision.

### Critical Questions to Ask

1. **Benchmark reality check**: Does it actually outperform unquantized deepseek-v4-flash or mimo-2.5-pro on your actual workloads? (Not on Artificial Analysis—in real code/reasoning tasks)

2. **Why Qwen base?** It's respectable, but is there a reason beyond "available for jailbreak"? What about Llama 3.1 405B quantized, or waiting for deepseek-v4 quantized variants?

3. **Safety removal trade-offs**: If you're building products or tools that interact with external systems, removed safety layers can become liability (hallucinations on API calls, etc). This matters more than the "freedom" narrative suggests.

4. **Multimodal quality**: How does the vision actually perform vs Claude 3.5 Vision or deepseek-v4-vision for code/UI analysis? Real test: screenshot of a complex dashboard → does it extract data accurately?

### What I'd Actually Test

```bash
# On your 4070, compare:
# 1. qwen3.6-35b-q4_k_m (this model, uncensored)
# 2. deepseek-v4-flash quantized (if available)
# 3. Your existing mimo-2.5-pro setup via API

# Benchmark: 5 real tasks from your CLI agent work
# - Code generation + execution
# - Long-context reasoning (>8K tokens)
# - Vision analysis on screenshots
# - Tool calling accuracy

# Winner = actual value, not hype
```

### The Honest Assessment

This is a **solid local inference setup**, but it's not a "breakthrough." You're getting:
- ✅ **Free, uncapped inference** on decent hardware
- ✅ **Multimodal locally** (genuinely useful)
- ✅ **Fast serving** via llama.cpp (real optimization)
- ❌ **Not fundamentally smarter** (safety removal ≠ capability upgrade)
- ❌ **Not replacing deepseek-v4-flash** for quality reasoning (probably)

**For your use case:** Worth a 30-minute test on the 4070. If it integrates well with Hermes/OpenClaw and reduces API costs for your agent work without sacrificing reasoning, adopt it. Otherwise, keep deepseek-v4-flash for production reasoning + local multimodal for vision tasks.

The real technical question isn't "is it uncensored?" but "does it save you money and tokens while keeping quality?" That's measurable.
