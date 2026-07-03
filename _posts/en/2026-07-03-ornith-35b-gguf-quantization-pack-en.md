---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ornith-35B GGUF Quantization Pack
translated: false
type: note
---

**Question:** What is `deepreinforce-ai/Ornith-1.0-35B-GGUF` on Hugging Face?

**Answer:**

It's a brand-new release (the collection was updated hours ago). Ornith-1.0 is a self-improving family of open-source models for agentic coding from the DeepReinforce team, and this particular repo is the **GGUF quantization pack of the 35B-MoE member** — i.e., the llama.cpp/Ollama-ready build for local single-GPU/CPU-hybrid deployment.

Key facts:

**Lineage & family.** The family ships in 9B-Dense, 31B-Dense, 35B-MoE, and 397B-MoE sizes, post-trained on top of Gemma 4 and Qwen 3.5. The GGUF metadata confirms the 35B is `qwen35moe` architecture — so it's a Qwen 3.5 MoE base with heavy RL post-training for coding agents. MIT licensed, no regional restrictions.

**The interesting part — scaffold-generating RL.** The training framework uses RL where the model learns to generate not only solution rollouts, but also the scaffold that drives those rollouts; by jointly optimizing the scaffold and resulting solution, the model discovers better search trajectories. This is a step beyond standard agentic RL (GRPO-on-SWE-tasks style): instead of fixing the harness (system prompt, tool loop, planning structure) and only optimizing the policy inside it, the policy also emits its own harness. Conceptually it's meta-RL over the agent loop itself — the reward signal flows through both the scaffold choice and the trajectory it induces. Given your interest in agent architectures, the blog at deep-reinforce.com/ornith.html is worth reading for the actual objective formulation.

**Benchmarks (per the model card, self-reported).** The 35B scores 64.2 on Terminal-Bench 2.1 (Terminus-2) vs 41.4 for Qwen3.5-35B, and 75.6 on SWE-bench Verified vs 70 for Qwen3.5-35B — roughly matching the 397B Qwen3.5 (76.4) at ~11x smaller size. It's a reasoning model: assistant turns open with a `<think>…</think>` block, and the serving recipes enable a reasoning parser plus a qwen3 tool-call parser so `<tool_call>` blocks surface as OpenAI-style `tool_calls`. Usual caveat: vendor-reported numbers on a launch-day card; wait for independent Terminal-Bench runs.

**Quant sizes in this repo:** Q4_K_M 21.2 GB, Q5_K_M 24.7 GB, Q6_K 28.5 GB, Q8_0 36.9 GB, BF16 69.4 GB.

For your hardware:

- **RTX 4070 (12 GB) box**: Q4_K_M won't fit in VRAM, but this is exactly the case where MoE + llama.cpp hybrid offload shines — only a fraction of the 35B params are active per token, so with 62 GB RAM you can keep experts on CPU and attention/shared layers on GPU (`--n-gpu-layers` partial, or `--override-tensor "exp=CPU"` style expert offload). Expect usable but not fast tok/s.
- **MI300X (192 GB)**: run the full BF16 safetensors (`deepreinforce-ai/Ornith-1.0-35B`, non-GGUF repo) under vLLM with `--reasoning-parser qwen3 --tool-call-parser qwen3_xml`, then point OpenCode/OpenHands/your own `ww`/`iclaw` agents at the OpenAI-compatible endpoint. Recommended sampling: temp 0.6, top_p 0.95.
- **MacBook Air M2 16 GB**: skip it; even Q4 is too big.

Quick test on the workstation:

```bash
llama-server -hf deepreinforce-ai/Ornith-1.0-35B-GGUF:Q4_K_M -c 32768 --port 8000
# then point any OpenAI-compatible agent CLI at http://localhost:8000/v1
```

Given it's explicitly optimized for terminal coding agents (they even benchmarked it *inside* Claude Code as the harness), it'd be a natural candidate to slot into your CLI agent stack as a local/cheap tier.

**References:**

- [deepreinforce-ai/Ornith-1.0-35B-GGUF · Hugging Face](https://huggingface.co/deepreinforce-ai/Ornith-1.0-35B-GGUF)
- [Ornith blog — DeepReinforce](https://deep-reinforce.com/ornith.html)
